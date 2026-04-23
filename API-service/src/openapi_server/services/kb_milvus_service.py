from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional, Set, Tuple

# import kb_min
try:
    from .kb_min import build_kb_min_from_pdf, KbDocMeta, KbChunk  # type: ignore
except ImportError:
    SRC_DIR = Path(__file__).resolve().parents[2]  # .../src
    sys.path.insert(0, str(SRC_DIR))
    from openapi_server.services.kb_min import build_kb_min_from_pdf, KbDocMeta, KbChunk  # type: ignore

from unstructured.partition.pdf import partition_pdf  # type: ignore

from pymilvus import (  # type: ignore
    connections,
    utility,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
)

try:
    from .clients import get_client  # type: ignore
except ImportError:
    SRC_DIR = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(SRC_DIR))
    from openapi_server.services.clients import get_client  # type: ignore


OPENAPI_SERVER_DIR = Path(__file__).resolve().parents[1]
DEFAULT_KB_ROOT = OPENAPI_SERVER_DIR / "kb"
DEFAULT_META_DIR = DEFAULT_KB_ROOT / "_meta"


# -----------------------
# Config
# -----------------------
@dataclass
class KbMilvusConfig:
    kb_root: Path
    meta_dir: Path
    milvus_uri: str
    collection_name: str

    embed_provider: str
    embed_model: str
    embed_dim: int
    embed_device: str
    embed_fp16: bool

    exclude_dirs: Set[str]
    embed_batch_size: int
    normalize_embeddings: bool


def load_config(
    kb_root: Optional[str] = None,
    milvus_uri: Optional[str] = None,
    collection_name: Optional[str] = None,
) -> KbMilvusConfig:
    kb = (
        Path(kb_root).resolve()
        if kb_root
        else Path(os.getenv("KB_ROOT_DIR") or DEFAULT_KB_ROOT).resolve()
    )
    meta = Path(os.getenv("KB_META_DIR") or (kb / "_meta")).resolve()

    uri = milvus_uri or os.getenv("MILVUS_URI") or "http://localhost:19530"
    col = collection_name or os.getenv("KB_MILVUS_COLLECTION") or "kb_chunks_bgem3"

    # default to local BGE-M3
    embed_provider = (os.getenv("KB_EMBED_PROVIDER") or "bge-m3").strip()
    embed_model = (os.getenv("KB_EMBED_MODEL") or "BAAI/bge-m3").strip()

    # prefer explicit dim via env; otherwise choose by provider
    embed_dim_env = os.getenv("KB_EMBED_DIM")
    if embed_dim_env:
        try:
            embed_dim = int(embed_dim_env)
        except Exception:
            embed_dim = 1024
    else:
        embed_dim = (
            1024 if embed_provider.lower() in {"bge-m3", "bgem3", "bge_m3"} else 1536
        )

    embed_device = (os.getenv("KB_EMBED_DEVICE") or "cpu").strip()  # "cuda" / "cpu"
    embed_fp16 = (os.getenv("KB_EMBED_FP16") or "1") == "1"

    exclude_dirs = set(
        x.strip().lower()
        for x in (
            os.getenv("KB_EXCLUDE_DIRS") or "_meta,figs,__pycache__,.git,.venv"
        ).split(",")
        if x.strip()
    )

    embed_batch_size = int(os.getenv("KB_EMBED_BATCH_SIZE") or "16")
    normalize_embeddings = (os.getenv("KB_EMBED_NORMALIZE") or "1") == "1"

    return KbMilvusConfig(
        kb_root=kb,
        meta_dir=meta,
        milvus_uri=uri,
        collection_name=col,
        embed_provider=embed_provider,
        embed_model=embed_model,
        embed_dim=embed_dim,
        embed_device=embed_device,
        embed_fp16=embed_fp16,
        exclude_dirs=exclude_dirs,
        embed_batch_size=embed_batch_size,
        normalize_embeddings=normalize_embeddings,
    )


# -----------------------
# Cache
# -----------------------
def _json_dump(obj: Any) -> str:
    def default(o):
        if isinstance(o, datetime):
            return o.isoformat()
        return str(o)

    return json.dumps(obj, ensure_ascii=False, indent=2, default=default)


def _read_json(path: Path) -> Optional[dict]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_json_dump(data), encoding="utf-8")


def _meta_path(meta_dir: Path, doc_id: str) -> Path:
    return meta_dir / f"{doc_id}.json"


