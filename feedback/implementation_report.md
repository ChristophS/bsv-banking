# Implementation Report

## Branchname

agent2/codex-20260706-101614

## Geaenderte Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_dashboard.py
- feedback/implementation_report.md

## Umgesetzte Punkte

- `GET /api/termine` unterstuetzt den expliziten Query-Parameter `unassigned_upcoming=true`.
- `DashboardDataStore.list_termine()` filtert damit auf dieselben fachlichen Kriterien wie die Overview-Kennzahl `unassigned_termine`: `status = geplant`, Datum ab heute und keine Zuordnung in `vorgang_termine`.
- Der Klick auf die Overview-Karte `unassigned_termine` aktiviert im Frontend einen eigenen Terminlisten-Filterzustand und laedt die Terminansicht mit `unassigned_upcoming=true`.
- Allgemeine Terminaufrufe und die Karte `upcoming_termine` setzen den Spezialfilter zurueck; bestehende Aufrufe ohne neuen Parameter bleiben unveraendert.
- Automatisierte Tests fuer Store/API-Filter und den UI-nahen Kartenklick wurden ergaenzt.

## Nicht umgesetzte Punkte

- Keine neue sichtbare Terminfilter-UI in `banking_dashboard/static/index.html`, da der neue Zustand minimal im bestehenden Frontend-State gefuehrt wird.
- Keine Ueberarbeitung der bestehenden `beginnt_am`-Zeitlogik.
- Keine Aenderungen am Datenbankschema oder an der Termin-Persistenz.

## Ausgefuehrte Tests

- `"C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_dashboard.py`

## Testergebnis

- `tests/test_dashboard.py`: 76 passed, 4 skipped

## Bekannte Einschraenkungen

- Der neue Filter nutzt wie `overview_counts()` den Datumsteil von `beginnt_am` via `SUBSTR(..., 1, 10)` und wertet keine Uhrzeit innerhalb des heutigen Tages aus.
- Der Spezialfilter ist nicht als eigenes UI-Control sichtbar; er wird ueber den Overview-Kartenpfad gesetzt und bei allgemeinen Terminrouten wieder entfernt.

## Hinweise fuer den Review-Agenten

- Die API-Erweiterung liegt in `banking_dashboard/server.py` bei `DashboardDataStore.list_termine()` und dem GET-Handler fuer `/api/termine`.
- Die Frontend-Verdrahtung liegt in `banking_dashboard/static/app.js` im Overview-Card-Routing und in `loadTermine()`.
- Die relevanten Tests sind `DashboardDataStoreTests.test_list_termine_filters_unassigned_upcoming_termine`, der HTTP-Filterabschnitt in `test_overview_vorgang_and_termine_are_available_over_http` und die Playwright-Pruefung fuer `unassigned_termine`.
- `feedback/Review-report.md` und `feedback/agent2_prompt.md` waren bereits vor der Umsetzung im Arbeitsbaum sichtbar und wurden nicht bearbeitet.
