from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response

from app.schemas.exports import ExportCreateRequest, ExportJobResponse, ExportStatus
from app.services.audit_service import record_audit_event
from app.services.auth_service import RequestActor, get_request_actor
from app.services.exports_service import create_export_job, get_export_content, get_export_job

router = APIRouter()


@router.post("", response_model=ExportJobResponse)
def create_export(
    payload: ExportCreateRequest,
    actor: RequestActor = Depends(get_request_actor),
) -> ExportJobResponse:
    try:
        export_job = create_export_job(payload, actor)
    except HTTPException as exc:
        outcome = "denied" if exc.status_code in {403, 409} else "failed"
        record_audit_event(
            event_type="export",
            action="export.create",
            outcome=outcome,
            actor=actor,
            entity_type="generated_plan",
            entity_id=str(payload.generated_plan_id),
            message=str(exc.detail),
            details={"status_code": exc.status_code},
        )
        raise

    record_audit_event(
        event_type="export",
        action="export.create",
        outcome="success",
        actor=actor,
        entity_type="generated_plan",
        entity_id=str(payload.generated_plan_id),
        message="Export job created",
        details={"export_job_id": str(export_job.id), "format": export_job.export_format.value},
    )
    return export_job


@router.get("/{export_job_id}", response_model=ExportJobResponse)
def get_export(export_job_id: UUID) -> ExportJobResponse:
    export_job = get_export_job(export_job_id)
    if export_job is None:
        raise HTTPException(status_code=404, detail="Export job not found")
    return export_job


@router.get("/{export_job_id}/download")
def download_export(
    export_job_id: UUID,
    actor: RequestActor = Depends(get_request_actor),
) -> Response:
    export_data = get_export_content(export_job_id)
    if export_data is None:
        raise HTTPException(status_code=404, detail="Export job not found")

    export_job, content = export_data
    if export_job.status != ExportStatus.SUCCEEDED:
        raise HTTPException(status_code=409, detail="Export job is not completed yet")

    media_type = "application/json" if export_job.export_format.value == "json" else "text/plain"
    response = Response(content=content, media_type=media_type)
    if export_job.file_name:
        response.headers["Content-Disposition"] = f'attachment; filename="{export_job.file_name}"'

    record_audit_event(
        event_type="export",
        action="export.download",
        outcome="success",
        actor=actor,
        entity_type="export_job",
        entity_id=str(export_job.id),
        message="Export downloaded",
        details={"generated_plan_id": str(export_job.generated_plan_id)},
    )
    return response
