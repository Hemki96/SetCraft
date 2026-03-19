# Shared Schemas

Gemeinsame Schema-Definitionen für API, Services und spätere Worker.

## Python Schemas

Die initialen Pydantic-Modelle für das MVP-Domänenmodell liegen unter:

- `packages/schemas/python/training_plan_schemas/domain_v1.py`

Diese Modelle bilden die Grundlage für:
- Trennung von historischen und generierten Inhalten
- Trennung von Rohdaten (`raw_snapshot`) und normalisierten Feldern
- nachvollziehbare Review- und Validierungsergebnisse
