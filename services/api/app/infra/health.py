from __future__ import annotations

from app.infra.db.session import ping_database


class SqlalchemyDatabaseProbe:
    def is_reachable(self) -> bool:
        try:
            return ping_database()
        except Exception:
            return False

