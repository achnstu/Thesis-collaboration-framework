"""Create a synthetic, editable table with two header levels and native rules."""

import argparse
from pathlib import Path

from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt


def element(name, **attributes):
    node = OxmlElement("w:" + name)
    for key, value in attributes.items():
        node.set(qn("w:" + key), str(value))
    return node


def borders(properties, values):
    name = "tblBorders" if properties.tag == qn("w:tblPr") else "tcBorders"
    old = properties.find(qn("w:" + name))
    if old is not None:
        properties.remove(old)
    node = element(name)
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        size = values.get(edge, 0)
        node.append(
            element(
                edge, val="single" if size else "nil", sz=size, color="000000", space=0
            )
        )
    properties.append(node)


def format_cell(cell, text, bold=False):
    cell.text = text
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for paragraph in cell.paragraphs:
        paragraph.alignment = 1
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.paragraph_format.line_spacing = 1.1
        for run in paragraph.runs:
            run.bold = bold
            run.font.name = "Arial"
            run.font.size = Pt(10 if bold else 9.5)


def group_rule(cell):
    """Trim a native paragraph rule inside each parent header cell."""
    properties = cell.paragraphs[0]._p.get_or_add_pPr()
    properties.append(element("ind", left=60, right=60))
    rule = element("pBdr")
    rule.append(element("bottom", val="single", sz=4, color="000000", space=1))
    properties.append(rule)


def math_node(name):
    return OxmlElement("m:" + name)


def math_run(text, upright=False):
    run = math_node("r")
    properties = math_node("rPr")
    style = math_node("sty")
    style.set(qn("m:val"), "b" if upright else "bi")
    properties.append(style)
    run.append(properties)
    fonts = element("rPr")
    fonts.append(element("sz", val=20))
    fonts.append(element("szCs", val=20))
    fonts.append(element("b", val=1))
    run.append(fonts)
    content = math_node("t")
    content.text = text
    run.append(content)
    return run


def metric_heading(cell, base, script, unit, superscript=False):
    format_cell(cell, "", True)
    paragraph = cell.paragraphs[0]
    equation = math_node("oMath")
    structure = math_node("sSup" if superscript else "sSub")
    expression = math_node("e")
    expression.append(math_run(base))
    index = math_node("sup" if superscript else "sub")
    index.append(math_run(script, upright=True))
    structure.extend([expression, index])
    equation.append(structure)
    paragraph._p.append(equation)
    run = paragraph.add_run(" (" + unit + ")")
    run.bold, run.font.size, run.font.name = True, Pt(10), "Arial"


def make_table(document):
    table = document.add_table(rows=6, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [Cm(3.4)] + [Cm(2.6)] * 4
    for column, width in zip(table.columns, widths):
        column.width = width
    for row in table.rows:
        for cell, width in zip(row.cells, widths):
            cell.width = width
    table.cell(0, 0).merge(table.cell(1, 0))
    table.cell(0, 1).merge(table.cell(0, 2))
    format_cell(table.cell(0, 0), "Method", True)
    for index, text in [(1, "Energy use"), (3, "Tracking"), (4, "Actuation")]:
        format_cell(table.cell(0, index), text, True)
        group_rule(table.cell(0, index))
    metric_heading(table.cell(1, 1), "E", "raw", "Wh", True)
    metric_heading(table.cell(1, 2), "E", "adj", "Wh", True)
    metric_heading(table.cell(1, 3), "e", "rms", "a.u.")
    metric_heading(table.cell(1, 4), "Δu", "rms", "a.u.")
    values = [
        ["Method A", "10.0", "0.8", "11.0", "0.9"],
        ["Method B", "9.7", "0.7", "10.5", "0.8"],
        ["Method C", "10.4", "0.9", "10.8", "0.7"],
        ["Method D", "9.9", "0.6", "10.2", "0.8"],
    ]
    for row, record in zip(table.rows[2:], values):
        for cell, text in zip(row.cells, record):
            format_cell(cell, text)
    borders(table._tbl.tblPr, {"top": 12, "bottom": 12})
    for row_index, row in enumerate(table._tbl.tr_lst):
        properties = row.get_or_add_trPr()
        properties.append(element("cantSplit"))
        if row_index < 2:
            properties.append(element("tblHeader"))
        for cell_index, cell in enumerate(row.tc_lst):
            rules = {}
            if row_index == 0:
                rules = {"top": 12, "bottom": 6 if cell_index == 0 else 0}
            if row_index == 1:
                rules = {"bottom": 6}
            if row_index == 5:
                rules = {"bottom": 12}
            borders(cell.get_or_add_tcPr(), rules)
    return table


def build(output):
    document = Document()
    section = document.sections[0]
    section.page_width, section.page_height = Cm(21), Cm(29.7)
    section.top_margin = section.bottom_margin = Cm(2.5)
    section.left_margin = section.right_margin = Cm(2.5)
    normal = document.styles["Normal"]
    normal.font.name, normal.font.size = "Arial", Pt(11)
    normal.paragraph_format.space_after = Pt(8)
    title = document.add_paragraph("Two level table header example")
    title.runs[0].bold = True
    title.runs[0].font.size = Pt(15)
    document.add_paragraph(
        "The first header row names the physical categories. The second gives "
        "the metric symbols and units. Each category has its own short rule."
    )
    caption = document.add_paragraph("Table X. Illustrative metric comparison")
    caption.paragraph_format.keep_with_next = True
    make_table(document)
    document.add_paragraph(
        "Notes. All values are fictional. a.u., arbitrary units; raw, unadjusted; "
        "adj, adjusted; rms, root mean square. Labels and layout are editable."
    )
    properties = document.core_properties
    properties.author = properties.last_modified_by = ""
    properties.title = "Two level table header example"
    properties.subject = "Synthetic academic table template"
    properties.keywords = properties.comments = ""
    document.save(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error("Output already exists. Choose a new filename.")
    if not output.parent.is_dir():
        parser.error("Output parent directory does not exist.")
    build(output)
    print("Created synthetic table example.", flush=True)


if __name__ == "__main__":
    main()
