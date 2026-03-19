# Deployment

## Deployment-Ziele

- lokal startbar
- self-hosted-fähig
- mit geringer Betriebs- und Infrastrukturkomplexität
- reproduzierbar
- sauber trennbar nach Umgebung
- ohne Architekturbruch von lokal zu Server erweiterbar

## Zielarchitektur für Deployment

### Kerncontainer
- `web` – React-Frontend
- `api` – FastAPI-Service
- `worker` – Hintergrundverarbeitung
- `db` – PostgreSQL
- `redis` – Queue/Broker
- optional `ollama` – lokales Modell-Gateway
- optional `proxy` – Reverse Proxy / TLS

## Deployment-Modell im MVP

### Standard
Docker Compose

### Gründe
- einfach lokal und auf kleinem Server nutzbar
- reproduzierbar
- geringe Einstiegshürde
- Services sauber trennbar
- passend für self-hosted Erstbetrieb