def _docmeta_to_cache_dict(
    doc_meta: KbDocMeta,
    source_pdf: Path,
    embed_provider: str,
    embed_model: str,
    embed_dim: int,
    chunk_count: int,
) -> dict:
    # Only these parameters changing should trigger reindex
    return {
        "doc_id": doc_meta.doc_id,
        "domain": doc_meta.domain,
        "title": doc_meta.title,
        "doc_summary": doc_meta.doc_summary,
        "ingested_at": doc_meta.ingested_at.isoformat(),
        "source_pdf": str(source_pdf),
        "pdf_mtime": source_pdf.stat().st_mtime if source_pdf.exists() else None,
        "pdf_size": source_pdf.stat().st_size if source_pdf.exists() else None,
        "indexed_at": datetime.now().astimezone().isoformat(),
        "chunk_count": int(chunk_count),
        "embed_provider": str(embed_provider),
        "embed_model": str(embed_model),
        "embed_dim": int(embed_dim),
        # ---- chunk/env snapshot ----
        "pdf_strategy": (os.getenv("KB_PDF_STRATEGY", "fast") or "fast").strip(),
        "infer_table_structure": os.getenv("KB_INFER_TABLE_STRUCTURE", "1") == "1",
        "chunk_max_characters": int(os.getenv("KB_CHUNK_MAX_CHARACTERS", "2800")),
        "chunk_new_after_n_chars": int(os.getenv("KB_CHUNK_NEW_AFTER_N_CHARS", "2400")),
        "chunk_combine_under_n_chars": int(os.getenv("KB_CHUNK_COMBINE_UNDER_N_CHARS", "900")),
        "extract_images": os.getenv("KB_EXTRACT_IMAGES", "0") == "1",
    }


def load_cached_doc_meta(meta_dir: Path, doc_id: str) -> Optional[dict]:
    p = _meta_path(meta_dir, doc_id)
    if not p.exists():
        return None
    return _read_json(p)


# -----------------------
# Helpers
# -----------------------
def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _iter_pdfs(kb_root: Path, exclude_dirs: Set[str]) -> List[Path]:
    pdfs: List[Path] = []
    if not kb_root.exists():
        return pdfs
    for p in kb_root.rglob("*.pdf"):
        parts_lower = {x.lower() for x in p.parts}
        if any(ex in parts_lower for ex in exclude_dirs):
            continue
        pdfs.append(p)
    return sorted(pdfs)


def _safe_expr_str(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _normalize(vec: List[float]) -> List[float]:
    import math

    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def _title_from_filename(pdf_path: Path) -> str:
    return pdf_path.stem.replace("_", " ").replace("-", " ").strip()


def _title_from_elements(elements, fallback: str) -> str:
    for el in elements:
        if getattr(el, "category", None) != "Title":
            continue
        t = (getattr(el, "text", None) or "").strip()
        if t:
            return t[:300].strip()
    return fallback


def _discover_domain_folders(kb_root: Path, exclude_dirs: Set[str]) -> Set[str]:
    domains: Set[str] = set()
    if not kb_root.exists():
        return domains
    for p in kb_root.iterdir():
        if not p.is_dir():
            continue
        name = (p.name or "").strip().lower()
        if not name:
            continue
        if name.startswith(".") or name.startswith("_"):
            continue
        if name in exclude_dirs:
            continue
        domains.add(name)
    return domains


def _infer_domain_from_kb_root(
    kb_root: Path, pdf_path: Path, exclude_dirs: Set[str]
) -> str:
    allowed = _discover_domain_folders(kb_root, exclude_dirs)
    rel = pdf_path.resolve().relative_to(kb_root.resolve())
    if len(rel.parts) < 2:
        raise ValueError(f"Expected kb_root/<domain>/... structure, got: {pdf_path}")
    domain = rel.parts[0].lower()
    if allowed and domain not in allowed:
        raise ValueError(
            f"Unknown domain '{domain}'. Allowed under {kb_root}: {sorted(allowed)}"
        )
    return domain


# -----------------------
# Embeddings (BGE-M3 local + OpenAI-like fallback)
# -----------------------
_BGE_M3_EF = None


def _get_bge_m3_ef(model_name: str, device: str, use_fp16: bool):
    global _BGE_M3_EF
    if _BGE_M3_EF is not None:
        return _BGE_M3_EF
    try:
        from pymilvus.model.hybrid import BGEM3EmbeddingFunction  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "BGEM3EmbeddingFunction is not available. "
            "Install/upgrade pymilvus with model support, e.g. `pip install -U pymilvus` "
            "and ensure required deps are installed."
        ) from e

    _BGE_M3_EF = BGEM3EmbeddingFunction(
        model_name=model_name,
        device=device,
        use_fp16=use_fp16,
    )
    return _BGE_M3_EF


