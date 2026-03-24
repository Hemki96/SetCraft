from __future__ import annotations

import json
from pathlib import Path
from uuid import UUID

from fastapi import HTTPException
from training_plan_schemas.domain_v1 import ApprovalStatus

from app.schemas.exports import ExportCreateRequest, ExportJobResponse, ExportStatus
from app.services.store import STORE, ExportJob

_EXPORT_DIR = Path("/tmp/setcraft-exports")


def _to_response(job: ExportJob) -> ExportJobResponse:
    return ExportJobResponse(
        id=job.id,
        generated_plan_id=job.generated_plan_id,
        export_format=job.export_format,
        status=job.status,
        file_name=job.file_name,
        created_at=job.created_at,
        completed_at=job.completed_at,
        error_message=job.error_message,
    )


def create_export(payload: ExportCreateRequest) -> ExportJobResponse:
    with STORE.lock:
        plan = STORE.generated_plans.get(payload.generated_plan_id)
        if plan is None:
            raise HTTPException(status_code=404, detail="Generated plan not found")
        if plan.approval_status != ApprovalStatus.APPROVED:
            raise HTTPException(status_code=409, detail="Generated plan must be approved before export")

        job_id = STORE.next_uuid()
        job = ExportJob(
            id=job_id,
            generated_plan_id=payload.generated_plan_id,
            export_format=payload.export_format,
            status=ExportStatus.QUEUED,
            file_name=None,
            created_at=STORE.now(),
        )
        STORE.export_jobs[job.id] = job

        job.status = ExportStatus.RUNNING

        _EXPORT_DIR.mkdir(parents=True, exist_ok=True)
        file_name = f"{job.id}.{payload.export_format.value}"
        path = _EXPORT_DIR / file_name

        if payload.export_format.value == "json":
            path.write_text(json.dumps(plan.model_dump(mode="json"), indent=2), encoding="utf-8")
        else:
            path.write_text(str(plan.model_dump(mode="json")), encoding="utf-8")

        job.file_name = file_name
        job.status = ExportStatus.SUCCEEDED
        job.completed_at = STORE.now()
        STORE.export_paths[job.id] = str(path)

        return _to_response(job)


def get_export(export_job_id: UUID) -> ExportJobResponse | None:
    with STORE.lock:
        job = STORE.export_jobs.get(export_job_id)
    if job is None:
        return None
    return _to_response(job)


def get_export_file_path(export_job_id: UUID) -> str | None:
    with STORE.lock:
        return STORE.export_paths.get(export_job_id)
