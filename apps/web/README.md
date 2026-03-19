# Web App

React + TypeScript Scaffold fuer das SetCraft-Frontend.

## Ziele dieses Scaffolds

- Routing-Grundstruktur fuer zentrale MVP-Screens
- Layout-Shell als stabiler App-Rahmen
- Placeholder-Screens fuer Login, Dashboard, Sources, Sessions, Generate
- Optionaler minimaler API-Health-Check im Dashboard

## Start

```bash
cd apps/web
npm install
npm run dev
```

## Verfuegbare Skripte

```bash
npm run dev
npm run typecheck
npm run lint
npm run build
npm run preview
```

## Aktuelle Routen

- `/login`
- `/dashboard`
- `/sources`
- `/sessions`
- `/generate`

## Nicht enthalten

- Fachliche Formularlogik
- API-Fachintegration
- Persistente Zustandsverwaltung
- Authentifizierungs-Backend

## Health-Check (minimal)

- Dashboard prueft den API-Status ueber `GET /api/v1/health`.
- In der lokalen Entwicklung leitet Vite alle `/api/*`-Anfragen per Proxy auf `http://localhost:8000` weiter.