def _bge_m3_encode_texts(
    texts: List[str], model: str, device: str, fp16: bool
) -> List[List[float]]:
    ef = _get_bge_m3_ef(model_name=model, device=device, use_fp16=fp16)

    # Prefer encode_documents for chunk text; encode_queries for search query if available.
    out = ef.encode_documents(texts)

    # expected: dict with "dense": np.ndarray
    dense = out.get("dense") if isinstance(out, dict) else None
    if dense is None:
        raise RuntimeError("BGE-M3 embedding output does not contain 'dense' vectors.")

    # dense may be numpy array
    try:
        return [v.tolist() for v in dense]
    except Exception:
        # fallback: already list
        return [list(v) for v in dense]


def _bge_m3_encode_query(text: str, model: str, device: str, fp16: bool) -> List[float]:
    ef = _get_bge_m3_ef(model_name=model, device=device, use_fp16=fp16)

    if hasattr(ef, "encode_queries"):
        out = ef.encode_queries([text])
    else:
        out = ef.encode_documents([text])

    dense = out.get("dense") if isinstance(out, dict) else None
    if dense is None:
        raise RuntimeError(
            "BGE-M3 query embedding output does not contain 'dense' vectors."
        )
    v = dense[0]
    try:
        return v.tolist()
    except Exception:
        return list(v)


def embed_texts(
    texts: List[str],
    provider: str,
    model: str,
    normalize: bool,
    *,
    bge_device: str = "cpu",
    bge_fp16: bool = True,
) -> List[List[float]]:
    if not texts:
        return []

    prov = (provider or "").lower().strip()

    # local BGE-M3
    if prov in {"bge-m3", "bgem3", "bge_m3"}:
        vecs = _bge_m3_encode_texts(
            texts, model=model, device=bge_device, fp16=bge_fp16
        )
        if normalize:
            vecs = [_normalize(v) for v in vecs]
        return vecs

    # fallback: OpenAI-like embeddings client
    client = get_client(provider, async_=False)
    resp = client.embeddings.create(model=model, input=texts)
    vecs = [d.embedding for d in resp.data]
    if normalize:
        vecs = [_normalize(v) for v in vecs]
    return vecs


def embed_query(
    text: str,
    provider: str,
    model: str,
    normalize: bool,
    *,
    bge_device: str = "cpu",
    bge_fp16: bool = True,
) -> List[float]:
    prov = (provider or "").lower().strip()

    if prov in {"bge-m3", "bgem3", "bge_m3"}:
        v = _bge_m3_encode_query(text, model=model, device=bge_device, fp16=bge_fp16)
        return _normalize(v) if normalize else v

    # fallback
    client = get_client(provider, async_=False)
    resp = client.embeddings.create(model=model, input=[text])
    v = resp.data[0].embedding
    return _normalize(v) if normalize else v


