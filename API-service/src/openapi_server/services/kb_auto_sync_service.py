# src/openapi_server/services/kb_auto_sync_service.py
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional

# ---- import kb_milvus_service (module-friendly) ----
try:
    from .kb_milvus_service import load_config, KbMilvusStore, sync_kb
except ImportError:
    SRC_DIR = Path(__file__).resolve().parents[2]  # .../src
    sys.path.insert(0, str(SRC_DIR))
    from openapi_server.services.kb_milvus_service import load_config, KbMilvusStore, sync_kb  # type: ignore


def _is_pdf(path: str) -> bool:
    return path.lower().endswith(".pdf")


def run_watch(
    kb_root: Optional[str] = None,
    milvus_uri: Optional[str] = None,
    collection_name: Optional[str] = None,
    debounce_seconds: float = 2.5,
    initial_sync: bool = True,
    verbose: bool = True,
) -> None:
    """
    Watch kb folder; on any pdf file event, debounce then call sync_kb() once.
    """
    # lazy import to keep dependency local
    from watchdog.observers import Observer  # type: ignore
    from watchdog.events import FileSystemEventHandler  # type: ignore

    cfg = load_config(kb_root=kb_root, milvus_uri=milvus_uri, collection_name=collection_name)
    store = KbMilvusStore(cfg)

    if initial_sync:
        if verbose:
            print("[KB-WATCH] initial sync ...")
        out = sync_kb(store, force_rebuild=False, verbose=verbose)
        if verbose:
            print("[KB-WATCH] initial sync done:", out)

    kb = cfg.kb_root
    if not kb.exists():
        raise FileNotFoundError(f"KB root not found: {kb}")

    # Debounce state
    last_event_ts = 0.0
    pending = False

    def mark_event(src_path: str) -> None:
        nonlocal last_event_ts, pending
        if not _is_pdf(src_path):
            return
        pending = True
        last_event_ts = time.time()
        if verbose:
            print(f"[KB-WATCH] event: {src_path}")

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if not event.is_directory:
                mark_event(event.src_path)

        def on_modified(self, event):
            if not event.is_directory:
                mark_event(event.src_path)

        def on_deleted(self, event):
            if not event.is_directory:
                mark_event(event.src_path)

        def on_moved(self, event):
            if not event.is_directory:
                # moved has src_path + dest_path
                mark_event(getattr(event, "src_path", ""))
                mark_event(getattr(event, "dest_path", ""))

    observer = Observer()
    observer.schedule(Handler(), str(kb), recursive=True)
    observer.start()

    if verbose:
        print(f"[KB-WATCH] watching: {kb}")
        print(f"[KB-WATCH] debounce_seconds={debounce_seconds}")

    try:
        while True:
            time.sleep(0.25)
            if not pending:
                continue

            # if no new event for debounce window -> run sync once
            if (time.time() - last_event_ts) >= debounce_seconds:
                pending = False
                if verbose:
                    print("[KB-WATCH] debounce window passed -> sync_kb()")
                try:
                    out = sync_kb(store, force_rebuild=False, verbose=verbose)
                    if verbose:
                        print("[KB-WATCH] sync result:", out)
                except Exception as e:
                    # don’t crash the watcher
                    print("[KB-WATCH] sync error:", repr(e))

    except KeyboardInterrupt:
        if verbose:
            print("[KB-WATCH] stopping ...")
    finally:
        observer.stop()
        observer.join()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--kb", default=None, help="KB root dir (default: openapi_server/kb or env KB_ROOT_DIR)")
    p.add_argument("--milvus", default=None, help="Milvus URI (default: env MILVUS_URI or http://localhost:19530)")
    p.add_argument("--collection", default=None, help="Milvus collection name (default: env KB_MILVUS_COLLECTION)")
    p.add_argument("--debounce", type=float, default=2.5, help="Debounce seconds before syncing")
    p.add_argument("--no-initial-sync", action="store_true", help="Skip initial sync at startup")
    p.add_argument("--quiet", action="store_true", help="Less logs")
    args = p.parse_args()

    run_watch(
        kb_root=args.kb,
        milvus_uri=args.milvus,
        collection_name=args.collection,
        debounce_seconds=args.debounce,
        initial_sync=not args.no_initial_sync,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
