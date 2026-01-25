# Achieve PDF processing for a minimal knowledge base: generate DocMeta and Chunks (domain dynamically derived from subdirectories under kb/).
# src/openapi_server/services/kb_min.py
from __future__ import annotations

import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Set

from pydantic import BaseModel, Field, constr
from unstructured.partition.pdf import partition_pdf


# -------- paths that do NOT depend on cwd --------
OPENAPI_SERVER_DIR = Path(__file__).resolve().parents[1]          # .../src/openapi_server
DEFAULT_KB_ROOT = OPENAPI_SERVER_DIR / "kb"                      # .../src/openapi_server/kb


try:
    from .llm_habit_service import classify_habit_via_llm_prompt
except ImportError:
    import sys
    SRC_DIR = Path(__file__).resolve().parents[2]                # .../src
    sys.path.insert(0, str(SRC_DIR))
    from openapi_server.services.llm_habit_service import classify_habit_via_llm_prompt


# -----------------------
# Models (Doc-level & Chunk-level)
# -----------------------
class KbDocMeta(BaseModel):
    doc_id: constr(min_length=16)
    domain: constr(min_length=1)
    title: constr(min_length=1)
    doc_summary: constr(min_length=50)
    ingested_at: datetime


class KbChunk(BaseModel):
    doc_id: constr(min_length=16)
    chunk_id: int = Field(ge=0)
    page_number: int = Field(ge=1)
    text: constr(min_length=1)


# -----------------------
# Helpers (env / casting)
# -----------------------
def _as_int(x, default: int) -> int:
    try:
        if x is None:
            return default
        return int(x)
    except Exception:
        return default


def _as_float(x, default: float) -> float:
    try:
        if x is None:
            return default
        return float(x)
    except Exception:
        return default


# -----------------------
# Helpers (kb path + domains)
# -----------------------
def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _kb_root_from_pdf_path(pdf_path: Path, kb_root_name: str = "kb") -> Path:
    """
    Priority:
    1) KB_ROOT_DIR env (most explicit)
    2) Default openapi_server/kb (does not depend on cwd, adapts to your project structure)
    3) Search for the kb root directory in pdf_path (.../kb/...)
    """
    kb_root_dir = os.getenv("KB_ROOT_DIR")
    if kb_root_dir:
        return Path(kb_root_dir).resolve()

    if DEFAULT_KB_ROOT.exists():
        return DEFAULT_KB_ROOT.resolve()

    # fallback: Find the KB file in the passed-in pdf_path
    parts = list(pdf_path.parts)
    lower = [p.lower() for p in parts]
    if kb_root_name.lower() not in lower:
        raise ValueError(f"Path does not contain '{kb_root_name}/': {pdf_path}")
    kb_idx = lower.index(kb_root_name.lower())
    return Path(*parts[: kb_idx + 1]).resolve()


def _discover_domain_folders(kb_root: Path) -> Set[str]:
    exclude = set(
        x.strip().lower()
        for x in os.getenv("EXCLUDE_DOMAIN_FOLDERS", "_shared,__pycache__,figs").split(",")
        if x.strip()
    )

    domains: Set[str] = set()
    if not kb_root.exists():
        return domains

    for p in kb_root.iterdir():
        if not p.is_dir():
            continue
        name = (p.name or "").strip()
        if not name:
            continue
        if name.startswith(".") or name.startswith("_"):
            continue
        if name.lower() in exclude:
            continue
        domains.add(name.lower())

    return domains


def _infer_domain_from_kb_folder(pdf_path: Path, kb_root_name: str = "kb") -> str:
    kb_root = _kb_root_from_pdf_path(pdf_path, kb_root_name=kb_root_name)
    allowed = _discover_domain_folders(kb_root)
    if not allowed:
        raise ValueError(f"No domain folders found under kb root: {kb_root}")

    rel = pdf_path.resolve().relative_to(kb_root)
    if len(rel.parts) < 2:
        raise ValueError(f"Expected kb_root/<domain>/... structure, got: {pdf_path}")

    domain = rel.parts[0].lower()
    if domain not in allowed:
        raise ValueError(f"Unknown domain '{domain}'. Allowed domains under {kb_root}: {sorted(allowed)}")

    return domain


# -----------------------
# Helpers (title + summary input)
# -----------------------
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


def _build_summary_input(elements, max_chars: int = 12000) -> str:
    texts: List[str] = []
    total = 0
    for el in elements:
        t = (getattr(el, "text", None) or str(el) or "").strip()
        if not t:
            continue

        remain = max_chars - total
        if remain <= 0:
            break

        take = t[:remain]
        if take:
            texts.append(take)
            total += len(take)

        if total >= max_chars:
            break

    return "\n\n".join(texts)