# -----------------------
# Milvus store
# -----------------------
class KbMilvusStore:
    def __init__(self, cfg: KbMilvusConfig):
        self.cfg = cfg
        self._col: Optional[Collection] = None
        self._connect_and_ensure()

    @property
    def collection(self) -> Collection:
        assert self._col is not None
        return self._col

    def _connect_and_ensure(self) -> None:
        connections.connect(uri=self.cfg.milvus_uri)

        if not utility.has_collection(self.cfg.collection_name):
            self._create_collection()
        else:
            # Validate embedding dim matches existing schema
            col = Collection(self.cfg.collection_name)
            try:
                emb_field = next(
                    (f for f in col.schema.fields if f.name == "embedding"), None
                )
                if emb_field is not None:
                    existing_dim = int(
                        getattr(emb_field, "params", {}).get("dim", 0) or 0
                    )
                    if existing_dim and existing_dim != int(self.cfg.embed_dim):
                        raise RuntimeError(
                            f"Milvus collection '{self.cfg.collection_name}' embedding dim mismatch: "
                            f"schema={existing_dim} vs cfg={self.cfg.embed_dim}. "
                            f"Fix by setting KB_EMBED_DIM to {existing_dim}, or use a new collection name, "
                            f"or run with --force to drop & rebuild."
                        )
            except Exception:
                # If schema introspection fails, continue; insert will still fail with clear dim error.
                pass

        self._col = Collection(self.cfg.collection_name)
        try:
            self._col.load()
        except Exception:
            pass

    def _create_collection(self) -> None:
        fields = [
            FieldSchema(
                name="id",
                dtype=DataType.VARCHAR,
                is_primary=True,
                auto_id=False,
                max_length=128,
            ),
            FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=80),
            FieldSchema(name="domain", dtype=DataType.VARCHAR, max_length=64),
            FieldSchema(name="chunk_id", dtype=DataType.INT64),
            FieldSchema(name="page_number", dtype=DataType.INT64),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=16384),
            FieldSchema(
                name="embedding",
                dtype=DataType.FLOAT_VECTOR,
                dim=int(self.cfg.embed_dim),
            ),
        ]
        schema = CollectionSchema(
            fields, description="KB chunks (doc_id/domain/page_number/text + embedding)"
        )
        col = Collection(
            name=self.cfg.collection_name, schema=schema, consistency_level="Strong"
        )

        # For normalized embeddings + IP => cosine-like ranking
        try:
            col.create_index(
                "embedding", {"index_type": "AUTOINDEX", "metric_type": "IP"}
            )
        except Exception:
            col.create_index(
                "embedding",
                {
                    "index_type": "HNSW",
                    "metric_type": "IP",
                    "params": {"M": 16, "efConstruction": 200},
                },
            )

    def drop_collection(self) -> None:
        if utility.has_collection(self.cfg.collection_name):
            utility.drop_collection(self.cfg.collection_name)
        self._col = None
        self._connect_and_ensure()

    def has_doc(self, doc_id: str) -> bool:
        expr = f'doc_id == "{_safe_expr_str(doc_id)}"'
        try:
            rows = self.collection.query(expr=expr, output_fields=["id"], limit=1)
            return bool(rows)
        except Exception:
            rows = self.collection.query(expr=expr, output_fields=["id"])
            return bool(rows)

    def delete_doc(self, doc_id: str) -> None:
        expr = f'doc_id == "{_safe_expr_str(doc_id)}"'
        self.collection.delete(expr=expr)
        try:
            self.collection.flush()
        except Exception:
            pass

    def list_doc_ids(self, batch_size: int = 1000) -> Set[str]:
        """
        Return all distinct doc_id values that currently exist in Milvus.

        Why this exists:
        - stale cleanup must rely on the actual contents of Milvus, not only on _meta files
        - orphan rows can remain in Milvus even when their cache json has already been deleted

        Implementation notes:
        - Prefer query_iterator() when available (more memory-safe on large collections)
        - Fall back to paged query(offset/limit)
        - Final fallback is a single query without paging
        """
        doc_ids: Set[str] = set()
        expr = 'doc_id != ""'

        # 1) Best effort: iterator API (available in newer pymilvus versions)
        try:
            iterator = self.collection.query_iterator(
                batch_size=int(batch_size),
                expr=expr,
                output_fields=["doc_id"],
            )
            while True:
                rows = iterator.next()
                if not rows:
                    break
                for row in rows:
                    doc_id = str((row or {}).get("doc_id") or "").strip()
                    if doc_id:
                        doc_ids.add(doc_id)
            try:
                iterator.close()
            except Exception:
                pass
            return doc_ids
        except Exception:
            pass

        # 2) Fallback: offset/limit paging
        try:
            offset = 0
            while True:
                rows = self.collection.query(
                    expr=expr,
                    output_fields=["doc_id"],
                    limit=int(batch_size),
                    offset=int(offset),
                )
                if not rows:
                    break
                for row in rows:
                    doc_id = str((row or {}).get("doc_id") or "").strip()
                    if doc_id:
                        doc_ids.add(doc_id)
                if len(rows) < int(batch_size):
                    break
                offset += int(batch_size)
            return doc_ids
        except Exception:
            pass

        # 3) Last resort: single query
        rows = self.collection.query(expr=expr, output_fields=["doc_id"])
        for row in rows:
            doc_id = str((row or {}).get("doc_id") or "").strip()
            if doc_id:
                doc_ids.add(doc_id)
        return doc_ids

    def upsert_chunks(
        self,
        doc_id: str,
        domain: str,
        chunks: List[KbChunk],
        vectors: List[List[float]],
    ) -> int:
        assert len(chunks) == len(vectors)

        self.delete_doc(doc_id)

        ids = [f"{doc_id}:{c.chunk_id}" for c in chunks]
        doc_ids = [doc_id] * len(chunks)
        domains = [domain.lower()] * len(chunks)
        chunk_ids = [int(c.chunk_id) for c in chunks]
        pages = [int(c.page_number) for c in chunks]
        texts = [str(c.text)[:16384] for c in chunks]
        embs = vectors

        self.collection.insert([ids, doc_ids, domains, chunk_ids, pages, texts, embs])
        try:
            self.collection.flush()
        except Exception:
            pass
        return len(chunks)

    def search(
        self, query_vec: List[float], top_k: int = 5, domain: Optional[str] = None
    ) -> List[dict]:
        expr = None
        if domain:
            expr = f'domain == "{_safe_expr_str(domain.lower())}"'

        res = self.collection.search(
            data=[query_vec],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {}},
            limit=int(top_k),
            expr=expr,
            output_fields=["doc_id", "domain", "chunk_id", "page_number", "text"],
        )

        hits = res[0] if res else []
        out: List[dict] = []
        for h in hits:
            d = h.entity
            out.append(
                {
                    "score": float(h.score),
                    "doc_id": d.get("doc_id"),
                    "domain": d.get("domain"),
                    "chunk_id": d.get("chunk_id"),
                    "page_number": d.get("page_number"),
                    "text": d.get("text"),
                }
            )
        return out


