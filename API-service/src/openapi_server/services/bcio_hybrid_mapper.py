import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Iterable, Tuple

import numpy as np
from pymilvus import (
    connections,
    MilvusClient,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
from pymilvus.model.hybrid import BGEM3EmbeddingFunction


def _iter_jsonl(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def _best_label(rec: dict) -> str:
    pref = rec.get("preferred_labels") or []
    if isinstance(pref, list) and len(pref) > 0 and str(pref[0]).strip():
        return str(pref[0]).strip()

    labels = rec.get("labels") or []
    if isinstance(labels, list) and len(labels) > 0 and str(labels[0]).strip():
        return str(labels[0]).strip()

    name = rec.get("name")
    if name:
        return str(name)

    iri = rec.get("iri", "")
    return iri.rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _clip01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def _dense_ip_to_prob(ip: float) -> float:
    """
    If embeddings are L2-normalized, inner product ~= cosine similarity in [-1, 1].
    Map to [0, 1] by (cos + 1)/2.
    """
    return _clip01((ip + 1.0) / 2.0)


def _sparse_ip_to_prob(ip: float) -> float:
    """
    Sparse IP is usually >= 0, unbounded.
    Map to [0, 1) with a monotonic squashing: ip / (ip + 1).
    """
    if ip <= 0:
        return 0.0
    return _clip01(ip / (ip + 1.0))


def _sanitize_collection_name(name: str) -> str:
    # Milvus: only allows letters/digits/underscore, and must start with letter or underscore
    name = re.sub(r"[^0-9a-zA-Z_]+", "_", name)
    if not re.match(r"^[A-Za-z_]", name):
        name = f"c_{name}"
    return name


class BCIOHybridMapper:
    """
    Build a hybrid (dense+sparse) index in Milvus from concepts_*.jsonl,
    then map a short sentence to top BCIO concepts.

    Output format (list):
    [
      {"bcio_label": "...", "iri": "...", "probability": 0.96},
      ...
    ]

    If debug=True, each item additionally includes:
      dense_ip, dense_prob, sparse_ip, sparse_prob, fused_prob
    """

    def __init__(
        self,
        milvus_uri: str = "http://localhost:19530",
        collection_name: Optional[str] = None,
        jsonl_path: str = "concepts_bcio_only.jsonl",
        device: str = "cpu",
        use_fp16: bool = False,
        entity_types: Tuple[str, ...] = ("Class",),  # usually only classes for mapping
        dense_weight: float = 0.65,  # dense vs sparse fusion weight
    ):
        self.milvus_uri = milvus_uri
        self.jsonl_path = Path(jsonl_path)
        auto_name = _sanitize_collection_name(f"{self.jsonl_path.stem}_hybrid")
        self.collection_name = collection_name or auto_name
        self.entity_types = entity_types
        self.dense_weight = float(dense_weight)

        # Connect once
        connections.connect(uri=self.milvus_uri)
        self.client = MilvusClient(uri=self.milvus_uri)

        # Embedding function (dense+sparse)
        self.ef = BGEM3EmbeddingFunction(use_fp16=use_fp16, device=device)

        # Prepare collection handle (create if needed)
        self.collection = self._ensure_collection()

    def _ensure_collection(self) -> Collection:
        if self.client.has_collection(self.collection_name):
            return Collection(self.collection_name)

        # Schema: use INT64 auto_id
        fields = [
            FieldSchema(name="pk", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="iri", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="label", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="etype", dtype=DataType.VARCHAR, max_length=32),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=32),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=16384),
            FieldSchema(name="sparse_vector", dtype=DataType.SPARSE_FLOAT_VECTOR),
            FieldSchema(name="dense_vector", dtype=DataType.FLOAT_VECTOR, dim=self.ef.dim["dense"]),
        ]
        schema = CollectionSchema(fields, description="BCIO concept cards hybrid index (dense+sparse)")
        collection = Collection(name=self.collection_name, schema=schema, consistency_level="Strong")

        # Indexes
        sparse_index = {"index_type": "SPARSE_INVERTED_INDEX", "metric_type": "IP"}
        dense_index = {"index_type": "AUTOINDEX", "metric_type": "IP"}
        collection.create_index("sparse_vector", sparse_index)
        collection.create_index("dense_vector", dense_index)

        return collection

    def index_if_needed(self, batch_size: int = 256, rebuild: bool = False) -> None:
        """
        Build index data if collection empty (or rebuild=True).
        """
        if rebuild and self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)
            self.collection = self._ensure_collection()

        # quick empty check
        try:
            n = self.collection.num_entities
        except Exception:
            n = 0

        if n and n > 0:
            # already indexed
            self.collection.load()
            return

        if not self.jsonl_path.exists():
            raise FileNotFoundError(f"JSONL not found: {self.jsonl_path.resolve()}")

        # Load records
        records = []
        for rec in _iter_jsonl(self.jsonl_path):
            if self.entity_types and rec.get("type") not in self.entity_types:
                continue
            txt = rec.get("text") or ""
            if not str(txt).strip():
                continue
            records.append(rec)

        if not records:
            raise ValueError("No usable records found in JSONL (after filtering).")

        # Batch insert
        for start in range(0, len(records), batch_size):
            batch = records[start: start + batch_size]

            iris = [str(r.get("iri", "")) for r in batch]
            labels = [_best_label(r) for r in batch]
            etypes = [str(r.get("type", "")) for r in batch]
            sources = [str(r.get("source", "")) for r in batch]
            texts = [str(r.get("text", ""))[:16384] for r in batch]  # safe truncate

            emb = self.ef(texts)
            sparse_vecs = emb["sparse"]
            dense_vecs = emb["dense"]

            self.collection.insert(
                [
                    iris,
                    labels,
                    etypes,
                    sources,
                    texts,
                    sparse_vecs,
                    dense_vecs,
                ]
            )

        self.collection.flush()
        self.collection.load()

    def map_sentence(
        self,
        sentence: str,
        threshold: float = 0.8,
        top_n: int = 5,
        search_k: Optional[int] = None,
        expr: Optional[str] = None,
        debug: bool = True,
    ) -> List[Dict]:
        """
        Input:
          - sentence: short text
          - threshold: fused probability threshold in [0,1]
          - top_n: max number of mappings to return
          - search_k: internal recall size (default: max(50, top_n*10))
          - expr: optional Milvus filter, e.g. 'source == "BCIO"' or 'etype == "Class"'
          - debug: if True, return dense/sparse raw IP scores and mapped probs

        Output:
          List of dicts. Always includes:
            bcio_label, iri, probability
          If debug=True, also includes:
            dense_ip, dense_prob, sparse_ip, sparse_prob, fused_prob
        """
        if not sentence or not str(sentence).strip():
            return []

        threshold = float(threshold)
        if search_k is None:
            search_k = max(50, int(top_n) * 10)

        # Ensure loaded
        self.collection.load()

        # Embed query
        qemb = self.ef([sentence])
        q_dense = qemb["dense"][0]
        q_sparse = qemb["sparse"]._getrow(0)

        search_params = {"metric_type": "IP", "params": {}}
        out_fields = ["iri", "label", "etype", "source"]

        # Dense search
        dense_hits = self.collection.search(
            [q_dense],
            anns_field="dense_vector",
            param=search_params,
            limit=search_k,
            expr=expr,
            output_fields=out_fields,
        )[0]

        # Sparse search
        sparse_hits = self.collection.search(
            [q_sparse],
            anns_field="sparse_vector",
            param=search_params,
            limit=search_k,
            expr=expr,
            output_fields=out_fields,
        )[0]

        # Collect raw IP scores by IRI
        dense_by_iri: Dict[str, float] = {}
        sparse_by_iri: Dict[str, float] = {}
        meta_by_iri: Dict[str, Dict] = {}

        for h in dense_hits:
            iri = h.entity.get("iri")
            if not iri:
                continue
            dense_by_iri[iri] = float(h.distance)  # dense_ip
            meta_by_iri.setdefault(
                iri,
                {
                    "iri": iri,
                    "label": h.entity.get("label") or iri,
                    "etype": h.entity.get("etype"),
                    "source": h.entity.get("source"),
                },
            )

        for h in sparse_hits:
            iri = h.entity.get("iri")
            if not iri:
                continue
            sparse_by_iri[iri] = float(h.distance)  # sparse_ip
            meta_by_iri.setdefault(
                iri,
                {
                    "iri": iri,
                    "label": h.entity.get("label") or iri,
                    "etype": h.entity.get("etype"),
                    "source": h.entity.get("source"),
                },
            )

        # Fuse
        w = _clip01(self.dense_weight)
        all_iris = set(dense_by_iri.keys()) | set(sparse_by_iri.keys())

        fused_rows = []
        for iri in all_iris:
            dense_ip = dense_by_iri.get(iri, None)
            sparse_ip = sparse_by_iri.get(iri, None)

            dense_prob = _dense_ip_to_prob(dense_ip) if dense_ip is not None else 0.0
            sparse_prob = _sparse_ip_to_prob(sparse_ip) if sparse_ip is not None else 0.0

            fused_prob = w * dense_prob + (1.0 - w) * sparse_prob

            if fused_prob >= threshold:
                fused_rows.append(
                    {
                        "iri": iri,
                        "dense_ip": dense_ip,
                        "dense_prob": dense_prob,
                        "sparse_ip": sparse_ip,
                        "sparse_prob": sparse_prob,
                        "fused_prob": fused_prob,
                    }
                )

        fused_rows.sort(key=lambda r: r["fused_prob"], reverse=True)
        fused_rows = fused_rows[: int(top_n)]

        # Build output
        out = []
        for r in fused_rows:
            iri = r["iri"]
            meta = meta_by_iri.get(iri, {"iri": iri, "label": iri})

            item = {
                "bcio_label": meta.get("label") or iri,
                "iri": iri,
                "probability": float(round(r["fused_prob"], 4)),
            }

            if debug:
                item.update(
                    {
                        "dense_ip": None if r["dense_ip"] is None else float(round(r["dense_ip"], 6)),
                        "dense_prob": float(round(r["dense_prob"], 4)),
                        "sparse_ip": None if r["sparse_ip"] is None else float(round(r["sparse_ip"], 6)),
                        "sparse_prob": float(round(r["sparse_prob"], 4)),
                        "fused_prob": float(round(r["fused_prob"], 4)),
                    }
                )

            out.append(item)

        return out


# Example usage
if __name__ == "__main__":
    mapper = BCIOHybridMapper(
        milvus_uri="http://localhost:19530",
        jsonl_path="Ontologies/concepts_all_merged.jsonl",
        device="cuda",
        use_fp16=False,
        entity_types=("Class", "ObjectProperty"),
        dense_weight=0.8,
    )

    mapper.index_if_needed(batch_size=256, rebuild=True)

    query = """Label: behaviour change intervention delivery
Definition: An intervention delivery in which the intervention is a behaviour change intervention."""
    mappings = mapper.map_sentence(
        query,
        threshold=0.0,
        top_n=5,
        expr='etype in ["Class", "ObjectProperty"]',
        debug=False,
    )

    print(json.dumps({"bcio_mappings": mappings}, ensure_ascii=False, indent=2))
