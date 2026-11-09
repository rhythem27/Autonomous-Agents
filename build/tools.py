"""Specialized tools for the autonomous agent to invoke during step execution."""

from typing import Dict, Any, List, Optional
from build.schemas import DocumentSection, TableData


def draft_section_tool(
    section_title: str,
    instructions: str,
    context: str,
    bullet_count: int = 4
) -> Dict[str, Any]:
    """Generates structured narrative text and bullet points for a specific section."""
    return {
        "tool": "draft_section_tool",
        "section_title": section_title,
        "instructions": instructions,
        "context": context,
        "bullet_count": bullet_count
    }


def table_generator_tool(
    caption: str,
    columns: List[str],
    context: str
) -> Dict[str, Any]:
    """Instructs the LLM/executor to produce a high-fidelity data matrix."""
    return {
        "tool": "table_generator_tool",
        "caption": caption,
        "columns": columns,
        "context": context
    }


def reconciliation_tool(
    conflict_summary: str,
    stakeholders: List[str],
    context: str
) -> Dict[str, Any]:
    """Reconciles conflicting timelines, scope constraints, and governance gaps."""
    return {
        "tool": "reconciliation_tool",
        "conflict_summary": conflict_summary,
        "stakeholders": stakeholders,
        "context": context
    }

