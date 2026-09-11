
 DocuFlow v2 – Architecture Diagram

 Mermaid Diagram (Preferred)

mermaid
flowchart TD
    A[Client / API Consumer] -->|HTTP| B[FastAPI API Layer]

    %% Core API
    B --> C[Hybrid Search Endpoint]
    B --> D[Route-from-Search Endpoint]

    %% Hybrid Search
    C --> E[FAISS Vector Store]
    E --> C
    C --> F[Hybrid Reranker]
    F --> C

    %% Routing Flow
    D --> G[Text Classifier]
    D --> H[Workflow Router]
    H --> I[rules.yaml]

    %% Governance
    D --> J[Permission Guard]
    J --> K[Roles & Capabilities]

    %% Execution
    D --> L[Workflow Executor]

    %% Audit
    D --> M[Audit Logger]
    M --> N[audit_logs/*.jsonl]

    %% Storage
    E --> O[data/store.index]
    E --> P[data/metadata.json]


 ASCII Diagram (Fallback)


┌──────────────┐
│ Client / API │
└──────┬───────┘
       │ HTTP
┌──────▼───────────────┐
│ FastAPI Application  │
└──────┬───────────────┘
       │
       ├── Hybrid Search
       │     ├── FAISS Vector Store
       │     │     ├── store.index
       │     │     └── metadata.json
       │     └── Keyword Reranker
       │
       └── Route-from-Search
             ├── Text Classifier
             ├── Workflow Router
             │     └── rules.yaml
             ├── Permission Guard
             │     └── Roles & Capabilities
             ├── Workflow Executor
             └── Audit Logger
                   └── audit_logs/*.jsonl


 Architecture Principles

- Search is semantic-first (FAISS) with deterministic reranking
- Routing logic is externalised and auditable
- Permissions and audit are enforced outside business logic
- Industry-agnostic by design

 Scope of this diagram
This diagram describes the current, documented DocuFlow v2 system, which
lives entirely under `ml-api-service/`. The repository also contains
`legacy_prototype/`, an earlier and architecturally unrelated set of
prototype scripts (see `legacy_prototype/README.md`) — it is not part of this
architecture and nothing in it is used by the system shown above.

Note also that "Permission Guard" here enforces a capability check against a
single statically configured role (no authentication / no per-user
identity), and "Workflow Executor" performs simulated execution only — it
does not call any real external queue, webhook, or notification system.
