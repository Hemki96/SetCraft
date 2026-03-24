from __future__ import annotations

import json
from uuid import UUID

from fastapi import HTTPException
from training_plan_schemas.domain_v1 import SessionApprovalStatus

from app.schemas.exports import ExportCreateRequest, ExportFormat, ExportJobResponse, ExportStatus
from app.services.auth_service import RequestActor
from app.services.store import STORE, ExportJob, seed_placeholder_data


def _build_export_content(generated_plan_id: UUID, export_format: ExportFormat) -> str:
    plan = STORE.generated_plans[generated_plan_id]
    payload = {
        "generated_plan_id": str(plan.id),
        "plan_type": plan.plan_type.value,
        "approval_status": plan.approval_status.value,
        "review_status": plan.review_status.value,
        "content_snapshot": plan.content_snapshot,
    }
    if export_format == ExportFormat.TXT:
        return (
            f"Generated Plan: {payload['generated_plan_id']}\n"
            f"Type: {payload['plan_type']}\n"
            f"Approval: {payload['approval_status']}\n"
            f"Review: {payload['review_status']}\n"
            f"Content: {json.dumps(payload['content_snapshot'], ensure_ascii=True)}\n"
        )
    return json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2)


def create_export_job(payload: ExportCreateRequest, actor: RequestActor) -> ExportJobResponse:
    del actor
    seed_placeholder_data()
    with STORE.lock:
        plan = STORE.generated_plans.get(payload.generated_plan_id)
        if plan is None:
            raise HTTPException(status_code=404, detail="Generated plan not found")

        if plan.approval_status != SessionApprovalStatus.APPROVED:
            raise HTTPException(
                status_code=409,
                detail="Only approved generated plans can be exported",
            )

        export_job_id = STORE.next_uuid()
        file_name = f"generated-plan-{plan.id}.{payload.export_format.value}"
        export_content = _build_export_content(plan.id, payload.export_format)

        export_job = ExportJob(
            id=export_job_id,
            generated_plan_id=plan.id,
            export_format=payload.export_format,
            status=ExportStatus.SUCCEEDED,
            file_name=file_name,
            created_at=STORE.now(),
            completed_at=STORE.now(),
        )
        STORE.export_jobs[export_job_id] = export_job
        STORE.export_paths[export_job_id] = export_content
        return ExportJobResponse.model_validate(export_job)


def get_export_job(export_job_id: UUID) -> ExportJobResponse | None:
    with STORE.lock:
        export_job = STORE.export_jobs.get(export_job_id)
    if export_job is None:
        return None
    return ExportJobResponse.model_validate(export_job)


def get_export_content(export_job_id: UUID) -> tuple[ExportJobResponse, str] | None:
    with STORE.lock:
        export_job = STORE.export_jobs.get(export_job_id)
        export_content = STORE.export_paths.get(export_job_id)
    if export_job is None or export_content is None:
        return None
    return ExportJobResponse.model_validate(export_job), export_content
