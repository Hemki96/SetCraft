# Tech Stack

## Stack-Übersicht

## Backend
- **Python 3.12+**
- **FastAPI**
- **Pydantic**
- **SQLAlchemy** oder **SQLModel**
- **Alembic**

## Datenhaltung
- **PostgreSQL**
- **pgvector**

## Hintergrundverarbeitung
- **Celery** oder **RQ**
- **Redis**

## Frontend
- **React**
- **TypeScript**
- **Vite**
- optional: **TanStack Query**, **React Hook Form**, **Zod**

## Dokumentverarbeitung
- **python-docx** für DOCX-Export/-Hilfslogik
- **PyMuPDF** oder ähnliche PDF-Extraktion
- optional: **Tesseract OCR** als Fallback

## KI / lokale Modelle
- **Ollama** als lokales Modell-Gateway
- lokales Embedding-Modell über Ollama oder alternative austauschbare Adapter

## Test & Qualität
- **pytest**
- **ruff**
- **mypy**
- **pre-commit**
- Frontend: **Vitest**, **Playwright**

## Betrieb / Infrastruktur
- **Docker**
- **Docker Compose**
- optional später: **Traefik** oder **Nginx**