# -----------------------
# chunks-only extractor (NO LLM)
# -----------------------
def parse_pdf_chunks_no_llm(
    kb_root: Path,
    pdf: Path,
    exclude_dirs: Set[str],
    language: str = "eng",
) -> Tuple[str, str, List[KbChunk]]:
    """
    Partition PDF and produce (domain, title, chunks) WITHOUT calling any LLM.
    Must match kb_min.py chunking behavior closely.
    """
    raw_pdf_elements = partition_pdf(
        filename=str(pdf),
        extract_images_in_pdf=os.getenv("KB_EXTRACT_IMAGES", "0") == "1",
        infer_table_structure=os.getenv("KB_INFER_TABLE_STRUCTURE", "1") == "1",
        skip_infer_table_types=False,
        strategy=(os.getenv("KB_PDF_STRATEGY", "fast") or "fast").strip(),
        languages=[language],
        chunking_strategy="by_title",
        max_characters=int(os.getenv("KB_CHUNK_MAX_CHARACTERS", "2800")),
        new_after_n_chars=int(os.getenv("KB_CHUNK_NEW_AFTER_N_CHARS", "2400")),
        combine_text_under_n_chars=int(os.getenv("KB_CHUNK_COMBINE_UNDER_N_CHARS", "900")),
    )

    domain = _infer_domain_from_kb_root(kb_root, pdf, exclude_dirs)
    fallback_title = _title_from_filename(pdf)
    title = _title_from_elements(raw_pdf_elements, fallback=fallback_title)
    if not title.strip():
        title = fallback_title or "Untitled"

    doc_id = _sha256_file(pdf)

    chunks: List[KbChunk] = []
    chunk_idx = 0
    for el in raw_pdf_elements:
        text = getattr(el, "text", None)
        if not text or not str(text).strip():
            continue
        meta = getattr(el, "metadata", None)
        page_number = getattr(meta, "page_number", None) if meta else None
        if page_number is None:
            continue
        chunks.append(
            KbChunk(
                doc_id=doc_id,
                chunk_id=chunk_idx,
                page_number=int(page_number),
                text=str(text).strip(),
            )
        )
        chunk_idx += 1

    return domain, title, chunks


