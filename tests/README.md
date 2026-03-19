# Tests

Dieses Verzeichnis ist für Test-Suites vorgesehen:
- Unit-Tests
- Integrationstests
- spätere E2E-Tests

Die Ausführung erfolgt über die im Repository definierten Make-Targets:
- `make test`
- `make test-unit`
- `make test-int`

## Integration: DB-Smoke-Test

Für den DB-Smoke-Test wird eine erreichbare PostgreSQL-Instanz benötigt.

- Setze `TEST_DATABASE_URL` (oder alternativ `DATABASE_URL`)
- Führe Migrationen über Alembic aus (im Test automatisch `upgrade head`)
- Starte anschließend den Integrationstest:

```bash
pytest tests/integration/test_db_smoke.py
```
