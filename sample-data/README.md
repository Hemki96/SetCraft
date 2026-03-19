# Sample Data

Dieses Verzeichnis enthaelt kleine, reproduzierbare Beispieldaten fuer die MVP-Phase.

## Struktur

- `raw/`: Rohquellen (DOCX, PDF, TXT) als Eingaben fuer spaetere Extraktion
- `normalized/`: erwartete normalisierte Zwischenstruktur je Rohquelle
- `expected/`: kompakte Erwartungswerte fuer assertions in Tests

## Konventionen

- Pro Dateityp existiert mindestens ein `clean`- und ein `problematic`-Fall.
- Alle Inhalte sind synthetisch und enthalten keine sensiblen Echtinformationen.
- Problematische Faelle modellieren typische Qualitaetsprobleme (z. B. fehlende Distanz, unklare Intervalle), keine Produktionsdaten.
