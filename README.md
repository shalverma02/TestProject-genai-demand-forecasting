# TestProject-genai-demand-forecasting


graph TD
    %% Define Styles
    classDef external fill:#f9f,stroke:#333,stroke-width:2px;
    classDef script fill:#bbf,stroke:#333,stroke-width:2px;
    classDef rules fill:#ffd700,stroke:#333,stroke-width:2px;
    classDef ai fill:#a2fca2,stroke:#333,stroke-width:2px;

    subgraph "1. The Model (Data & Rules)"
        A[🌐 Google News RSS]:::external -->|Raw XML| B[🐍 data_ingestion.py]:::script
        B -->|Extracts Headlines| C(Python List)
        R[📐 Pydantic Schema]:::rules -.->|Forces structure| F
    end

    subgraph "2. The Controller (Orchestration & Logic)"
        C -->|Feeds Data| D[⚙️ ai_engine.py]:::script
        V[🔐 .env Vault] -->|API Key| D
        D -->|Prompt Payload| F((🧠 Gemini API)):::ai
        F -->|Returns Validated JSON| D
    end

    subgraph "3. The View (Presentation)"
        D -->|Prints Data| G[💻 VS Code Terminal]
        G -.->|Next Step Option| H[📊 Database / Web Dashboard]
    end