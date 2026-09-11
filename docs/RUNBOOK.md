
 DocuFlow v2 – Operational Runbook

 Purpose
Operational guidance for running, maintaining, and troubleshooting DocuFlow v2.

 Service Startup (local)
Run from inside `ml-api-service/` (the FastAPI app and its Python packages
live there, not at the repo root):

cd ml-api-service
pip install -r ../requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8001

 Service Startup (Docker)
From the repository root:

docker build -t docuflow-v2 .
docker run -p 8001:8001 docuflow-v2

or:

docker compose up --build

Verified: `docker build` and `docker run` were tested locally on
2026-09-11 — the container starts, `/`, `/faiss/add`, and `/route-from-search`
respond correctly, and audit records are written to
`/app/audit_logs/workflow_audit.jsonl` inside the container. This has not
been tested beyond a single local container (no orchestration, scaling, or
production hardening).

 Health Check
GET /

 Common Operations
- POST /ingest-file
- POST /hybrid-search
- POST /route-from-search

 Running Tests
From the repository root:

pip install -r ml-api-service/tests/requirements-test.txt
pytest ml-api-service/tests

These are unit tests against already-implemented behaviour (routing,
permission checks, simulated execution). They deliberately only exercise
code paths that don't import the embedding model or FAISS
(`workflow/router.py`, `security/guard.py`, `security/roles.py`,
`workflow/executor.py`, `audit/logger.py`), so running them needs only
`pytest` + `PyYAML` — no model download, no FAISS build, no network access.
The heavier search/ingestion code paths (`nlp/embedder.py`,
`vector_db/faiss_store.py`, `hybrid_search.py`) are exercised manually via
the API, not by this automated suite.

The root `pytest.ini` scopes default test discovery to `ml-api-service/tests`
so a bare `pytest` run from the repo root does not also try to collect the
unrelated manual scripts under `legacy_prototype/` (which are named
`test_*.py` but are not an automated test suite — see
`legacy_prototype/README.md`).

 Audit Verification
Audit logs stored in audit_logs/workflow_audit.jsonl (append-only).

 Common Failure Scenarios
- Permission denied
- No routing rule matched
- Empty search results

 FAISS Maintenance
Stop service, back up data directory, rebuild index if required.

 Log Rotation
Use OS-level rotation. Never modify existing logs.

 Security
No secrets in code. There is no authentication in this repository: the role
used for every request is a single statically configured value
(`DOCUFLOW_DEFAULT_ROLE`), not a per-user authenticated identity. Capability
checks are real and enforced against that configured role, but they do not
distinguish between callers. Do not treat this service as access-controlled
for multiple real users.

 Incident Response
Identify audit record, review rule, apply fix, re-run if needed.

 Decommissioning
Stop service, archive audit logs, back up FAISS data.

 Final Note
System fails safely by design.