# -----------------------
# Core ops
# -----------------------
def ingest_one_pdf(
    store: KbMilvusStore,
    pdf_path: str,
    provider: Optional[str] = None,
    model: Optional[str] = None,
    language: Optional[str] = None,
    force_rebuild: bool = False,
    verbose: bool = True,
) -> dict:
    """
    Add/ingest a single PDF.

    GUARANTEE:
      - If cache exists for doc_id and force_rebuild=False:
          -> NO LLM calls.
    """
    cfg = store.cfg
    pdf = Path(pdf_path).resolve()
    if not pdf.exists():
        raise FileNotFoundError(str(pdf))

    cfg.meta_dir.mkdir(parents=True, exist_ok=True)

    doc_id = _sha256_file(pdf)
    cache_file = _meta_path(cfg.meta_dir, doc_id)
    cached = _read_json(cache_file) if cache_file.exists() else None

    # If embedding config changed since cached index -> must reindex (still NO LLM on cache hit)
    embed_mismatch = False
    if cached:
        if str(cached.get("embed_provider") or "") != str(cfg.embed_provider):
            embed_mismatch = True
        if str(cached.get("embed_model") or "") != str(cfg.embed_model):
            embed_mismatch = True
        if int(cached.get("embed_dim") or 0) not in (0, int(cfg.embed_dim)):
            embed_mismatch = True

    # Only these chunk/env parameters changing should trigger reindex
    chunk_mismatch = False
    if cached:
        now_pdf_strategy = (os.getenv("KB_PDF_STRATEGY", "fast") or "fast").strip()
        now_infer_table = os.getenv("KB_INFER_TABLE_STRUCTURE", "1") == "1"
        now_extract_images = os.getenv("KB_EXTRACT_IMAGES", "0") == "1"
        now_max = int(os.getenv("KB_CHUNK_MAX_CHARACTERS", "2800"))
        now_new = int(os.getenv("KB_CHUNK_NEW_AFTER_N_CHARS", "2400"))
        now_combine = int(os.getenv("KB_CHUNK_COMBINE_UNDER_N_CHARS", "900"))

        cached_pdf_strategy = (str(cached.get("pdf_strategy") or "")).strip()
        # if old cache has no these fields, treat as mismatch so one-time reindex upgrades cache format
        if cached_pdf_strategy == "":
            chunk_mismatch = True
        else:
            cached_infer_table = bool(cached.get("infer_table_structure"))
            cached_extract_images = bool(cached.get("extract_images"))
            try:
                cached_max = int(cached.get("chunk_max_characters"))
            except Exception:
                cached_max = None
            try:
                cached_new = int(cached.get("chunk_new_after_n_chars"))
            except Exception:
                cached_new = None
            try:
                cached_combine = int(cached.get("chunk_combine_under_n_chars"))
            except Exception:
                cached_combine = None

            if cached_pdf_strategy != now_pdf_strategy:
                chunk_mismatch = True
            elif cached_infer_table != now_infer_table:
                chunk_mismatch = True
            elif cached_extract_images != now_extract_images:
                chunk_mismatch = True
            elif cached_max != now_max:
                chunk_mismatch = True
            elif cached_new != now_new:
                chunk_mismatch = True
            elif cached_combine != now_combine:
                chunk_mismatch = True

    # Fast skip: already indexed + cache hit + no mismatch
    if (
        (not force_rebuild)
        and cached
        and (not embed_mismatch)
        and (not chunk_mismatch)
        and store.has_doc(doc_id)
    ):
        if verbose:
            print(f"[KB] skip (already indexed): doc_id={doc_id} pdf={pdf.name}")
        return {
            "ok": True,
            "skipped": True,
            "doc_id": doc_id,
            "reason": "already_indexed",
        }

    language = language or os.getenv("KB_LANGUAGE") or "eng"

    # -------------------------
    # CACHE HIT -> NO LLM
    # -------------------------
    if cached and (not force_rebuild):
        if verbose:
            msg = "cache hit (no LLM)"
            if embed_mismatch:
                msg += " + embedding config changed -> reindex"
            if chunk_mismatch:
                msg += " + chunk env changed -> reindex"
            print(f"[KB] {msg}: doc_id={doc_id}")

        domain, title, chunks = parse_pdf_chunks_no_llm(
            kb_root=cfg.kb_root,
            pdf=pdf,
            exclude_dirs=cfg.exclude_dirs,
            language=language,
        )

        # reuse cached summary (must exist)
        doc_summary = str(cached.get("doc_summary") or "").strip()
        if len(doc_summary) < 50:
            # keep system stable; still no LLM
            doc_summary = (
                "Cached summary is missing/too short. "
                "Please delete the cache file to force regeneration."
            )

        # keep original ingested_at if possible
        ingested_at = datetime.now().astimezone()
        try:
            if cached.get("ingested_at"):
                ingested_at = datetime.fromisoformat(str(cached["ingested_at"]))
        except Exception:
            pass

        doc_meta = KbDocMeta(
            doc_id=doc_id,
            domain=domain,
            title=title,
            doc_summary=doc_summary,
            ingested_at=ingested_at,
        )

    # -------------------------
    # CACHE MISS -> call kb_min (LLM summary)
    # -------------------------
    else:
        provider = (
            provider or os.getenv("KB_PROVIDER") or os.getenv("PROVIDER") or "scads"
        )
        model = (
            model
            or os.getenv("KB_MODEL")
            or os.getenv("CLASSIFY_HABIT_MODEL")
            or "meta-llama/Llama-3.3-70B-Instruct"
        )

        if verbose:
            print(f"[KB] ingest (cache miss -> LLM ok): {pdf}")

        doc_meta, chunks = build_kb_min_from_pdf(
            str(pdf),
            provider=provider,
            model=model,
            language=language,
            kb_root_name=os.getenv("KB_ROOT_NAME") or "kb",
        )

    if not chunks:
        # Still write cache (including env snapshot) for stability
        _write_json(
            cache_file,
            _docmeta_to_cache_dict(
                doc_meta,
                pdf,
                cfg.embed_provider,
                cfg.embed_model,
                cfg.embed_dim,
                chunk_count=0,
            ),
        )
        return {
            "ok": False,
            "doc_id": doc_id,
            "reason": "no_chunks",
            "pdf_strategy": (os.getenv("KB_PDF_STRATEGY", "fast") or "fast").strip(),
            "infer_table_structure": os.getenv("KB_INFER_TABLE_STRUCTURE", "1") == "1",
            "chunk_max_characters": int(os.getenv("KB_CHUNK_MAX_CHARACTERS", "2800")),
            "chunk_new_after_n_chars": int(os.getenv("KB_CHUNK_NEW_AFTER_N_CHARS", "2400")),
            "chunk_combine_under_n_chars": int(os.getenv("KB_CHUNK_COMBINE_UNDER_N_CHARS", "900")),
            "extract_images": os.getenv("KB_EXTRACT_IMAGES", "0") == "1",
        }

    # embed chunks -> vectors
    texts = [c.text for c in chunks]
    vectors: List[List[float]] = []
    bs = int(cfg.embed_batch_size)
    for i in range(0, len(texts), bs):
        batch = texts[i : i + bs]
        vectors.extend(
            embed_texts(
                batch,
                provider=cfg.embed_provider,
                model=cfg.embed_model,
                normalize=cfg.normalize_embeddings,
                bge_device=cfg.embed_device,
                bge_fp16=cfg.embed_fp16,
            )
        )

    n = store.upsert_chunks(
        doc_id=doc_meta.doc_id, domain=doc_meta.domain, chunks=chunks, vectors=vectors
    )

    # update cache (also refresh domain/title if moved) + persist env snapshot
    _write_json(
        cache_file,
        _docmeta_to_cache_dict(
            doc_meta,
            pdf,
            cfg.embed_provider,
            cfg.embed_model,
            cfg.embed_dim,
            chunk_count=n,
        ),
    )

    if verbose:
        print(
            f"[KB] indexed: doc_id={doc_id} chunks={n} domain={doc_meta.domain} title={doc_meta.title}"
        )

    return {
        "ok": True,
        "skipped": False,
        "doc_id": doc_id,
        "chunks": n,
        "domain": doc_meta.domain,
        "title": doc_meta.title,
    }


