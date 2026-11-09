# DocuAgent: Autonomous Document Synthesis Agent

DocuAgent is an autonomous AI agent built in Python and FastAPI. It accepts natural language business requests, understands intent, autonomously decomposes requirements into an execution plan (TODO list), invokes specialized tools, evaluates its work via a Reflection & Self-Check Engine, and outputs publication-grade Microsoft Word (`.docx`) documents.

---

## 🌟 Key Features

1. **Autonomous Planning Engine (`planner.py`)**:
   - Parses open-ended, ambiguous, or conflicting business requests.
   - Autonomously formulates logical assumptions to resolve gaps.
   - Decomposes goals into an ordered task list (`TODO list`) with assigned tools.
2. **Tool Orchestration (`executor.py` & `tools.py`)**:
   - State-machine execution (`pending` ➔ `in_progress` ➔ `completed`).
   - Supports `draft_section_tool`, `table_generator_tool`, and `reconciliation_tool`.
3. **Mandatory Real Engineering Improvement: Reflection & Self-Check (`reflector.py`)**:
   - Audits drafted content against original constraints and user requirements.
   - Evaluates completeness, conflict reconciliation, and tone.
   - Issues a quality score (1–10) and applies automated refinements before document compilation.
4. **Professional Document Engine (`doc_generator.py`)**:
   - Custom `python-docx` renderer with an Executive Navy theme (`#1B365D`).
   - Generates metadata strips, callout highlight boxes, formatted tables with zebra striping, and an audit appendix.
5. **REST API (`main.py`)**:
   - `POST /agent`: Main agent execution endpoint.
   - `GET /agent/documents/{filename}`: File download endpoint.
   - Built-in Swagger UI at `/docs`.

---

## 🚀 Quickstart Guide

### 1. Configure Environment
Add your Gemini or Groq API key to `.env` (optional; built-in resilient fallback operates out-of-the-box):
```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Start the API Server
```powershell
poetry run uvicorn main:app --reload
```
Access the interactive Swagger UI at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 3. Run Automated Tests
```powershell
poetry run python test_agent.py
```

---

## 📹 Video Walkthrough & Script
For the complete 8–10 minute recording walkthrough script, see [WALKTHROUGH_GUIDE.md](file:///c:/Projects/Autonomous-Agents/WALKTHROUGH_GUIDE.md).
