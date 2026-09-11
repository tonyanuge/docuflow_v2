Legacy Prototype (Historical Reference Only)

Status
This directory is **not** part of the current DocuFlow v2 architecture described in
the top-level `README.md` and `docs/`. It is retained to show an earlier stage of
this project's evolution and is kept for historical reference only.

What this was
Before the governed FastAPI service in `ml-api-service/` existed, this project
started as a much simpler set of standalone scripts:

* `services/ml_client.py`, `services/search_client.py` — thin HTTP clients that
  called an early, minimal API exposing `/classify` and `/embed` only (no hybrid
  search, no routing, no permissions, no audit trail).
* `ingestion/` — an early multi-format text-extraction module (PDF via PyMuPDF,
  DOCX, `.eml`, and Tesseract-based OCR) that predates and was superseded by the
  simpler `ml-api-service/ingest_file/` package used by the current API.
* `vector_db/vector_store.py` — an early experiment storing embeddings in SQLite
  using the `sqlite-vec` extension, before the project moved to the FAISS-based
  store now used in `ml-api-service/vector_db/faiss_store.py`.
* `test_*.py` — manual smoke scripts (no assertions, not a test suite) written
  against the scripts above.

Why it's kept
It documents real project evolution: simple client/script prototype →
multi-format ingestion experiments → the governed, YAML-routed, audited FastAPI
service that is the actual subject of this repository. Deleting it would erase
that history for no accuracy benefit.

Known limitations (not fixed, by design)
* These scripts are not exercised by any test suite or CI and are not guaranteed
  to run as-is (for example, `test_vector_store.py` imports a top-level `nlp`
  package that does not exist in this repository — it only exists inside
  `ml-api-service/`).
* `vector_store.py` requires the native `sqlite-vec` extension binary for your
  platform. That binary is intentionally **not** committed here (see below) —
  it previously shipped as a Windows-only `vec0.dll` of unverified provenance,
  which is not something a portfolio repository should carry as a tracked
  binary. To actually run this script, obtain `sqlite-vec` for your own platform.
* `ingestion/ocr.py` hardcodes a Windows path to a local Tesseract install.

None of this legacy code is imported by, or required by, `ml-api-service/`.
The current, documented system is entirely self-contained under `ml-api-service/`.
