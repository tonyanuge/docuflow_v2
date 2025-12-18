
 DocuFlow v2 – Operational Runbook

 Purpose
Operational guidance for running, maintaining, and troubleshooting DocuFlow v2.

 Service Startup
uvicorn app.main:app --host 0.0.0.0 --port 8001

 Health Check
GET /

 Common Operations
- POST /ingest-file
- POST /hybrid-search
- POST /route-from-search

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
No secrets in code. Role assignment currently static.

 Incident Response
Identify audit record, review rule, apply fix, re-run if needed.

 Decommissioning
Stop service, archive audit logs, back up FAISS data.

 Final Note
System fails safely by design.
