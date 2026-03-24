from __future__ import annotations

import re
import zipfile
from io import BytesIO
from typing import Iterable
from xml.etree import ElementTree

from training_plan_schemas.domain_v1 import SourceType

from .models import ExtractedSegment, ExtractionIssue, ExtractionOutput, SegmentType

_SET_TOKEN_PATTERN = re.compile(r"(\d+\s*[x×]\s*\d+|\b\d{2,5}\s*m\b)", re.IGNORECASE)


def _normalize_lines(text: str) -> list[tuple[int, str]]:
    return [
        (line_index + 1, line.strip())
        for line_index, line in enumerate(text.splitlines())
        if line.strip()
    ]


def _classify_segment(line: str) -> SegmentType:
    lowered = line.lower()
    if line.endswith(":") or lowered in {"warmup", "hauptsatz", "cooldown"}:
        return SegmentType.BLOCK_HEADER
    if _SET_TOKEN_PATTERN.search(line):
        return SegmentType.SET_LINE
    return SegmentType.FREE_TEXT


def _parse_docx_bytes(content: bytes) -> tuple[str, list[ExtractionIssue]]:
    issues: list[ExtractionIssue] = []
    try:
        with zipfile.ZipFile(BytesIO(content)) as zf:
            xml_bytes = zf.read("word/document.xml")
    except (KeyError, zipfile.BadZipFile):
        return "", [
            ExtractionIssue(
                code="docx_parse_failed",
                message=(
                    "DOCX content could not be parsed; "
                    "falling back to generic text extraction."
                ),
                confidence_impact=0.25,
            )
        ]

    root = ElementTree.fromstring(xml_bytes)
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", namespace):
        texts = [node.text or "" for node in paragraph.findall(".//w:t", namespace)]
        joined = "".join(texts).strip()
        if joined:
            paragraphs.append(joined)

    if not paragraphs:
        issues.append(
            ExtractionIssue(
                code="docx_no_text",
                message="DOCX parsed successfully but no text nodes were found.",
                confidence_impact=0.2,
            )
        )

    return "\n".join(paragraphs), issues


def _parse_pdf_content(content: str) -> tuple[str, list[ExtractionIssue]]:
    issues: list[ExtractionIssue] = []
    extracted_tokens = re.findall(r"\(([^\)]{1,200})\)", content)
    cleaned_tokens = [token.strip() for token in extracted_tokens if token.strip()]

    if not cleaned_tokens:
        issues.append(
            ExtractionIssue(
                code="pdf_low_text_signal",
                message="PDF content had low text signal; extracted lines may be incomplete.",
                confidence_impact=0.3,
            )
        )
        return content, issues

    return "\n".join(cleaned_tokens), issues


def _decode_content(content: str | bytes) -> tuple[str, list[ExtractionIssue]]:
    if isinstance(content, str):
        return content, []

    try:
        return content.decode("utf-8"), []
    except UnicodeDecodeError:
        return content.decode("latin-1", errors="ignore"), [
            ExtractionIssue(
                code="binary_decode_fallback",
                message="Binary source required latin-1 fallback decode.",
                confidence_impact=0.2,
            )
        ]


def _materialize_segments(
    lines: Iterable[tuple[int, str]],
    *,
    base_confidence: float,
) -> tuple[list[ExtractedSegment], list[ExtractionIssue]]:
    segments: list[ExtractedSegment] = []
    issues: list[ExtractionIssue] = []

    for order_index, (source_line, line) in enumerate(lines):
        segment_type = _classify_segment(line)
        segment_issues: list[ExtractionIssue] = []
        confidence = base_confidence

        if segment_type == SegmentType.FREE_TEXT and len(line.split()) <= 2:
            issue = ExtractionIssue(
                code="low_information_segment",
                message="Segment has very little structure and may require manual review.",
                segment_index=order_index,
                confidence_impact=0.1,
            )
            segment_issues.append(issue)
            issues.append(issue)
            confidence -= issue.confidence_impact

        segments.append(
            ExtractedSegment(
                order_index=order_index,
                text=line,
                segment_type=segment_type,
                confidence=max(0.0, min(1.0, confidence)),
                source_line=source_line,
                issues=segment_issues,
            )
        )

    if not segments:
        issues.append(
            ExtractionIssue(
                code="empty_extraction",
                message="Source produced no non-empty segments.",
                confidence_impact=0.5,
            )
        )

    return segments, issues


def extract_from_source(*, source_type: SourceType, content: str | bytes) -> ExtractionOutput:
    decoded, decode_issues = _decode_content(content)
    parser_issues: list[ExtractionIssue] = []

    if source_type == SourceType.DOCX and isinstance(content, bytes):
        docx_text, parser_issues = _parse_docx_bytes(content)
        working_text = docx_text or decoded
    elif source_type == SourceType.PDF:
        parsed_pdf_text, parser_issues = _parse_pdf_content(decoded)
        working_text = parsed_pdf_text
    else:
        working_text = decoded

    normalized_text = working_text.strip()
    line_items = _normalize_lines(normalized_text)

    base_confidence = {
        SourceType.TEXT: 0.95,
        SourceType.DOCX: 0.85,
        SourceType.PDF: 0.7,
    }[source_type]

    segments, segment_issues = _materialize_segments(line_items, base_confidence=base_confidence)
    issues = [*decode_issues, *parser_issues, *segment_issues]

    confidence = base_confidence - sum(issue.confidence_impact for issue in issues)
    confidence = max(0.0, min(1.0, confidence))

    return ExtractionOutput(
        source_type=source_type,
        raw_text=normalized_text,
        segments=segments,
        confidence=confidence,
        issues=issues,
        trace={
            "segment_count": len(segments),
            "issue_count": len(issues),
            "parser": source_type.value,
        },
    )