def delete_doc(
    store: KbMilvusStore,
    doc_id: str,
    remove_cache: bool = True,
    verbose: bool = True,
) -> dict:
    cfg = store.cfg
    store.delete_doc(doc_id)
    if remove_cache:
        p = _meta_path(cfg.meta_dir, doc_id)
        if p.exists():
            try:
                p.unlink()
            except Exception:
                pass
    if verbose:
        print(f"[KB] deleted: doc_id={doc_id} (milvus + cache={remove_cache})")
    return {"ok": True, "doc_id": doc_id}


def sync_kb(
    store: KbMilvusStore,
    force_rebuild: bool = False,
    verbose: bool = True,
) -> dict:
    cfg = store.cfg
    kb_root = cfg.kb_root
    meta_dir = cfg.meta_dir

    if force_rebuild:
        if verbose:
            print("[KB] force_rebuild=True -> drop & recreate collection")
        store.drop_collection()

    if not kb_root.exists():
        raise FileNotFoundError(f"KB root not found: {kb_root}")

    meta_dir.mkdir(parents=True, exist_ok=True)

    pdfs = _iter_pdfs(kb_root, cfg.exclude_dirs)
    if verbose:
        print(f"[KB] scan PDFs: {len(pdfs)} under {kb_root}")

    ingested = 0
    skipped = 0
    errors: List[str] = []
    alive_doc_ids: Set[str] = set()

    for pdf in pdfs:
        try:
            doc_id = _sha256_file(pdf)
            alive_doc_ids.add(doc_id)
            out = ingest_one_pdf(
                store, str(pdf), force_rebuild=force_rebuild, verbose=verbose
            )
            if out.get("skipped"):
                skipped += 1
            elif out.get("ok"):
                ingested += 1
        except Exception as e:
            errors.append(f"{pdf}: {repr(e)}")
            if verbose:
                print("[KB] ingest error:", pdf, repr(e))

    # delete stale docs based on the REAL doc_ids currently stored in Milvus,
    # not only on cache files in _meta. This prevents orphaned Milvus rows from
    # surviving forever after their cache json has been removed manually.
    stale = 0
    try:
        milvus_doc_ids = store.list_doc_ids()
    except Exception as e:
        milvus_doc_ids = set()
        errors.append(f"list_doc_ids: {repr(e)}")
        if verbose:
            print("[KB] list_doc_ids error:", repr(e))

    stale_doc_ids = sorted(doc_id for doc_id in milvus_doc_ids if doc_id not in alive_doc_ids)
    for doc_id in stale_doc_ids:
        try:
            delete_doc(store, doc_id, remove_cache=True, verbose=verbose)
            stale += 1
        except Exception as e:
            errors.append(f"delete {doc_id}: {repr(e)}")
            if verbose:
                print("[KB] delete error:", doc_id, repr(e))

    # optional hygiene: remove orphan cache files that no longer correspond to any
    # live pdf and are also not present in Milvus anymore.
    for cf in sorted(meta_dir.glob("*.json")):
        if cf.name == "_kb_state.json" or cf.stem.startswith("_"):
            continue
        doc_id = cf.stem
        if doc_id in alive_doc_ids or doc_id in milvus_doc_ids:
            continue
        try:
            cf.unlink()
            if verbose:
                print("[KB] removed orphan cache file:", cf.name)
        except Exception as e:
            errors.append(f"remove cache {doc_id}: {repr(e)}")
            if verbose:
                print("[KB] remove cache error:", doc_id, repr(e))

    return {
        "ok": len(errors) == 0,
        "kb_root": str(kb_root),
        "collection": cfg.collection_name,
        "pdfs_found": len(pdfs),
        "ingested": ingested,
        "skipped": skipped,
        "stale_deleted": stale,
        "errors": errors[:20],
    }


