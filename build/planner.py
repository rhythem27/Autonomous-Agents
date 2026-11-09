"""Autonomous Planning Module.

Analyzes natural language requests, resolves ambiguities, formulates assumptions,
and generates a structured execution plan (TODO list).
"""

from typing import Dict, Any
from build.schemas import Plan, Task, TaskStatus
from build.llm import LLMClient


PLANNER_SYSTEM_PROMPT = """You are an Autonomous AI Planning Agent specialized in enterprise document architecture.
Your goal is to inspect a user request, identify the desired document type (e.g. Project Proposal, SOP, Launch Strategy, Technical Spec), detect any ambiguities, missing parameters, or conflicting requirements, make sensible executive assumptions, and decompose the work into an ordered list of tasks (TODO list).

You must select from these tools for each task:
- 'reconciliation_tool': Use when there are conflicting requirements or competing stakeholder interests.
- 'draft_section_tool': Use to draft rich narrative content, principles, and bullet points for a section.
- 'table_generator_tool': Use when structured metrics, timelines, risk matrices, budget tables, or RACI charts are required.

Respond strictly in the following JSON format:
{
  "document_title": "string",
  "document_type": "string",
  "executive_summary": "string",
  "assumptions_made": ["string"],
  "tasks": [
    {
      "id": 1,
      "title": "string",
      "description": "string",
      "tool_name": "draft_section_tool | table_generator_tool | reconciliation_tool",
      "status": "pending",
      "reasoning": "string"
    }
  ]
}
"""


class Planner:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def create_plan(self, user_request: str) -> Plan:
        """Analyzes the user request and outputs a validated Plan."""
        prompt = (
            f"Please analyze this user request, determine the required document, formulate assumptions "
            f"for any missing or conflicting elements, and generate a 3 to 5 step execution plan (TODO list):\n\n"
            f"Request: \"{user_request}\""
        )

        plan_data = self.llm.generate_json(prompt, system_prompt=PLANNER_SYSTEM_PROMPT)

        # Ensure task status defaults to PENDING
        tasks = []
        for t in plan_data.get("tasks", []):
            task_obj = Task(
                id=t.get("id", len(tasks) + 1),
                title=t.get("title", f"Task {len(tasks) + 1}"),
                description=t.get("description", ""),
                tool_name=t.get("tool_name", "draft_section_tool"),
                status=TaskStatus.PENDING,
                reasoning=t.get("reasoning", "")
            )
            tasks.append(task_obj)

        return Plan(
            document_title=plan_data.get("document_title", "Autonomous Enterprise Document"),
            document_type=plan_data.get("document_type", "Business Report"),
            executive_summary=plan_data.get("executive_summary", "Autonomous document generated based on user request."),
            assumptions_made=plan_data.get("assumptions_made", []),
            tasks=tasks
        )

