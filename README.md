DocuFlow v2 – Governed AI Workflow Routing Prototype

DocuFlow v2 is an industry-agnostic prototype demonstrating a governed AI
workflow-routing pattern. It combines:
* Hybrid semantic + keyword search
* Rule-based workflow routing
* Capability-based permission checks
* Append-only audit logging

It is a working demonstration of explainable, controllable AI-assisted
decision routing — not a certified, production-hardened, or regulator-approved
system. See "What This Is (and Is Not)" and "Project Lineage" below.

What Problem This Solves
Most document and AI automation systems fail in three areas:
1. Search without context (keyword only or opaque embeddings)
2. Automation without control (no governance or overrides)
3. No audit trail (unsuitable for regulated environments)

DocuFlow v2 solves all three by design.

High-Level Architecture
Client (API / UI)
        |
        v
FastAPI Application
        |
        + Hybrid Search Engine
        |     - FAISS (vector recall)
        |     - Keyword reranking
        |
        + Classification Layer
        |
        + Workflow Router (YAML rules)
        |
        + Permission Guard (RBAC)
        |
        + Workflow Executor
        |
        + Audit Logger (JSONL, append-only)

Core Components
1. Hybrid Search Engine

* FAISS for semantic recall
* Keyword overlap for deterministic reranking
* Chunk-level indexing, document-level results
* No external vector DB dependency

Why it matters:
Search is explainable, fast, and fully self-hosted.

2. Workflow Routing (YAML-Driven)

Routing decisions are defined in rules.yaml, not code.

Example (matches the actual `rules.yaml` shipped in this repo):

routes:
  - when:
      classification: payment_request
    route:
      queue: finance_ops
      priority: high
default_route:
  queue: general_review
  priority: normal


Why it matters:
Non-developers can change behaviour safely.
No redeploy required.

3. Governance & Permissions

Role-based access control using explicit capabilities:

Roles:
* viewer
* operator
* manager
* admin

Capabilities:
* execute_workflow
* override_route
* view_audit_logs
* manage_rules

Why it matters:
Workflow execution is gated behind an explicit capability check rather than
happening unconditionally.

Important limitation: there is no authentication in this repository. Every
request is evaluated under a single statically configured role
(`DOCUFLOW_DEFAULT_ROLE`, default `operator`) rather than a per-user
authenticated identity. The capability check itself is real and enforced —
what's missing is a way to tell *which* role a given caller actually is.

4. Error Boundaries & Guardrails

Handled failure cases (each one is caught and audited rather than causing a
silent success):

* Permission denied
* No search results
* No routing rule matched

These failures do not crash the request silently — they are logged to the
audit trail with a reason. The API does not yet translate them into a custom
structured error body; an unhandled failure currently falls through to
FastAPI's default error response (no stack trace is exposed in production
mode, but the response is generic, not a documented error schema).

5. Audit & Lineage

Every routing attempt is logged:

Audit events:

* ROUTE_DECISION
* ROUTE_EXECUTED
* ROUTE_DENIED
* ROUTE_FAILED

Each audit record includes:
* Role
* Query
* Classification
* Decision
* Execution outcome
* Timestamp (UTC)

Stored as append-only JSONL (append-only by convention of how the app writes
to it — the file itself has no tamper-evidence, integrity hashing, or access
control, so it is not a compliance-grade audit store as-is).

Why it matters:
Every governed decision is traceable after the fact, which is the right
foundation for audit/compliance use — but real regulatory or audit-grade
guarantees would need additional controls (log integrity, retention policy,
access control) that this prototype does not implement.

API Highlights
Ingest Documents
POST /ingest-file

Hybrid Search
POST /hybrid-search

Governed Routing
POST /route-from-search


End-to-end flow:

1. Permission check
2. Hybrid search
3. Classification
4. YAML routing
5. Execution
6. Audit logging

Configuration & Deployment

The following are externalised via environment variables rather than
hardcoded: default role, FAISS data paths, audit log location, environment
mode (see `ml-api-service/app/config/settings.py`).

This enables:
* Local dev
* Containerised deployment via the included `Dockerfile` / `docker-compose.yml`
  (build and startup verified locally — see `docs/RUNBOOK.md`)

On-prem/production deployment beyond a single container has not been
attempted or verified.

What This Is (and Is Not)
This is:

* An early-stage prototype of a governance-first AI workflow-routing pattern
* A working demonstration of hybrid search, YAML-driven routing, capability
  checks, and audit logging, wired together end-to-end
* Explainable by design: every routing decision is traceable to a rule and an
  audit record

This is not:

* A production-grade, hardened, or regulator-certified system
* A system with authentication or per-user identity
* A black-box AI system
* A UI-heavy product
* A hard-coded finance-only tool

See "Project Lineage" below for how this repository relates to later work on
the same concept.

Project Status

✔ Hybrid search implemented (FAISS + keyword rerank)
✔ FAISS vector store
✔ YAML workflow routing, including simulated execution driven by the routing
  decision (queue/priority), not just logging
✔ Capability-based permission checks (static configured role — no
  authentication)
✔ Basic audit trail (JSONL, not tamper-evident)
✔ Environment-configurable paths and default role
✔ Minimal automated test suite (`pytest`) covering routing, permissions, and
  execution behaviour
✔ Container build verified locally (`docker build` + `docker run`, see
  `docs/RUNBOOK.md`)

Not implemented (not "coming soon" — out of scope for this prototype):

- Authentication / per-user identity
- Real external integrations (queueing, webhooks, notifications) — execution
  is simulated only
- Tamper-evident or access-controlled audit storage
- An HTML UI beyond the single static demo page in `ui/`

Project Lineage

This repository represents an early, self-contained stage of this governed
workflow-routing concept. It is kept public as an accurate record of that
stage. Development of this idea continued afterward in a separate, private
project that is not published here and is out of scope for this repository —
nothing from that later work has been backported into DocuFlow v2. If you're
evaluating this repo, treat it as a snapshot of an earlier prototype, not the
current state of the underlying idea.

This repository also contains `legacy_prototype/`, an even earlier set of
prototype scripts that predate `ml-api-service/`, kept for historical
reference only and not part of the current architecture described above (see
`legacy_prototype/README.md`).
