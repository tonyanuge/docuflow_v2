
 DocuFlow v2 – System Documentation

 Purpose
DocuFlow v2 is a governed AI workflow engine that ingests documents, performs hybrid search, classifies intent, routes workflows via rules, enforces permissions, and records auditable decisions.

Designed to be:
- Industry-agnostic
- Self-hosted
- Explainable
- Audit-ready

 Core Concepts
 Hybrid Search
Combines semantic recall (FAISS) with keyword reranking for deterministic and explainable results.

 Workflow Routing
Routing logic is externalised to YAML. Rules are evaluated in order, first match wins, with a safe default fallback.

 Governance Model
Roles and capabilities are enforced at execution time using guards, ensuring controlled and auditable behaviour.

 Audit & Lineage
All routing executions are logged in append-only JSONL format with role, classification, decision, and outcome.

 Key Components
FastAPI, FAISS, Hybrid Search, Workflow Router, Executor, Security Guard, Audit Logger.

 Configuration
All environment-sensitive values are externalised via environment variables to support local, on-prem, and container deployments.

 Supported Operations
Document ingestion, hybrid search, workflow routing, permission enforcement, and audit logging.

 Non-Goals
No autonomous actions, no hidden logic, no SaaS dependency.

 Deployment Model
Backend-first engine designed for internal systems and governed environments.

 Summary
DocuFlow v2 prioritises control over automation for regulated and high-trust environments.
