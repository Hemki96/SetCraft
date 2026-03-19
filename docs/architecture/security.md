# Security

## Sicherheitsziele

- Schutz hochgeladener Dateien und strukturierter Trainingsdaten
- Schutz vor unsicheren Dateioperationen
- kontrollierter Zugriff auf schreibende Funktionen
- Nachvollziehbarkeit kritischer Änderungen
- saubere Trennung von Konfiguration und Quellcode
- sichere lokale und serverseitige Standardkonfiguration

## Sicherheitsprinzipien

### 1. Default deny für riskante Operationen
Nur explizit erlaubte Dateitypen, Formate und Aktionen sind zulässig.

### 2. Keine geheimen Werte im Repository
Secrets werden ausschließlich über Umgebungsvariablen oder Secret-Management eingebracht.

### 3. Upload ist untrusted input
Jede Datei und jeder Textinput gilt als nicht vertrauenswürdig.

### 4. Historische Inhalte und generierte Inhalte sind auditierbar
Review, Freigabe und Korrekturen müssen nachvollziehbar sein.

### 5. Least privilege
Das Rollenmodell wird klein, aber restriktiv begonnen.

### 6. Sicherheitslogik gehört nicht ins Frontend
Validierung und Schutzmaßnahmen müssen serverseitig durchgesetzt werden.
