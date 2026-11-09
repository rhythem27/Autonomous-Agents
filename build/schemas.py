from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    id: int = Field(..., description="Unique integer index of the task in execution order")
    title: str = Field(..., description="Clear, concise task title")
    description: str = Field(..., description="Actionable description of the specific work required")
    tool_name: str = Field(
        ...,
        description="Tool designated to execute this task: draft_section_tool, table_generator_tool, or reconciliation_tool"
    )
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current execution status of the task")
    reasoning: Optional[str] = Field(None, description="Why this task is necessary to complete the user request")
    output: Optional[str] = Field(None, description="Output or summary of results produced by this step")


class TableData(BaseModel):
    caption: Optional[str] = Field(None, description="Title or caption of the table")
    headers: List[str] = Field(..., description="Column header labels")
    rows: List[List[str]] = Field(..., description="Matrix of row data strings")


class DocumentSection(BaseModel):
    section_title: str = Field(..., description="Header title for the document section")
    subheading: Optional[str] = Field(None, description="Optional subheading or subtitle")
    content: str = Field(..., description="Detailed narrative paragraphs explaining the topic")
    bullet_points: List[str] = Field(default_factory=list, description="Key takeaway bullet points or numbered lists")
    table: Optional[TableData] = Field(None, description="Optional structured table for metrics, timelines, or matrices")
    callout_box: Optional[str] = Field(None, description="Optional highlight box for key decisions, warnings, or notes")


class Plan(BaseModel):
    document_title: str = Field(..., description="Formal title of the resulting business document")
    document_type: str = Field(
        ...,
        description="Type of document (e.g., 'Project Proposal', 'Rollout SOP & Strategy', 'Technical Architecture', 'Executive Report')"
    )
    executive_summary: str = Field(..., description="High-level overview of the document's objectives and approach")
    assumptions_made: List[str] = Field(
        default_factory=list,
        description="Assumptions or decisions made autonomously by the agent to resolve ambiguities or missing inputs"
    )
    tasks: List[Task] = Field(..., description="Ordered list of tasks the agent will execute")


class ReflectionResult(BaseModel):
    passed_checks: bool = Field(..., description="Whether the drafted document meets all criteria and constraints")
    quality_score: int = Field(..., ge=1, le=10, description="Overall completeness and quality score (1 to 10)")
    strengths: List[str] = Field(default_factory=list, description="Identified strengths of the drafted document")
    missing_elements: List[str] = Field(
        default_factory=list,
        description="Any missing requirements, unaddressed conflicts, or weak spots"
    )
    critique: str = Field(..., description="Detailed critique of the draft against the user's original request")
    suggested_improvements: List[str] = Field(
        default_factory=list,
        description="Specific recommendations applied during final document compilation"
    )
    refinements_applied: List[str] = Field(
        default_factory=list,
        description="Actions taken by the agent during reflection to correct and enhance the document"
    )


class AgentRequest(BaseModel):
    request: str = Field(..., min_length=5, description="Natural language prompt describing the desired document")


class AgentResponse(BaseModel):
    execution_id: str
    status: str
    request: str
    document_title: str
    document_type: str
    assumptions_made: List[str]
    tasks: List[Task]
    reflection: ReflectionResult
    sections_count: int
    document_filename: str
    document_download_url: str
    total_execution_time_seconds: float

