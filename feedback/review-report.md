# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Umsetzung erfüllt die Muss-Anforderungen: manuelle Korrekturen werden separat und auditierbar persistiert, der lokale API-Flow validiert Konto, Betrag, Datum und Begründung, passende bestätigte Korrekturen werden nur stichtags- und kontogenau verwendet, und beobachtete Banksalden sowie Quelldateien bleiben getrennt erhalten. Die relevanten Regressionstests und API-Tests sind ergänzt. Der GitHub-Branch ist zwei Commits vor main und enthält keine fehlenden Vergleichsänderungen.

## Review-Ergebnis

**Entscheidung: Angenommen**

### Erfüllte Anforderungen

- Die Migration auf Schema-Version 19 legt eine separate Tabelle `manual_balance_corrections` an.
- Die Korrektur enthält Kontoidentität, Integer-Centbetrag, Stichtag, Begründung, Erstellzeitpunkt, Quelle, Kennzeichnung als manuelle Korrektur und Bestätigungsstatus.
- Eine fachlich identische Korrektur ist idempotent; eine abweichende Korrektur für dasselbe Konto und denselben Stichtag wird abgelehnt.
- Der API-Endpunkt `POST /api/balance-corrections` verlangt genau die Pflichtfelder `account_id`, `balance_minor`, `balance_as_of` und `reason`.
- Unbekannte Konten, ungültige Datumswerte, fehlende Begründungen und Nicht-Integer-Centbeträge werden kontrolliert als Client- oder Not-Found-Fehler beantwortet.
- `GET /api/balance-corrections` stellt die gespeicherten Korrekturen einschließlich Kontoidentität und Auditfeldern abrufbar bereit.
- Der Import sucht ausschließlich nach einer bestätigten Korrektur mit passendem Provider, passender Kontonummer und exakt passendem Stichtag.
- Der beobachtete Banksaldo und der lokale Vergleichsanker werden getrennt geführt. Das Manifest weist beide Werte getrennt aus.
- Die archivierte CSV-Datei und ihre Rohfelder werden nicht verändert.
- Ohne passende Korrektur bleibt die bestehende Volksbank-Saldoabweichung ein Validierungsfehler.
- Die Tests decken den Abbruch ohne Korrektur, den erfolgreichen Import mit Korrektur, die Unverändertheit der CSV-Daten, die getrennten Manifestwerte sowie API-Validierung und Idempotenz ab.

### Architektur- und Scope-Prüfung

Die Umsetzung führt eine separate lokale Korrektur-Faktentabelle ein und verändert weder Vorgänge noch bestehende N:M-Verknüpfungen. Es gibt keine echte Banking-Aktion und keine externen Dienstaufrufe in den neuen Tests. Die Änderung bleibt innerhalb des Arbeitspakets.

### Branch- und Vergleichsprüfung

Der Branch ist laut GitHub Compare `ahead` mit zwei Commits und nicht hinter `main`. `missing_from_github_compare` ist leer. Die zusätzlichen GitHub-Änderungen an `banking_dashboard/server.py` und `tests/test_dashboard.py` gehören fachlich zur API-Umsetzung und sind durch den GitHub-Diff nachvollziehbar.

### Optionale Verbesserungen

Die API könnte Stringtypen strenger validieren und konkurrierende Inserts explizit behandeln. Außerdem sollte der Runner künftig sämtliche im GitHub-Compare geänderten Dateien validieren, insbesondere Dashboard-Server und Dashboard-Tests.
