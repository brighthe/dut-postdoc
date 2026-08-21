"""Build the anonymous 1--5 form directly in the official Flat OPC format."""

from __future__ import annotations

import base64
from copy import deepcopy
from pathlib import Path

from lxml import etree


HERE = Path(__file__).resolve().parent
OFFICIAL = Path(r"C:\Users\Administrator\iCloudDrive\博士后-大连理工大学\个人办理材料\基金申报\中国博士后科学基金第80批面上资助\项目信息(1-5 部分).docx")
SOURCE = HERE / "80th-2026-application-draft-完整审阅版.docx"
OUTPUT = HERE / "80th-2026-项目信息(1-5部分)-匿名版.docx"

NS = {
    "pkg": "http://schemas.microsoft.com/office/2006/xmlPackage",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "pr": "http://schemas.openxmlformats.org/package/2006/relationships",
}


def part(root, name: str):
    return root.xpath(f"./pkg:part[@pkg:name='{name}']", namespaces=NS)[0]


def xml_root(package_part):
    return package_part.find("pkg:xmlData", NS)[0]


def cell_text(cell) -> str:
    return "".join(cell.xpath(".//w:t/text()", namespaces=NS))


def field_cell(document, label: str):
    for cell in document.xpath(".//w:tc", namespaces=NS):
        if cell_text(cell).startswith(label):
            return cell
    raise ValueError(f"Official field not found: {label}")


def replace_first_text(cell, value: str) -> None:
    """Replace a single text field while retaining its original run formatting."""
    cell.xpath(".//w:t", namespaces=NS)[0].text = value


def replace_section_body(cell, source_paragraphs) -> None:
    paragraphs = cell.xpath("./w:p", namespaces=NS)
    for paragraph in paragraphs[1:]:
        cell.remove(paragraph)
    for paragraph in source_paragraphs:
        cell.append(deepcopy(paragraph))


def add_figure_part(official_root, source_zip) -> None:
    """Copy Fig. 1 and its relationship, preserving the source paragraph's rId9."""
    relations = xml_root(part(official_root, "/word/_rels/document.xml.rels"))
    if not relations.xpath("./pr:Relationship[@Id='rId9']", namespaces=NS):
        relations.append(etree.Element(
            f"{{{NS['pr']}}}Relationship", Id="rId9",
            Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image",
            Target="media/image1.png",
        ))
    for existing in official_root.xpath("./pkg:part[@pkg:name='/word/media/image1.png']", namespaces=NS):
        official_root.remove(existing)
    media_part = etree.Element(
        f"{{{NS['pkg']}}}part",
        **{
            f"{{{NS['pkg']}}}name": "/word/media/image1.png",
            f"{{{NS['pkg']}}}contentType": "image/png",
        },
    )
    etree.SubElement(media_part, f"{{{NS['pkg']}}}binaryData").text = base64.b64encode(
        source_zip.read("word/media/image1.png")
    ).decode("ascii")
    official_root.append(media_part)


def build() -> None:
    import zipfile

    parser = etree.XMLParser(remove_blank_text=False)
    official = etree.parse(str(OFFICIAL), parser).getroot()
    with zipfile.ZipFile(SOURCE) as source_zip:
        source_document = etree.fromstring(source_zip.read("word/document.xml"), parser)
        source_paragraphs = source_document.xpath(".//w:body/w:p", namespaces=NS)
        document = xml_root(part(official, "/word/document.xml"))

        # The project-title label and its editable value are separate cells.
        title_cell = document.xpath(".//w:tbl/w:tr[1]/w:tc[2]", namespaces=NS)[0]
        replace_first_text(
            title_cell,
            "面向大规模拓扑优化的 PIML Matrix-Free 求解与 GPU 协同加速方法研究",
        )
        # Keep the official "（限5个）" prompt in its own run, and change only
        # the following value run.
        keyword_cell = field_cell(document, "（限5个）")
        keyword_value = keyword_cell.xpath(".//w:r", namespaces=NS)[1].xpath("./w:t", namespaces=NS)[0]
        keyword_value.text = "大规模拓扑优化，问题无关机器学习，Matrix-Free，Krylov 求解，GPU 加速"
        section_headers = [
            ("选题依据", "1. 选题依据"),
            ("研究内容", "2. 研究内容"),
            ("3.研究方案", "3. 研究方案"),
            ("4.特色与创新之处", "4. 特色与创新之处"),
            ("5.研究计划及预期成果", "5. 研究计划及预期成果"),
            ("6.研究基础", "6. 研究基础"),
        ]
        header_indices = []
        for label, prefix in section_headers:
            for idx, p in enumerate(source_paragraphs):
                t = "".join(p.xpath(".//w:t/text()", namespaces=NS)).strip()
                if t.startswith(prefix):
                    header_indices.append((label, idx))
                    break

        sections = {}
        for i in range(len(header_indices) - 1):
            label = header_indices[i][0]
            start_idx = header_indices[i][1] + 1
            end_idx = header_indices[i+1][1]
            sections[label] = range(start_idx, end_idx)

        for label, indices in sections.items():
            replace_section_body(field_cell(document, label), [source_paragraphs[i] for i in indices])
        add_figure_part(official, source_zip)

    OUTPUT.write_bytes(etree.tostring(
        official, encoding="UTF-8", xml_declaration=True, standalone=True, pretty_print=False
    ))


if __name__ == "__main__":
    build()
