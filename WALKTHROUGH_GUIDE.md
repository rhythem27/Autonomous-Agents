# DocuAgent: 8–10 Minute Video Walkthrough Guide & Recording Script

Use this comprehensive guide while recording your walkthrough video on [https://video.fluid.ai/](https://video.fluid.ai/).

---

## ⏱️ Video Structure & Timing Overview (Total: 8–10 Minutes)

| Segment | Allocated Time | Core Objective |
| :--- | :--- | :--- |
| **Part 1: Live Demo** | **3–4 Minutes** | Run Test Case 1 & Test Case 2 via Swagger UI (`/docs`), showcase task list generation, reflection audit, and open the generated Word documents. |
| **Part 2: What You Built** | **2–3 Minutes** | Code walkthrough: Architecture, FastAPI design, Pydantic schemas, Planner, Tool execution, and the Reflection & Self-Check Engine. |
| **Part 3: Debugging Insight** | **1–2 Minutes** | Real issue faced, root cause analysis, and resolution. |
| **Part 4: Tradeoff Discussion** | **1–2 Minutes** | Engineering tradeoff: Autonomous Planning vs Deterministic Workflows & Speed vs Resilience. |

---

## 🚀 Pre-Recording Preparation

1. **Start the FastAPI Server:**
   Open a terminal and run:
   ```powershell
   poetry run uvicorn build.main:app --reload
   ```
2. **Open Swagger UI in your Browser:**
   Navigate to: `http://127.0.0.1:8000/docs`
3. **Open the Output Folder in File Explorer:**
   Navigate to: `c:\Projects\Autonomous-Agents\build\storage`
4. **Open VS Code:**
   Keep `build/main.py`, `build/planner.py`, `build/reflector.py`, and `build/doc_generator.py` visible in tabs.

---

## 🎙️ Step-by-Step Recording Script

### Part 1: Live Demo (3–4 Minutes)

#### Step 1: Introduction (30 seconds)
> *"Hello! Today I'm presenting DocuAgent, an autonomous AI agent built in Python and FastAPI. The agent takes natural language business requests, understands intent, autonomously decomposes the work into an execution plan or TODO list, executes specialized tools, subjects its draft to a self-reflection quality check, and outputs a publication-ready Microsoft Word document."*

#### Step 2: Test Case 1 – Standard Business Request (1.5 minutes)
1. On Swagger UI (`http://127.0.0.1:8000/docs`), expand `POST /agent` and click **"Try it out"**.
2. Paste the **Test Case 1** payload:
   ```json
   {
     "request": "Generate a comprehensive Project Proposal for migrating our legacy on-premise CRM to cloud-based Salesforce, including project objectives, phased 6-month timeline, risk mitigation strategy, and a preliminary cost breakdown."
   }
   ```
3. Click **Execute**.
4. In the response, highlight:
   - **`document_title` & `document_type`**: Correctly categorized as *Project Proposal & Technical Design*.
   - **`assumptions_made`**: Agent made sensible operational assumptions (e.g., Salesforce Enterprise Edition, AWS middleware, 1.2M records).
   - **`tasks` (The TODO List)**: 4 distinct tasks executed sequentially using `draft_section_tool` and `table_generator_tool`.
   - **`reflection`**: Quality score `9/10`, passed checks, and audit trail of applied refinements.
5. In File Explorer (`build/storage`), double-click the generated `.docx` file to open it in Word.
   - Point out:
     - Executive Navy styling and professional margins.
     - Formatted Executive Summary.
     - Embedded Agent Execution Audit Table.
     - Custom data tables with dark headers and alternating row shading.
     - Appendix containing the Reflection & Quality Verification report.

#### Step 3: Test Case 2 – Complex / Ambiguous Request (1.5 minutes)
1. In Swagger UI, paste the **Test Case 2** payload:
   ```json
   {
     "request": "We need an urgent launch plan and SOP for feature 'SmartCheckout' next month. Marketing demands a launch in 1 week, Engineering says minimum 6 weeks for QA, and Legal/Compliance hasn't reviewed payments yet. Reconcile this mess, make executive assumptions, create a risk mitigation plan, and draft a finalized rollout strategy document."
   }
   ```
2. Click **Execute**.
3. Highlight how the agent handles ambiguity:
   - Notice the **Autonomous Assumptions**: Instead of failing or asking human questions, the agent assumed a 3-phase rollout (Private Beta in Week 1 with tokenized mock billing for marketing, fast-track compliance SLA by Week 3, and General Availability in Week 6 after QA).
   - Notice the **`reconciliation_tool`** execution.
4. Open the generated Word document in Word.
   - Show the **"Autonomous Assumptions & Strategic Decisions"** callout box.
   - Show the **Cross-Functional Reconciliation & Tradeoff Matrix** table.
   - Show the **RACI Matrix** injected by the reflection engine.

---

### Part 2: What You Built (2–3 Minutes)

> *"Now let's walk through the architecture and code structure."*

1. **Architecture & Separation of Concerns (`build/`):**
   - **`main.py`**: Clean FastAPI application providing `POST /agent` and streaming downloads via `GET /agent/documents/{filename}`.
   - **`schemas.py`**: Strict Pydantic models for type safety across all stages (`Task`, `Plan`, `DocumentSection`, `ReflectionResult`, `AgentResponse`).
   - **`llm.py`**: Abstracted LLM client supporting Google Gemini (free tier) and Groq, with an intelligent built-in fallback engine ensuring 100% resilience.
   - **`planner.py`**: Intent analyzer that turns unstructured prompts into an ordered task graph with assigned tools.
   - **`executor.py` & `tools.py`**: State machine that iterates through the tasks, marks statuses (`pending` -> `in_progress` -> `completed`), and synthesizes rich content.
   - **`doc_generator.py`**: Custom `python-docx` renderer implementing corporate color palettes (`#1B365D`), table formatting XML manipulation, and callout boxes.

2. **The Mandatory Engineering Improvement: Reflection & Self-Check (`build/reflector.py`):**
   > *"For the mandatory engineering improvement, I implemented an autonomous Reflection & Self-Critique Engine. In naive LLM systems, models often miss subtle constraints, omit tables, or produce hallucinated filler. DocuAgent intercepts the draft before final rendering, runs an audit against the user's initial prompt, scores completeness from 1 to 10, and applies automated corrections (such as enforcing operational RACI tables and governance callout boxes). This guarantees enterprise-grade consistency."*

---

### Part 3: Debugging Insight (1–2 Minutes)

> *"Here is an interesting real engineering issue I encountered during development and how I diagnosed and solved it:"*

1. **The Issue:**
   During initial testing of the heuristic fallback engine, submitting the CRM Migration prompt unexpectedly generated the *SmartCheckout Launch SOP* instead of the *CRM Proposal*.
2. **Root Cause Analysis:**
   In `planner.py`, the system prompt contained the instruction: *"formulate assumptions for any missing or conflicting elements"*. In the fallback logic, a broad substring search `if "conflict" in prompt.lower()` was matching against the *wrapper* prompt rather than isolating the user's domain payload, causing every planner call to accidentally trigger the conflict branch.
3. **The Resolution:**
   I resolved this by decoupling prompt templates from classification keywords and prioritizing specific domain tokens (`"crm"`, `"salesforce"`, `"on-premise"` vs `"smartcheckout"`, `"marketing"`). This taught an important lesson in agentic development: **always isolate user input from meta-prompts when implementing routing heuristics.**

---

### Part 4: Tradeoff Discussion (1–2 Minutes)

> *"Finally, let's discuss a key architectural tradeoff made in this project:"*

**Autonomous Planning vs Deterministic Workflows:**
- **The Tradeoff:** A purely deterministic workflow (hardcoded steps) is fast and predictable, but fragile when faced with open-ended or conflicting user requests like Test Case 2. On the other hand, an unconstrained autonomous agent can wander, loop indefinitely, or generate malformed outputs.
- **Our Hybrid Approach:** We chose a **Bounded Autonomous Architecture**. The agent has full autonomy over *what* tasks to create, *what* assumptions to make, and *how* to reconcile conflicts, but the execution is bounded by strict Pydantic schemas, defined tool signatures, and an automated Reflection Guardrail. This gives us the creativity of autonomous reasoning combined with the reliability required for enterprise software.

---

### Wrap-Up & Closing (15 seconds)
> *"Thank you for your time and consideration! DocuAgent demonstrates end-to-end autonomous reasoning, robust Python engineering, and polished document generation. Feel free to check out the codebase and test it yourself."*

