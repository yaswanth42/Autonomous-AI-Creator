# AutoPersona AI 🤖⚡
### Autonomous AI & Technology Persona Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js 15](https://img.shields.io/badge/Next.js-15.5+-black.svg?style=flat&logo=next.js&logoColor=white)](https://nextjs.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-StateGraph-FF4F00.svg?style=flat&logo=langchain&logoColor=white)](https://langchain-ai.github.io/langgraph/)
[![Python](https://img.shields.io/badge/Python-3.12%20%7C%203.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-38B2AC.svg?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-100%25%20Passing%20(85%25%20Coverage)-brightgreen.svg)]()

> **AutoPersona AI** is an autonomous AI agent engineered with persistent cognitive memory, multi-factor editorial gatekeeping, and automated scheduling to continuously discover, evaluate, and publish research-grounded technical publications.

---

## 🌟 Persona Specification: "Ada"
AutoPersona AI is pre-configured with **Ada**, an authoritative AI Security Specialist persona:
- **Domain:** AI Security, LLM Alignment, Agent Sandboxing, Cryptographic Watermarking, Model Safety.
- **Cognitive Traits:** Professional, Research-based, Technical, Friendly, Opinionated.
- **Editorial Mandate:** Strictly avoids clickbait/sensationalism, always explains technical mechanisms, always cites primary research sources, and maintains a consistent analytical voice across all publications.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Autonomous Scheduler (4-Hour Interval)
        A[APScheduler Trigger] --> B[Topic Discovery Engine]
    end

    subgraph Intelligence & Discovery
        B -->|Curated AI Keywords| C[Tavily Search / Research Sources]
        C --> D[Candidate Topics Pool]
    end

    subgraph Cognitive Pipeline (LangGraph)
        D --> E[Breeth Memory Engine]
        E -->|TF-IDF Semantic Vector Check| F{Duplicate / Novelty Gate}
        F -- Novel Topic --> G[7-Factor Editorial Engine]
        F -- Duplicate / Stale --> H[Drop Candidate]
        
        G -->|Score >= 7.0| I[Persona Generation Engine]
        G -->|Score < 7.0| J[Rejected Topics Store]
        
        I -->|LinkedIn Format: Hook + Body + Insights + Takeaway| K[Post Generator]
        K --> L[SQLite Persistent Store]
        K --> M[Breeth Memory Node Sync]
    end

    subgraph API & UI Layer
        L --> N[FastAPI REST Backend]
        N --> O[Next.js 15 Dashboard]
        O -->|Real-Time Telemetry| P[Feed, Status, Memory, Analytics, AI Usage]
    end
```

---

## 🚀 Key Features

1. **Autonomous 4-Hour Discovery Cycle**:
   - Background APScheduler job orchestrates continuous discovery of cutting-edge AI security intelligence.
2. **Breeth Memory Cognitive Engine**:
   - Custom TF-IDF cosine-similarity vector store with importance weighting, access counting, and recency decay.
   - Prevents duplicate topic coverage and guarantees consistent long-term editorial style.
3. **7-Factor Editorial Decision Engine**:
   - Scores candidates on: *Novelty (15%)*, *Importance (20%)*, *Trustworthiness (20%)*, *Trending Velocity (10%)*, *Technical Value (20%)*, *Community Impact (15%)*, and *Duplicate Penalty*.
   - Strict `7.0/10.0` quality threshold automatically separates top-tier publications from rejected noise.
4. **LangGraph State Graph Pipeline**:
   - Deterministic execution flow: `memory_check` ➔ `editorial_gate` ➔ `persona_generation` ➔ `memory_persist`.
5. **LinkedIn-Optimized Post Generator**:
   - Produces high-engagement 200–350 word publications featuring a bold headline, punchy hook, in-depth architectural breakdown, 3 key bulleted insights, and strategic takeaways with primary source citations.
6. **Glassmorphism Next.js 15 Dashboard**:
   - Dark theme dashboard with live pipeline metrics, LinkedIn publication feed with copy buttons, Breeth semantic search tester, rejected topic score visualizer, and prompt execution audit trail.
7. **AI Usage & Token Telemetry**:
   - Built-in audit trail logging token consumption, execution latencies, and milestone outputs.

---

## 📡 API Reference

### 1. Agent Initialization & Feed (Hackathon Specification)
- **`POST /api/agent/init`**
  - Initializes or retrieves the active persona.
  ```json
  {
    "name": "Ada",
    "domain": "AI Security",
    "characteristics": ["Professional", "Technical", "Opinionated"]
  }
  ```
- **`GET /api/agent/feed`**
  - Returns published posts in standard hackathon format:
  ```json
  {
    "posts": [
      {
        "id": "post-uuid",
        "createdAt": "2026-08-07T18:00:00Z",
        "text": "**Title**\n\nHook...\n\nBody...",
        "rationale": "High score on AI security impact.",
        "sources": [{"title": "Anthropic Research", "url": "https://..."}]
      }
    ],
    "count": 1
  }
  ```

### 2. Autonomous Control & Execution
- **`GET /api/agent/status`**: Returns current agent configuration and APScheduler cadence.
- **`POST /api/agent/trigger`**: Manually forces an autonomous discovery, editorial review, and publishing cycle.

### 3. Editorial & Rejections
- **`POST /api/editorial/evaluate`**: Evaluates a topic against the 7-factor editorial engine.
- **`GET /api/rejected/topics`**: Returns all candidate topics rejected by the quality gate with full score breakdowns.

### 4. Breeth Memory Engine
- **`POST /api/memory/query`**: Executes semantic vector search across cognitive nodes.
- **`GET /api/memory/items`**: Lists all active memory nodes categorized by type (`POST`, `REJECTED`, `PREFERENCE`, `STYLE`).
- **`GET /api/memory/stats`**: Returns cognitive memory distribution and node volume.

### 5. Analytics & AI-Usage Telemetry
- **`GET /api/analytics/dashboard`**: Telemetry metrics including daily publishing trends, category breakdowns, and source credibility.
- **`GET /api/ai-usage`**: Complete prompt execution log with token count, latency, and prompt history.

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.12 or 3.13
- Node.js 18+ and npm
- (Optional) OpenAI API Key / Tavily API Key

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env

# Run FastAPI backend server
uvicorn app.main:app --reload --port 8000
```
Backend will be live at `http://localhost:8000` (API Docs at `http://localhost:8000/docs`).

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install npm dependencies
npm install

# Start Next.js development server
npm run dev
```
Frontend dashboard will be accessible at `http://localhost:3000`.

---

## 🧪 Testing & Validation

AutoPersona AI features a 100% passing test suite with 85%+ code coverage:

```bash
# Run pytest with coverage report
python -m pytest backend/tests -v --cov=backend/app --cov-report=term-missing
```

### Test Suite Summary
- `test_models.py`: Database schema integrity, soft-delete, and feed serialization.
- `test_breeth_memory.py`: Semantic vector similarity, duplicate detection, and memory decay.
- `test_editorial_engine.py`: 7-Factor evaluation logic and rejection reason formulation.
- `test_post_generator.py`: Ada voice consistency, word length constraints (200-350w), and LinkedIn formatting.
- `test_api.py`: Full REST API endpoint integration tests.

---

## 📁 Repository Structure

```
Autonomous-AI-Creator/
├── backend/
│   ├── app/
│   │   ├── agents/          # LangGraph state machine & workflow nodes
│   │   ├── core/            # Config, logging, and AI token tracker
│   │   ├── database/        # SQLite engine, Base model, and session
│   │   ├── memory/          # Breeth Memory TF-IDF vector engine
│   │   ├── models/          # SQLAlchemy ORM models (Agent, Post, Memory, etc.)
│   │   ├── routers/         # FastAPI REST route endpoints
│   │   ├── scheduler/       # APScheduler jobs & autonomous runner
│   │   ├── schemas/         # Pydantic validation schemas
│   │   └── services/        # Editorial, Persona, Post Generator, Analytics
│   ├── tests/               # Comprehensive Pytest test suite
│   ├── requirements.txt     # Backend Python dependencies
│   └── run.py               # Direct entrypoint script
├── frontend/
│   ├── app/                 # Next.js 15 App router (page.tsx, layout.tsx)
│   ├── components/          # Dark-theme Glassmorphism Dashboard UI views
│   └── package.json         # Frontend dependencies & Next.js scripts
├── PROMPTS.md               # Complete AI Prompt execution audit log (1-15)
├── README.md                # Project documentation
└── LICENSE                  # MIT License
```

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