# -----------------------
# LLM summary
# -----------------------
def _llm_doc_summary(
    content: str,
    provider: str = "openai",
    model: str = "gpt-4.1",
    temperature: float = 0.0,
    max_tokens: int = 350,
) -> str:
    prompt = (
        "Summarize the document for a knowledge base.\n"
        "Focus on recommendations / behaviour-change measures.\n"
        "Return 6-10 concise bullet points. Plain text only.\n"
        "Do NOT include citations or links.\n"
    )

    raw = classify_habit_via_llm_prompt(
        prompt=prompt,
        sentence=content,
        provider=provider,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    summary = (raw or "").strip()
    if len(summary) < 50:
        summary = (
            "Summary generation returned empty output. "
            "Please retry with a different model/provider or check configuration."
        )
    return summary


def _dump_compat(m: BaseModel) -> dict:
    return m.model_dump() if hasattr(m, "model_dump") else m.dict()


# -----------------------
# Main: PDF -> (DocMeta, Chunks)
# -----------------------
def build_kb_min_from_pdf(
    pdf_path: str,
    provider: str = "openai",
    model: str = "gpt-4.1",
    language: str = "eng",
    kb_root_name: str = "kb",
) -> Tuple[KbDocMeta, List[KbChunk]]:
    pdf = Path(pdf_path).resolve()
    if not pdf.exists():
        raise FileNotFoundError(str(pdf))

    doc_id = _sha256_file(pdf)
    ingested_at = datetime.now().astimezone()

    domain = _infer_domain_from_kb_folder(pdf, kb_root_name=kb_root_name)
    extract_images = os.getenv("KB_EXTRACT_IMAGES", "0") == "1"

    raw_pdf_elements = partition_pdf(
        filename=str(pdf),
        extract_images_in_pdf=extract_images,
        infer_table_structure=os.getenv("KB_INFER_TABLE_STRUCTURE", "1") == "1",
        skip_infer_table_types=False,
        strategy=os.getenv("KB_PDF_STRATEGY", "fast"),
        languages=[language],
        chunking_strategy="by_title",
        max_characters=os.getenv("KB_CHUNK_MAX_CHARACTERS", "2800"),
        new_after_n_chars=os.getenv("KB_CHUNK_NEW_AFTER_N_CHARS", "2400"),
        combine_text_under_n_chars=os.getenv("KB_CHUNK_COMBINE_UNDER_N_CHARS", "900"),
        # image_output_dir_path=str(pdf.parent / "figs"),
    )

    fallback_title = _title_from_filename(pdf)
    title = _title_from_elements(raw_pdf_elements, fallback=fallback_title)
    if not title.strip():
        title = fallback_title or "Untitled"

    summary_max_chars = _as_int(os.getenv("KB_SUMMARY_MAX_CHARS"), 12000)
    summary_input = _build_summary_input(raw_pdf_elements, max_chars=summary_max_chars)
    if not summary_input.strip():
        summary_input = f"Title: {title}"

    temperature = _as_float(os.getenv("KB_TEMPERATURE"), 0.0)
    max_tokens = _as_int(os.getenv("KB_MAX_TOKENS"), 350)

    doc_summary = _llm_doc_summary(
        content=summary_input,
        provider=provider,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    doc_meta = KbDocMeta(
        doc_id=doc_id,
        domain=domain,
        title=title,
        doc_summary=doc_summary,
        ingested_at=ingested_at,
    )

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

    return doc_meta, chunks


# -----------------------
# Quick test
# -----------------------
if __name__ == "__main__":
    provider = os.getenv("KB_PROVIDER") or (os.getenv("PROVIDER") or "scads")
    model = os.getenv("KB_MODEL") or os.getenv("CLASSIFY_HABIT_MODEL") or "meta-llama/Llama-3.3-70B-Instruct"

    default_pdf_rel = Path("openapi_server") / "kb" / "sleep" / "NIH2005SOSPaperonInsomnia.pdf"
    default_pdf_abs = DEFAULT_KB_ROOT / "sleep" / "NIH2005SOSPaperonInsomnia.pdf"

    kb_pdf = os.getenv("KB_PDF") or (str(default_pdf_rel) if default_pdf_rel.exists() else str(default_pdf_abs))

    meta, chunks = build_kb_min_from_pdf(
        kb_pdf,
        provider=provider,
        model=model,
        language=os.getenv("KB_LANGUAGE", "eng"),
        kb_root_name=os.getenv("KB_ROOT_NAME", "kb"),
    )

    print("DOC META:", _dump_compat(meta))
    print("CHUNK[0]:", _dump_compat(chunks[0]) if chunks else None)
    print("CHUNKS:", len(chunks))
