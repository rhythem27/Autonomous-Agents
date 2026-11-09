"""DocuAgent FastAPI Application.

Autonomous AI Agent that accepts natural language requests, formulates an execution plan,
orchestrates tools, applies self-reflection, and produces professional Microsoft Word (.docx) documents.
"""

import os
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from build.schemas import AgentRequest, AgentResponse
from build.llm import LLMClient
from build.planner import Planner
from build.executor import AgentExecutor

# Load environment configuration
load_dotenv()

app = FastAPI(
    title="DocuAgent: Autonomous Document Synthesis Agent",
    description=(
        "Autonomous AI agent that decomposes natural language business requests, "
        "generates an execution plan (TODO list), executes tasks via specialized tools, "
        "conducts reflection / self-checking, and produces publication-ready Word documents (.docx)."
    ),
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core agent services
STORAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "storage"))
os.makedirs(STORAGE_DIR, exist_ok=True)

llm_client = LLMClient()
planner = Planner(llm_client)
executor = AgentExecutor(llm_client, storage_dir=STORAGE_DIR)


@app.get("/", tags=["General"])
def read_root():
    """Health check and API overview."""
    gemini_configured = bool(llm_client.gemini_key)
    groq_configured = bool(llm_client.groq_key)
    active_provider = llm_client.provider

    return {
        "status": "healthy",
        "service": "DocuAgent API",
        "version": "1.0.0",
        "llm_configuration": {
            "active_provider": active_provider,
            "gemini_key_detected": gemini_configured,
            "groq_key_detected": groq_configured,
            "fallback_engine": "ready"
        },
        "endpoints": {
            "agent_execution": "POST /agent",
            "document_download": "GET /agent/documents/{filename}",
            "interactive_docs": "GET /docs"
        }
    }


@app.post(
    "/agent",
    response_model=AgentResponse,
    status_code=status.HTTP_200_OK,
    tags=["Agent"],
    summary="Execute Autonomous Document Synthesis"
)
async def run_agent(payload: AgentRequest):
    """Primary autonomous agent endpoint.

    1. Analyzes user request and creates an execution plan (TODO list).
    2. Sequentially executes planned tasks using tools.
    3. Runs the Mandatory Engineering Improvement: Reflection & Self-Check loop.
    4. Compiles and saves the formatted Word document (.docx).
    """
    request_text = payload.request.strip()
    if not request_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The 'request' field cannot be empty."
        )

    try:
        # Step 1: Autonomous Planning
        plan = planner.create_plan(request_text)

        # Step 2: Execution & Document Generation
        response = executor.execute_plan(request_text, plan)

        return response

    except Exception as e:
        print(f"[DocuAgent Error]: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}"
        )


@app.get(
    "/agent/documents/{filename}",
    tags=["Documents"],
    summary="Download Generated Word Document (.docx)"
)
async def download_document(filename: str):
    """Serves the generated Microsoft Word document for download."""
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(STORAGE_DIR, safe_filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Document '{safe_filename}' not found."
        )

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=safe_filename
    )


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("build.main:app", host=host, port=port, reload=True)

