# Implementation Report

## Branchname

agent2/codex-20260710-080931

## Geaenderte Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py
- feedback/implementation_report.md

## Umgesetzte Punkte

- `DashboardDataStore.list_vorgaenge()` priorisiert serverseitig Vorgaenge mit `status <> 'abgeschlossen'` vor abgeschlossenen Vorgaengen.
- Die bestehende fachliche Reihenfolge innerhalb der Statusgruppen bleibt erhalten: letztes Transaktionsdatum absteigend, danach `aktualisiert_am` absteigend und `vorgangs_id`.
- Die Priorisierung gilt fuer normale Vorgangslisten und Suchtreffer, weil sie direkt in der gemeinsamen SQL-ORDER-BY-Klausel liegt.
- `hide_completed=True` blendet abgeschlossene Vorgaenge weiterhin aus.
- Tests fuer Standardliste, Suche, `hide_completed` und HTTP-API-Verhalten wurden ergaenzt bzw. erweitert.

## Nicht umgesetzte Punkte

- Keine UI-Aenderungen, da die API die Reihenfolge serverseitig liefert.
- Keine Aenderungen an Vorgangsstatus-Regeln oder automatischer Abschlusslogik.
- Keine Aenderung an `feedback/next_task.md`, `feedback/backlog.md`, `feedback/agent2_prompt.md`, `feedback/agent2_review_request.md` oder Review-Report-Dateien.

## Ausgefuehrte Tests

- `"C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_dashboard.py`

## Testergebnis

- `tests/test_dashboard.py`: 87 passed, 4 skipped

## Bekannte Einschraenkungen

- Vier bestehende Dashboard-Tests wurden vom vorhandenen Test-Setup uebersprungen.
- Keine manuellen Browser- oder externen Diensttests ausgefuehrt.

## Hinweise fuer den Review-Agenten

- Die Statuspriorisierung ist als `CASE WHEN v.status = 'abgeschlossen' THEN 1 ELSE 0 END` direkt vor der bisherigen Datumssortierung umgesetzt.
- Der Arbeitsbaum enthielt vor der Umsetzung bereits `feedback/Review-report.md` als geaendert und `feedback/agent2_prompt.md` als untracked; beide wurden nicht bearbeitet.
