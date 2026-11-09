"""Professional Microsoft Word (.docx) document generator.

Applies clean typography, corporate color palette, styled callout boxes,
and custom formatted tables.
"""

import os
from typing import List, Optional
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from schemas import DocumentSection, TableData, Task, ReflectionResult


# Corporate Palette
COLOR_PRIMARY = RGBColor(0x1B, 0x36, 0x5D)    # Navy
COLOR_SECONDARY = RGBColor(0x2B, 0x6C, 0xB0)  # Slate Blue
COLOR_ACCENT = RGBColor(0xC5, 0x30, 0x30)     # Amber/Red Accent
COLOR_TEXT = RGBColor(0x2D, 0x37, 0x48)       # Charcoal Body
COLOR_MUTED = RGBColor(0x71, 0x80, 0x96)      # Muted Gray
HEX_PRIMARY = "1B365D"
HEX_LIGHT_BG = "F7FAFC"
HEX_CALLOUT_BG = "EBF8FF"
HEX_CALLOUT_BORDER = "3182CE"
HEX_BORDER = "CBD5E0"


def set_cell_background(cell, hex_color: str):
    """Sets background shading of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets internal padding (in twips) of a table cell."""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tc_pr.append(tc_mar)


def create_callout_box(doc: Document, text: str, title: str = "KEY ASSUMPTION & EXECUTIVE DECISION"):
    """Creates a beautifully styled callout box with a colored left border and light background."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_CALLOUT_BG)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=180)

    # Left border only
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="{HEX_CALLOUT_BORDER}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tc_pr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run_title = p.add_run(f"[{title}]\n")
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(9.5)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_SECONDARY

    run_text = p.add_run(text)
    run_text.font.name = "Segoe UI"
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = COLOR_TEXT

    # Empty spacer after table
    spacer = doc.add_paragraph()
    spacer.paragraph_format.space_before = Pt(4)
    spacer.paragraph_format.space_after = Pt(6)


def format_table(table, table_data: TableData):
    """Applies corporate styling, dark header, and zebra striping to a Word table."""
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = True

    # Style Header Row
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(table_data.headers):
        cell = hdr_cells[i]
        set_cell_background(cell, HEX_PRIMARY)
        set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(header_text)
        run.font.name = "Segoe UI"
        run.font.size = Pt(10)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Style Data Rows
    for row_idx, row_data in enumerate(table_data.rows, start=1):
        row = table.rows[row_idx]
        is_even = (row_idx % 2 == 0)
        bg_color = HEX_LIGHT_BG if is_even else "FFFFFF"

        for col_idx, cell_value in enumerate(row_data):
            if col_idx < len(row.cells):
                cell = row.cells[col_idx]
                set_cell_background(cell, bg_color)
                set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(str(cell_value))
                run.font.name = "Segoe UI"
                run.font.size = Pt(9.5)
                run.font.color.rgb = COLOR_TEXT

    # Apply thin borders across table
    tbl_pr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:left w:val="none"/>'
        f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="{HEX_PRIMARY}"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tbl_pr.append(borders)


def build_docx_document(
    output_path: str,
    document_title: str,
    document_type: str,
    executive_summary: str,
    assumptions: List[str],
    tasks: List[Task],
    sections: List[DocumentSection],
    reflection: Optional[ReflectionResult] = None
) -> str:
    """Generates a complete, publication-grade Microsoft Word document."""
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc = Document()

    # 1. Page Setup: 1-inch margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

        # Header / Footer
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        ft_run = p_ft.add_run(f"{document_type}  |  Generated by DocuAgent  |  Confidential")
        ft_run.font.name = "Segoe UI"
        ft_run.font.size = Pt(8.5)
        ft_run.font.color.rgb = COLOR_MUTED

    # 2. Document Banner / Tag
    p_tag = doc.add_paragraph()
    p_tag.paragraph_format.space_before = Pt(0)
    p_tag.paragraph_format.space_after = Pt(2)
    run_tag = p_tag.add_run(document_type.upper())
    run_tag.font.name = "Segoe UI"
    run_tag.font.size = Pt(10)
    run_tag.font.bold = True
    run_tag.font.color.rgb = COLOR_SECONDARY

    # 3. Main Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    run_title = p_title.add_run(document_title)
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(24)
    run_title.font.bold = True
    run_title.font.color.rgb = COLOR_PRIMARY

    # 4. Metadata Strip
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(18)
    meta_run = p_meta.add_run("Author: Autonomous AI Agent  •  Version: 1.0 Final  •  Status: Approved")
    meta_run.font.name = "Segoe UI"
    meta_run.font.size = Pt(9.5)
    meta_run.font.color.rgb = COLOR_MUTED

    # Divider Line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(0)
    p_div.paragraph_format.space_after = Pt(14)
    p_div_border = parse_xml(
        f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="{HEX_PRIMARY}"/></w:pBdr>'
    )
    p_div._p.get_or_add_pPr().append(p_div_border)

    # 5. Executive Summary
    h_exec = doc.add_paragraph()
    h_exec.paragraph_format.space_before = Pt(12)
    h_exec.paragraph_format.space_after = Pt(4)
    r_h_exec = h_exec.add_run("Executive Summary")
    r_h_exec.font.name = "Segoe UI"
    r_h_exec.font.size = Pt(15)
    r_h_exec.font.bold = True
    r_h_exec.font.color.rgb = COLOR_PRIMARY

    p_exec = doc.add_paragraph()
    p_exec.paragraph_format.line_spacing = 1.15
    p_exec.paragraph_format.space_after = Pt(12)
    r_exec = p_exec.add_run(executive_summary)
    r_exec.font.name = "Segoe UI"
    r_exec.font.size = Pt(11)
    r_exec.font.color.rgb = COLOR_TEXT

    # 6. Assumptions & Autonomous Decisions (if any)
    if assumptions:
        assumptions_text = "\n".join([f"•  {a}" for a in assumptions])
        create_callout_box(
            doc,
            assumptions_text,
            title="AUTONOMOUS ASSUMPTIONS & STRATEGIC DECISIONS MADE BY AGENT"
        )

    # 7. Agent Execution Plan / Task List Section
    h_tasks = doc.add_paragraph()
    h_tasks.paragraph_format.space_before = Pt(12)
    h_tasks.paragraph_format.space_after = Pt(4)
    r_tasks = h_tasks.add_run("Agent Execution Plan & Audit Trail")
    r_tasks.font.name = "Segoe UI"
    r_tasks.font.size = Pt(14)
    r_tasks.font.bold = True
    r_tasks.font.color.rgb = COLOR_PRIMARY

    # Task Table
    task_tbl_data = TableData(
        caption="Agent Task Execution Breakdown",
        headers=["#", "Task Name", "Tool Used", "Status", "Execution Result"],
        rows=[
            [
                str(t.id),
                t.title,
                t.tool_name,
                t.status.upper() if isinstance(t.status, str) else t.status.value.upper(),
                t.output[:75] + ("..." if t.output and len(t.output) > 75 else "") if t.output else "Executed"
            ]
            for t in tasks
        ]
    )
    tbl_elem = doc.add_table(rows=len(task_tbl_data.rows) + 1, cols=len(task_tbl_data.headers))
    format_table(tbl_elem, task_tbl_data)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(16)

    # 8. Main Body Sections
    for section in sections:
        h_sec = doc.add_paragraph()
        h_sec.paragraph_format.space_before = Pt(16)
        h_sec.paragraph_format.space_after = Pt(4)
        r_sec = h_sec.add_run(section.section_title)
        r_sec.font.name = "Segoe UI"
        r_sec.font.size = Pt(14)
        r_sec.font.bold = True
        r_sec.font.color.rgb = COLOR_PRIMARY

        if section.subheading:
            p_sub = doc.add_paragraph()
            p_sub.paragraph_format.space_before = Pt(0)
            p_sub.paragraph_format.space_after = Pt(4)
            r_sub = p_sub.add_run(section.subheading)
            r_sub.font.name = "Segoe UI"
            r_sub.font.size = Pt(10.5)
            r_sub.font.italic = True
            r_sub.font.color.rgb = COLOR_SECONDARY

        # Narrative Content
        p_cnt = doc.add_paragraph()
        p_cnt.paragraph_format.line_spacing = 1.15
        p_cnt.paragraph_format.space_after = Pt(8)
        r_cnt = p_cnt.add_run(section.content)
        r_cnt.font.name = "Segoe UI"
        r_cnt.font.size = Pt(11)
        r_cnt.font.color.rgb = COLOR_TEXT

        # Bullet points
        if section.bullet_points:
            for bp in section.bullet_points:
                p_bp = doc.add_paragraph(style="List Bullet")
                p_bp.paragraph_format.space_before = Pt(2)
                p_bp.paragraph_format.space_after = Pt(2)
                p_bp.paragraph_format.line_spacing = 1.15
                r_bp = p_bp.add_run(bp)
                r_bp.font.name = "Segoe UI"
                r_bp.font.size = Pt(10.5)
                r_bp.font.color.rgb = COLOR_TEXT

        # Callout box if attached to section
        if section.callout_box:
            create_callout_box(doc, section.callout_box, title="SECTION FOCUS / COMPLIANCE NOTE")

        # Table if attached to section
        if section.table and section.table.headers and section.table.rows:
            if section.table.caption:
                p_cap = doc.add_paragraph()
                p_cap.paragraph_format.space_before = Pt(8)
                p_cap.paragraph_format.space_after = Pt(2)
                r_cap = p_cap.add_run(f"Table: {section.table.caption}")
                r_cap.font.name = "Segoe UI"
                r_cap.font.size = Pt(10)
                r_cap.font.bold = True
                r_cap.font.color.rgb = COLOR_SECONDARY

            s_table = doc.add_table(
                rows=len(section.table.rows) + 1,
                cols=len(section.table.headers)
            )
            format_table(s_table, section.table)

            p_sp = doc.add_paragraph()
            p_sp.paragraph_format.space_after = Pt(10)

    # 9. Quality Verification & Reflection Report (Appendix)
    if reflection:
        h_ref = doc.add_paragraph()
        h_ref.paragraph_format.space_before = Pt(20)
        h_ref.paragraph_format.space_after = Pt(4)
        r_ref = h_ref.add_run("Appendix: Agent Self-Reflection & Quality Verification")
        r_ref.font.name = "Segoe UI"
        r_ref.font.size = Pt(13)
        r_ref.font.bold = True
        r_ref.font.color.rgb = COLOR_PRIMARY

        ref_summary = (
            f"Quality Score: {reflection.quality_score}/10  |  "
            f"Verification Status: {'PASSED' if reflection.passed_checks else 'FLAGGED'}\n"
            f"Critique: {reflection.critique}\n\n"
            f"Refinements & Guardrails Applied:\n" +
            "\n".join([f"•  {r}" for r in reflection.refinements_applied or reflection.suggested_improvements])
        )
        create_callout_box(
            doc,
            ref_summary,
            title="MANDATORY ENGINEERING IMPROVEMENT: REFLECTION & SELF-CHECK"
        )

    # Save document
    doc.save(output_path)
    return output_path

