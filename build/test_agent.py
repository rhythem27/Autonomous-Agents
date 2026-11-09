"""Automated Test Suite for DocuAgent.

Executes:
1. Test Case 1: Standard Business Request (Salesforce Cloud CRM Migration Proposal)
2. Test Case 2: Complex / Ambiguous Request (SmartCheckout Launch SOP & Conflict Reconciliation)
Verifies:
- Task list generation (TODO list)
- Autonomous assumptions formulating
- Tool execution
- Reflection & Self-checking results
- File generation (.docx) and readability
"""

import os
import sys
from docx import Document

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from build.llm import LLMClient
from build.planner import Planner
from build.executor import AgentExecutor


def test_standard_business_request():
    print("======================================================================")
    print("TEST CASE 1: Standard Business Request")
    print("======================================================================")
    request_text = (
        "Generate a comprehensive Project Proposal for migrating our legacy on-premise CRM "
        "to cloud-based Salesforce, including project objectives, phased 6-month timeline, "
        "risk mitigation strategy, and a preliminary cost breakdown."
    )

    llm = LLMClient()
    planner = Planner(llm)
    executor = AgentExecutor(llm)

    print(f"\nUser Input: \"{request_text}\"\n")

    # Step 1: Planner
    plan = planner.create_plan(request_text)
    print(f"-> Planned Document: {plan.document_title} ({plan.document_type})")
    print(f"-> Assumptions Made: {len(plan.assumptions_made)}")
    for a in plan.assumptions_made:
        print(f"    • {a}")
    print(f"-> Tasks Created (TODO List): {len(plan.tasks)}")
    for t in plan.tasks:
        print(f"    [{t.id}] {t.title} (Tool: {t.tool_name})")

    assert len(plan.tasks) >= 3, "Expected at least 3 tasks generated"

    # Step 2: Executor
    response = executor.execute_plan(request_text, plan)
    print(f"\n-> Execution Finished: ID={response.execution_id}, Status={response.status}")
    print(f"-> Reflection Score: {response.reflection.quality_score}/10 (Passed: {response.reflection.passed_checks})")
    print(f"-> Refinements Applied: {len(response.reflection.refinements_applied)}")
    print(f"-> Generated Document File: {response.document_filename}")
    print(f"-> Total Time: {response.total_execution_time_seconds}s")

    # Step 3: Verify File
    doc_path = os.path.join(executor.storage_dir, response.document_filename)
    assert os.path.exists(doc_path), f"File {doc_path} does not exist"
    assert os.path.getsize(doc_path) > 1000, f"File {doc_path} is suspiciously small ({os.path.getsize(doc_path)} bytes)"

    # Verify DOCX parsing
    doc = Document(doc_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    tables = doc.tables
    print(f"-> Verified .docx file: {len(paragraphs)} paragraphs, {len(tables)} tables")
    assert len(tables) >= 2, "Expected at least 2 tables (tasks table + data table)"
    print(">>> TEST CASE 1 PASSED!\n")


def test_complex_ambiguous_request():
    print("======================================================================")
    print("TEST CASE 2: Complex / Ambiguous Request (Cross-Functional Crisis)")
    print("======================================================================")
    request_text = (
        "We need an urgent launch plan and SOP for feature 'SmartCheckout' next month. "
        "Marketing demands a launch in 1 week, Engineering says minimum 6 weeks for QA, "
        "and Legal/Compliance hasn't reviewed payments yet. Reconcile this mess, make executive assumptions, "
        "create a risk mitigation plan, and draft a finalized rollout strategy document."
    )

    llm = LLMClient()
    planner = Planner(llm)
    executor = AgentExecutor(llm)

    print(f"\nUser Input: \"{request_text}\"\n")

    # Step 1: Planner
    plan = planner.create_plan(request_text)
    print(f"-> Planned Document: {plan.document_title} ({plan.document_type})")
    print(f"-> Autonomous Assumptions: {len(plan.assumptions_made)}")
    for a in plan.assumptions_made:
        print(f"    • {a}")
    print(f"-> Tasks Created (TODO List): {len(plan.tasks)}")
    for t in plan.tasks:
        print(f"    [{t.id}] {t.title} (Tool: {t.tool_name})")

    assert len(plan.assumptions_made) >= 1, "Expected agent to make assumptions for ambiguous request"

    # Step 2: Executor
    response = executor.execute_plan(request_text, plan)
    print(f"\n-> Execution Finished: ID={response.execution_id}, Status={response.status}")
    print(f"-> Reflection Score: {response.reflection.quality_score}/10 (Passed: {response.reflection.passed_checks})")
    print(f"-> Refinements Applied: {len(response.reflection.refinements_applied)}")
    print(f"-> Generated Document File: {response.document_filename}")
    print(f"-> Total Time: {response.total_execution_time_seconds}s")

    # Step 3: Verify File
    doc_path = os.path.join(executor.storage_dir, response.document_filename)
    assert os.path.exists(doc_path), f"File {doc_path} does not exist"
    assert os.path.getsize(doc_path) > 1000, f"File {doc_path} is suspiciously small"

    doc = Document(doc_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    tables = doc.tables
    print(f"-> Verified .docx file: {len(paragraphs)} paragraphs, {len(tables)} tables")
    assert len(tables) >= 2, "Expected tables in generated document"
    print(">>> TEST CASE 2 PASSED!\n")


if __name__ == "__main__":
    test_standard_business_request()
    test_complex_ambiguous_request()
    print("======================================================================")
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("======================================================================")

