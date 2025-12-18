 Route-from-Search – Sequence Diagram

This document describes the **end-to-end execution flow** for the `/route-from-search` endpoint in DocuFlow v2.

It shows how search, classification, routing, governance, execution, and auditing work together.



 Mermaid Sequence Diagram (GitHub-renderable)

mermaid
sequenceDiagram
    participant Client
    participant API as FastAPI (/route-from-search)
    participant Guard as Permission Guard
    participant FAISS as FAISS Vector Store
    participant Classifier
    participant Router as Workflow Router (YAML)
    participant Executor
    participant Audit as Audit Logger

    Client->>API: POST /route-from-search (query, top_k)

    API->>Guard: enforce_permission(role, EXECUTE_WORKFLOW)
    Guard-->>API: allowed

    API->>FAISS: hybrid_search(query, top_k)
    FAISS-->>API: contextual search results

    API->>Classifier: classify(query)
    Classifier-->>API: classification label

    API->>Router: route(classification, query)
    Router-->>API: routing decision

    API->>Executor: execute(decision, context)
    Executor-->>API: execution result

    API->>Audit: log(ROUTE_EXECUTED, payload)
    Audit-->>API: logged

    API-->>Client: response (decision, execution, search_results)




 ASCII Sequence Diagram (Fallback)


Client
  |
  | POST /route-from-search
  v
FastAPI
  |
  | enforce_permission(role, EXECUTE_WORKFLOW)
  v
Permission Guard
  |
  | OK
  v
FastAPI
  |
  | hybrid_search(query)
  v
FAISS Vector Store
  |
  | search results
  v
FastAPI
  |
  | classify(query)
  v
Classifier
  |
  | classification label
  v
FastAPI
  |
  | route(classification, query)
  v
Workflow Router (YAML)
  |
  | routing decision
  v
FastAPI
  |
  | execute(decision)
  v
Workflow Executor
  |
  | execution result
  v
FastAPI
  |
  | audit log
  v
Audit Logger
  |
  | response
  v
Client




 Why This Matters

- **Traceability**: Every decision is explainable end-to-end
- **Governance**: Permissions and rules are enforced before execution
- **Auditability**: Every execution is logged for compliance
- **Extensibility**: Auth, UI, async execution can be added without refactor

This diagram is suitable for:
- Architecture reviews
- Interviews
- Compliance walkthroughs
- Runbooks and onboarding


