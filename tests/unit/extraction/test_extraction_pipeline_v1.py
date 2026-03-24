from __future__ import annotations

from training_plan_schemas.domain_v1 import SourceType

from services.extraction import SegmentType, extract_from_source


def test_text_source_extracts_structured_segments() -> None:
    content = "Warmup:\n4x100m easy @1:40\nDrills 200m"

    result = extract_from_source(source_type=SourceType.TEXT, content=content)

    assert result.raw_text == content
    assert result.confidence > 0.7
    assert len(result.segments) == 3
    assert result.segments[0].segment_type == SegmentType.BLOCK_HEADER
    assert result.segments[1].segment_type == SegmentType.SET_LINE


def test_pdf_source_with_low_signal_creates_issue() -> None:
    result = extract_from_source(
        source_type=SourceType.PDF,
        content="binary-ish stream no text objects",
    )

    assert any(issue.code == "pdf_low_text_signal" for issue in result.issues)
    assert result.confidence < 0.7


def test_docx_bytes_are_parsed_from_document_xml() -> None:
    from io import BytesIO
    from zipfile import ZipFile

    buffer = BytesIO()
    with ZipFile(buffer, "w") as archive:
        archive.writestr(
            "word/document.xml",
            """
            <w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>
              <w:body>
                <w:p><w:r><w:t>Warmup:</w:t></w:r></w:p>
                <w:p><w:r><w:t>8x50m race pace</w:t></w:r></w:p>
              </w:body>
            </w:document>
            """,
        )

    result = extract_from_source(source_type=SourceType.DOCX, content=buffer.getvalue())

    assert result.raw_text == "Warmup:\n8x50m race pace"
    assert len(result.segments) == 2
    assert result.segments[1].segment_type == SegmentType.SET_LINE
