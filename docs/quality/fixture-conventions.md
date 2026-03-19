# Fixture- und Testdatenkonventionen

Diese Konventionen definieren, wie Rohdaten- und Erwartungsfixtures fuer den Importpfad gepflegt werden.

## Ziel

- kleine, verstaendliche und reproduzierbare Beispiele
- Trennung von Eingabe (`raw`) und erwarteter Struktur (`normalized`/`expected`)
- explizite Abdeckung von robusten und fehleranfaelligen Faellen

## Pflichtabdeckung

- je Dateityp (`DOCX`, `PDF`, `TXT`) mindestens ein sauberer und ein problematischer Fall
- fuer jeden Fall ein Eintrag im `tests/fixtures/fixture-manifest.json`
- fuer jeden Fall zugehoerige Dateien in:
  - `sample-data/raw/`
  - `sample-data/normalized/`
  - `sample-data/expected/`

## Daten- und Sicherheitsvorgaben

- nur synthetische Testdaten
- keine Namen echter Personen, Vereine oder sensibler Leistungsdaten
- keine eingebetteten Secrets, Tokens oder Zugangsdaten

## Namenskonvention

- Dateinamen klein und sprechend, z. B. `session_clean.*` oder `session_problematic.*`
- IDs im Manifest stabil halten, damit Tests nicht bei jeder Aenderung umbenannt werden muessen
