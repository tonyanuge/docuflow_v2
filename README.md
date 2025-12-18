DocuFlow v2 – Governed AI Workflow Engine

DocuFlow v2 is an industry-agnostic, governed AI workflow engine that combines:
* Hybrid semantic + keyword search
* Rule-based workflow routing
* Role-based permissions
* Full auditability

It is designed for regulated and non-regulated organisations that need explainable, controllable AI-assisted decision routing.

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

Example:

routes:
  - when:
      classification: payment_request
      keyword_contains: [arrears, payment]
    route:
      department: finance
      action: review_payment
default_route:
  department: general_ops
  action: manual_review


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
AI decisions are controlled, not automatic.

4. Error Boundaries & Guardrails

The system fails predictably, not loudly.

Handled cases:

* Permission denied
* No search results
* No routing rule matched

Errors return structured responses.
No stack traces leak to clients.

5. Audit & Lineage (Regulator-Grade)

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

Stored as append-only JSONL.

Why it matters:
This is suitable for audits, compliance, and incident reviews.

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

All environment-sensitive values are externalised:
Default role
* FAISS paths
* Audit log location
* Environment mode

This enables:
* Local dev
* On-prem deployment
* Containerised deployment (Docker-ready)



What This Is (and Is Not)
This is:

* A production-grade backend engine
* Governance-first AI architecture
* Explainable and auditable by design

This is not:

* A black-box AI system
* A UI-heavy product
* A hard-coded finance-only tool

Project Status

✔ Hybrid search implemented
✔ FAISS vector store
✔ YAML workflow routing
✔ Role-based permissions
✔ Error guardrails
✔ Full audit trail
✔ Config hardening

Next (optional):

- Dockerisation
- HTML UI
- Authentication integration