def search(
    store: KbMilvusStore,
    query: str,
    top_k: int = 5,
    domain: Optional[str] = None,
    include_doc_meta: bool = True,
) -> List[dict]:
    qv = embed_query(
        query,
        provider=store.cfg.embed_provider,
        model=store.cfg.embed_model,
        normalize=store.cfg.normalize_embeddings,
        bge_device=store.cfg.embed_device,
        bge_fp16=store.cfg.embed_fp16,
    )
    hits = store.search(qv, top_k=top_k, domain=domain)

    if not include_doc_meta:
        return hits

    out: List[dict] = []
    for h in hits:
        doc_id = str(h.get("doc_id") or "")
        meta = load_cached_doc_meta(store.cfg.meta_dir, doc_id) if doc_id else None
        if meta:
            h["doc_title"] = meta.get("title")
            h["doc_summary"] = meta.get("doc_summary")
        out.append(h)
    return out


# -----------------------
# CLI
# -----------------------
def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--sync", action="store_true", help="Sync kb -> Milvus")
    p.add_argument(
        "--force",
        action="store_true",
        help="Force rebuild (drop collection and re-ingest)",
    )
    p.add_argument("--kb", default=None, help="KB root dir")
    p.add_argument("--milvus", default=None, help="Milvus URI")
    p.add_argument("--collection", default=None, help="Milvus collection name")
    p.add_argument("--pdf", default=None, help="Ingest one PDF")
    p.add_argument("--delete", default=None, help="Delete one doc_id")
    p.add_argument("--q", default=None, help="Search query")
    p.add_argument("--domain", default=None, help="Domain filter")
    p.add_argument("--k", type=int, default=5, help="Top-k")
    p.add_argument("--quiet", action="store_true", help="Less logs")
    args = p.parse_args()

    cfg = load_config(
        kb_root=args.kb, milvus_uri=args.milvus, collection_name=args.collection
    )
    store = KbMilvusStore(cfg)
    verbose = not args.quiet

    if args.pdf:
        out = ingest_one_pdf(store, args.pdf, force_rebuild=args.force, verbose=verbose)
        print(_json_dump(out))
        return

    if args.delete:
        out = delete_doc(store, args.delete, remove_cache=True, verbose=verbose)
        print(_json_dump(out))
        return

    if args.sync:
        out = sync_kb(store, force_rebuild=args.force, verbose=verbose)
        print(_json_dump(out))
        return

    if args.q:
        out = search(
            store, args.q, top_k=args.k, domain=args.domain, include_doc_meta=True
        )
        print(_json_dump(out))
        return

    p.print_help()


if __name__ == "__main__":
    main()
