# Fixture-Konventionen

`tests/fixtures/fixture-manifest.json` beschreibt alle Fixture-Faelle zentral.

## Aufbau eines Falls

Jeder Fall hat:

- `id`: stabile, testbare Fall-ID
- `source_type`: `docx`, `pdf` oder `text`
- `quality`: `clean` oder `problematic`
- `raw_file`: Pfad zur Eingabedatei in `sample-data/raw/`
- `normalized_file`: Pfad zur erwarteten Normalform in `sample-data/normalized/`
- `expected_file`: Pfad zur assertbaren Erwartung in `sample-data/expected/`

## Nutzungsziel in Tests

- Unit-Tests: Strukturannahmen und Feldpflichten gegen `normalized`/`expected` pruefen
- Integrationstests: spaeter echte Extraktion/Normalisierung gegen dieselben Fixtures laufen lassen

## Sicherheitsregel

Die Fixtures enthalten ausschliesslich synthetische Trainingsbeispiele ohne personenbezogene oder sensible Daten.
