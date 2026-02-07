from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple, Union

from owlready2 import get_ontology, ThingClass  # type: ignore


# =========================
# Constants
# =========================
ANN: Dict[str, str] = {
    "rdfs_label":      "http://www.w3.org/2000/01/rdf-schema#label",
    "rdfs_comment":    "http://www.w3.org/2000/01/rdf-schema#comment",
    "iao_pref_label":  "http://purl.obolibrary.org/obo/IAO_0000111",  # editor preferred label
    "iao_definition":  "http://purl.obolibrary.org/obo/IAO_0000115",  # definition
    "iao_example":     "http://purl.obolibrary.org/obo/IAO_0000112",  # example of usage
    "exact_syn":       "http://www.geneontology.org/formats/oboInOwl#hasExactSynonym",
    "related_syn":     "http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym",
    "broad_syn":       "http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym",
    "narrow_syn":      "http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym",
}

BCIO_CLASS_PREFIX = "http://humanbehaviourchange.org/ontology/BCIO_"
BCIO_REL_PREFIX   = "http://humanbehaviourchange.org/ontology/BCIOR_"


@dataclass
class ExportStats:
    out_path: Path
    mode: str
    total_classes: int
    total_object_properties: int
    total_data_properties: int
    total_annotation_properties: int
    exported_classes: int
    exported_object_properties: int
    exported_data_properties: int
    exported_annotation_properties: int
    lines_written: int


