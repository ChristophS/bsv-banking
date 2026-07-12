# Implementation Report

## Branchname

`agent2/codex-20260712-155339`

## Geänderte Dateien

- `transaction_store/database.py`
- `transaction_store/models.py`
- `transaction_store/pipeline.py`
- `banking_dashboard/server.py`
- `tests/test_transactions.py`
- `tests/test_dashboard.py`
- `feedback/implementation_report.md`

## Umgesetzte Punkte

- SQLite-Schema auf Version 19 erweitert und separate Tabelle `manual_balance_corrections` mit Konto, Integer-Centsaldo, Stichtag, Begründung, Erstellzeitpunkt, Quelle, manueller Kennzeichnung und Bestätigungsstatus ergänzt.
- Validierte Persistenzfunktionen für Anlage, Liste und stichtagsgenaue Suche umgesetzt.
- Doppelte fachlich identische Korrekturen werden idempotent beantwortet; abweichende parallele Korrekturen für dasselbe Konto und denselben Stichtag werden abgelehnt.
- Lokale API `GET/POST /api/balance-corrections` ergänzt. Unvollständige Daten, Nicht-Integer-Centwerte, ungültige Daten und unbekannte Konten führen zu kontrollierten 4xx-Antworten.
- Der Import verwendet ausschließlich eine bestätigte Korrektur mit exakt passendem Provider, Konto und Stichtag als lokalen Saldoanker.
- Der beobachtete Banksaldo bleibt unverändert und wird neben dem verwendeten Korrekturanker im Importmanifest ausgewiesen. CSV-Datei und Rohfelder werden nicht verändert.
- Ohne passende Korrektur bleibt die bestehende Volksbank-Saldoabweichung ein reproduzierbarer Parser-/Validierungsfehler.
- API-Antworten enthalten Kontoidentität, Betrag, Stichtag, Begründung, Auditfelder und einen Nutzungshinweis zur manuellen Prüfung.

## Nicht umgesetzte Punkte

- Keine Oberfläche, Widerrufs-/Ersetzungsfunktion oder Mehrrollenfreigabe; laut Arbeitspaket nicht Bestandteil.
- Keine zeitlich fortwirkenden Korrekturen. Wegen der offenen fachlichen Frage wurde die kleinste sichere Variante gewählt: Ein Anker gilt nur für den exakten Exportstichtag.

## Ausgeführte Tests

- `"C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m py_compile transaction_store/database.py transaction_store/models.py transaction_store/pipeline.py banking_dashboard/server.py`
- `"C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_transactions.py::TransactionPipelineTests::test_matching_manual_balance_correction_unblocks_snapshot_without_changing_raw_data tests/test_dashboard.py::DashboardHTTPTests::test_balance_correction_api_validates_persists_and_is_idempotent`
- `"C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_transactions.py tests/test_dashboard.py`

## Testergebnis

- Syntaxprüfung erfolgreich.
- Gezielte neue Regressionstests: 2 bestanden.
- Vollständige relevante Tests: 157 bestanden, 6 übersprungen.
- Die übersprungenen Tests sind vorhandene optionale Browser-/Playwright-Tests; es wurden keine externen Dienste aufgerufen.

## Bekannte Einschränkungen

- Ein Konto muss bereits lokal in `accounts` existieren, bevor über die API ein Korrekturanker angelegt werden kann.
- Eine bestehende Korrektur kann derzeit weder widerrufen noch ersetzt werden.
- API und Audittexte verwenden aus Kompatibilitätsgründen teilweise ASCII-Umschriften in Fehlermeldungen.

## Hinweise für den Review-Agenten

- Besonders prüfen: Migration 18 → 19, Unique-Constraint `(account_id, balance_as_of)` und stichtagsgenaue Auswahl in `manual_balance_correction_for`.
- Der Regressionstest simuliert zuerst den unveränderten Fehler mit einem Bankanker von 200,00 EUR und importiert anschließend mit einem bestätigten lokalen Anker von 100,00 EUR. Er prüft zusätzlich die unveränderte CSV-Zeile und die getrennten Manifestwerte.
- Bereits vorhandene fremde Worktree-Änderungen an `feedback/Review-report.md` und die unversionierte Datei `feedback/agent2_prompt.md` wurden nicht verändert.
