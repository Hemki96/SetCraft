from __future__ import annotations

import json
import logging

from app.services.auth_service import RequestActor
from app.services.store import STORE, AuditEvent

_audit_logger = logging.getLogger("setcraft.audit")


def record_audit_event(
    *,
    event_type: str,
    action: str,
    outcome: str,
    actor: RequestActor,
    entity_type: str,
    entity_id: str,
    message: str,
    details: dict[str, object] | None = None,
) -> AuditEvent:
    event = AuditEvent(
        id=STORE.next_uuid(),
        occurred_at=STORE.now(),
        event_type=event_type,
        action=action,
        outcome=outcome,
        actor_user_id=actor.user_id,
        actor_role=actor.role,
        entity_type=entity_type,
        entity_id=entity_id,
        message=message,
        details=details or {},
    )

    with STORE.lock:
        STORE.audit_events.append(event)

    _audit_logger.info(
        "audit_event %s",
        json.dumps(
            {
                "event_id": str(event.id),
                "event_type": event.event_type,
                "action": event.action,
                "outcome": event.outcome,
                "actor_user_id": event.actor_user_id,
                "actor_role": event.actor_role.value,
                "entity_type": event.entity_type,
                "entity_id": event.entity_id,
            },
            sort_keys=True,
        ),
    )
    return event


def list_audit_events() -> list[AuditEvent]:
    with STORE.lock:
        return list(STORE.audit_events)
