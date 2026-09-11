
 DocuFlow v2 – System Documentation

 Purpose
DocuFlow v2 is a prototype governed AI workflow-routing system. It ingests
documents, performs hybrid search, classifies intent, routes workflows via
rules, enforces capability-based permission checks, and records auditable
decisions.

Designed to be:
- Industry-agnostic
- Self-hosted
- Explainable

This is a working prototype, not a hardened or certified system — see
"Known Limitations" below and the top-level `README.md`'s "Project Lineage"
section for how it relates to later, unpublished work on the same concept.

 Core Concepts
 Hybrid Search
Combines semantic recall (FAISS) with keyword reranking for deterministic and explainable results.

 Workflow Routing
Routing logic is externalised to YAML. Rules are evaluated in order, first match wins, with a safe default fallback. Routing decisions (`queue`/`priority`) drive a simulated execution step — no real external system is called.

 Governance Model
Capabilities are enforced at execution time using a guard function, checked against a role. That role is currently a single statically configured value (`DOCUFLOW_DEFAULT_ROLE`) applied to every request — there is no authentication and no per-user identity in this repository. The permission check itself is real; what it checks against is not yet tied to a real caller.

 Audit & Lineage
All routing executions are logged in append-only JSONL format (append-only by convention — the file has no tamper-evidence or access control) with role, classification, decision, and outcome.

 Key Components
FastAPI, FAISS, Hybrid Search, Workflow Router, Executor, Security Guard, Audit Logger.

 Configuration
Default role, FAISS data paths, audit log location, and environment mode are externalised via environment variables (see `ml-api-service/app/config/settings.py`) to support local dev and single-container deployment.

 Supported Operations
Document ingestion, hybrid search, workflow routing, permission enforcement, and audit logging — all running in a single process, single-container deployment verified locally.

 Non-Goals
No autonomous actions, no hidden logic, no SaaS dependency, no real external side effects (execution is simulated).

 Known Limitations
- No authentication / no per-user RBAC — only a static configured role
- No tamper-evident or access-controlled audit storage
- No real queue/webhook/notification integrations
- Not verified beyond a single local container

 Deployment Model
Backend-first engine intended to illustrate a governed-routing pattern for internal systems. Deployment has been verified as a single local Docker container; it has not been tested or hardened for production, multi-instance, or regulated deployment.

 Summary
DocuFlow v2 demonstrates control-oriented workflow routing (search → classify → route → govern → audit) as a prototype. It is a foundation for that pattern, not a compliance-ready product.