# =========================
# Public API
# =========================
def export_concept_cards(
    owl_path: Union[str, Path],
    out_path: Optional[Union[str, Path]] = None,
    mode: str = "ALL_MERGED",  # "BCIO_ONLY" or "ALL_MERGED"
    preferred_langs: Tuple[Optional[str], ...] = ("en", None),
    export_annotation_properties: bool = False,
    verbose: bool = True,
) -> ExportStats:
    """
    Export OWL ontology into JSONL concept cards for RAG.

    Parameters
    ----------
    owl_path:
        Path to the OWL file.
    out_path:
        Output JSONL path. If None, defaults to concepts_{mode.lower()}.jsonl next to owl.
    mode:
        "ALL_MERGED" exports everything; "BCIO_ONLY" exports BCIO + BCIO_REL only.
    preferred_langs:
        Language preference order for annotations (e.g., ("en", None)).
    export_annotation_properties:
        Whether to export AnnotationProperty entities (usually False).
    verbose:
        Print progress.

    Returns
    -------
    ExportStats
    """
    owl_path = Path(owl_path).resolve()
    if not owl_path.exists():
        raise FileNotFoundError(f"OWL file not found: {owl_path}")

    mode = (mode or "ALL_MERGED").strip().upper()
    if mode not in ("ALL_MERGED", "BCIO_ONLY"):
        raise ValueError("mode must be 'ALL_MERGED' or 'BCIO_ONLY'")

    if out_path is None:
        # By default, it is written to the same directory as owl: concepts_{mode}.jsonl
        out_path = owl_path.parent / f"concepts_{mode.lower()}.jsonl"
    out_path = Path(out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # =========================
    # LOAD OWL
    # =========================
    if verbose:
        print("Loading OWL from:", owl_path)
    onto = get_ontology(str(owl_path)).load()
    world = onto.world

    if verbose:
        print("Loaded ontology base IRI:", onto.base_iri)
        print("Writing to:", out_path)
        print("MODE:", mode)

    # =========================
    # Helpers (Closure binding world / preferred_langs / mode)
    # =========================
    def iri_source(iri: str) -> str:
        if iri.startswith(BCIO_CLASS_PREFIX):
            return "BCIO"
        if iri.startswith(BCIO_REL_PREFIX):
            return "BCIO_REL"
        if iri.startswith("http://purl.obolibrary.org/obo/"):
            return "OBO_EXTERNAL"
        return "OTHER"

    def should_export(iri: str) -> bool:
        if mode == "ALL_MERGED":
            return True
        return iri.startswith((BCIO_CLASS_PREFIX, BCIO_REL_PREFIX))

    def _normalize_list(values):
        if values is None:
            return []
        if isinstance(values, (list, tuple)):
            return list(values)
        return [values]

    def _to_str_and_lang(v):
        lang = getattr(v, "lang", None)
        return str(v), lang

    def get_ann_values(entity, prop_iri: str) -> List[str]:
        """Read annotation values by annotation-property IRI; order by language preference."""
        prop = world[prop_iri]
        if prop is None:
            return []

        raw = _normalize_list(prop[entity])
        pairs = [_to_str_and_lang(v) for v in raw if v is not None]

        ordered: List[str] = []
        for lang in preferred_langs:
            ordered.extend([t for (t, l) in pairs if l == lang])
        ordered.extend([t for (t, l) in pairs if l not in preferred_langs])

        # dedupe, keep order
        seen, out = set(), []
        for t in ordered:
            if t not in seen:
                seen.add(t)
                out.append(t)
        return out

    def class_parents(cls) -> List[str]:
        """Only take superclass IRIs; ignore restrictions."""
        parents: List[str] = []
        for p in cls.is_a:
            if isinstance(p, ThingClass):
                parents.append(p.iri)
        return parents

    def build_class_card(cls) -> Dict:
        labels      = get_ann_values(cls, ANN["rdfs_label"])
        pref_labels = get_ann_values(cls, ANN["iao_pref_label"])
        definitions = get_ann_values(cls, ANN["iao_definition"])
        comments    = get_ann_values(cls, ANN["rdfs_comment"])

        synonyms: List[str] = []
        for k in ("exact_syn", "related_syn", "broad_syn", "narrow_syn"):
            synonyms.extend(get_ann_values(cls, ANN[k]))
        # dedupe synonyms
        seen, syn_out = set(), []
        for s in synonyms:
            if s not in seen:
                seen.add(s)
                syn_out.append(s)

        card = {
            "type": "Class",
            "source": iri_source(cls.iri),
            "iri": cls.iri,
            "name": cls.name,
            "labels": labels,
            "preferred_labels": pref_labels,
            "definition": definitions,
            "comment": comments,
            "synonyms": syn_out,
            "parents": class_parents(cls),
            "equivalent_to": [c.iri if hasattr(c, "iri") else str(c) for c in cls.equivalent_to],
        }

        # Text for embedding / RAG context
        text_parts: List[str] = []
        if pref_labels:
            text_parts.append("Preferred label: " + "; ".join(pref_labels))
        if labels:
            text_parts.append("Label: " + "; ".join(labels))
        if syn_out:
            text_parts.append("Synonyms: " + "; ".join(syn_out))
        if definitions:
            text_parts.append("Definition: " + " | ".join(definitions))
        if comments:
            text_parts.append("Comment: " + " | ".join(comments))
        card["text"] = "\n".join(text_parts)

        return card

    def build_property_card(prop, prop_type: str) -> Dict:
        labels      = get_ann_values(prop, ANN["rdfs_label"])
        pref_labels = get_ann_values(prop, ANN["iao_pref_label"])
        definitions = get_ann_values(prop, ANN["iao_definition"])
        comments    = get_ann_values(prop, ANN["rdfs_comment"])

        card = {
            "type": prop_type,  # ObjectProperty / DataProperty / AnnotationProperty
            "source": iri_source(prop.iri),
            "iri": prop.iri,
            "name": prop.name,
            "labels": labels,
            "preferred_labels": pref_labels,
            "definition": definitions,
            "comment": comments,
            "domain": [d.iri for d in getattr(prop, "domain", []) if hasattr(d, "iri")],
            "range":  [r.iri for r in getattr(prop, "range",  []) if hasattr(r, "iri")],
        }

        text_parts: List[str] = []
        if pref_labels:
            text_parts.append("Preferred label: " + "; ".join(pref_labels))
        if labels:
            text_parts.append("Label: " + "; ".join(labels))
        if definitions:
            text_parts.append("Definition: " + " | ".join(definitions))
        if comments:
            text_parts.append("Comment: " + " | ".join(comments))
        if card["domain"]:
            text_parts.append("Domain: " + "; ".join(card["domain"]))
        if card["range"]:
            text_parts.append("Range: " + "; ".join(card["range"]))
        card["text"] = "\n".join(text_parts)

        return card

    # =========================
    # Collect entities
    # =========================
    classes     = list(onto.classes())
    obj_props   = list(onto.object_properties())
    data_props  = list(onto.data_properties())
    ann_props   = list(onto.annotation_properties()) if export_annotation_properties else []

    # filter
    filtered_classes = [c for c in classes if should_export(c.iri)]
    filtered_obj     = [p for p in obj_props if should_export(p.iri)]
    filtered_data    = [p for p in data_props if should_export(p.iri)]
    filtered_ann     = [p for p in ann_props  if should_export(p.iri)] if export_annotation_properties else []

    if verbose:
        print("Total classes:", len(classes))
        print("Total object properties:", len(obj_props))
        print("Total data properties:", len(data_props))
        if export_annotation_properties:
            print("Total annotation properties:", len(ann_props))

        print("Exported classes:", len(filtered_classes))
        print("Exported object properties:", len(filtered_obj))
        print("Exported data properties:", len(filtered_data))
        if export_annotation_properties:
            print("Exported annotation properties:", len(filtered_ann))

    # =========================
    # Write JSONL
    # =========================
    written = 0
    with open(out_path, "w", encoding="utf-8") as f:
        for cls in filtered_classes:
            f.write(json.dumps(build_class_card(cls), ensure_ascii=False) + "\n")
            written += 1

        for p in filtered_obj:
            f.write(json.dumps(build_property_card(p, "ObjectProperty"), ensure_ascii=False) + "\n")
            written += 1

        for p in filtered_data:
            f.write(json.dumps(build_property_card(p, "DataProperty"), ensure_ascii=False) + "\n")
            written += 1

        if export_annotation_properties:
            for p in filtered_ann:
                f.write(json.dumps(build_property_card(p, "AnnotationProperty"), ensure_ascii=False) + "\n")
                written += 1

    if verbose:
        print(f"Done -> {out_path} (lines written: {written})")

    return ExportStats(
        out_path=out_path,
        mode=mode,
        total_classes=len(classes),
        total_object_properties=len(obj_props),
        total_data_properties=len(data_props),
        total_annotation_properties=len(ann_props),
        exported_classes=len(filtered_classes),
        exported_object_properties=len(filtered_obj),
        exported_data_properties=len(filtered_data),
        exported_annotation_properties=len(filtered_ann),
        lines_written=written,
    )


# =========================
# keep script runnable
# =========================
if __name__ == "__main__":
    MODE = os.getenv("EXTRACTION_MODEL", "ALL_MERGED")

    SCRIPT_DIR = Path(__file__).resolve().parent
    OWL_PATH = SCRIPT_DIR.parent / "Ontologies" / "bcio.owl"
    OUT_PATH = SCRIPT_DIR / f"concepts_{MODE.lower()}.jsonl"

    export_concept_cards(
        owl_path=OWL_PATH,
        out_path=OUT_PATH,
        mode=MODE,
        preferred_langs=("en", None),
        export_annotation_properties=False,
        verbose=True,
    )
