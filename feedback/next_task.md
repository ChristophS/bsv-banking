# Nächstes Arbeitspaket

## Titel

Expliziten Migrationstest für Schema-Version 13 auf 14 ergänzen

## Ziel

Die Migration von Schema-Version 13 auf 14 mit einem gezielten Test absichern, damit die neue Tabelle `transaction_splits` bei bestehenden Datenbanken korrekt angelegt wird und die erwartete Struktur verfügbar ist.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- tests/test_transactions.py: neuen Testfall für die Migration einer bestehenden v13-Datenbank auf v14 ergänzen
- transaction_store/database.py: nur als Referenz für die bestehende Migration und Tabellendefinition; voraussichtlich keine Änderung nötig
- transaction_store/models.py: nur als Referenz für die erwarteten Spalten der Split-Tabellenstruktur

## Muss umgesetzt werden

- Einen automatisierten Test ergänzen, der eine Datenbank im Zustand von Schema-Version 13 simuliert und anschließend die normale Initialisierungs- bzw. Öffnungslogik ausführt.
- Im Test verifizieren, dass `schema_info.version` nach der Migration auf 14 steht.
- Im Test verifizieren, dass die Tabelle `transaction_splits` existiert.
- Im Test verifizieren, dass die erwarteten Spalten vorhanden sind, insbesondere `split_id`, `transaction_id`, `amount_minor`, `description`, `transaction_type`, `top_category`, `sub_category`, `sphere`, `professional_description`, `vorgangs_id`, `created_at`, `updated_at`.
- Im Test verifizieren, dass die wesentlichen Beziehungen nutzbar sind, mindestens per `PRAGMA foreign_key_list(transaction_splits)` für `transaction_id` und `vorgangs_id`.
- Falls die bestehende Teststruktur es erlaubt, prüfen, dass die Migration auf einer befüllten v13-Datenbank vorhandene Daten nicht zerstört.

## Soll umgesetzt werden

- Zusätzlich einen kleinen Assert auf den Index `idx_transaction_splits_transaction_id` ergänzen, wenn das im Teststil des Repos üblich ist.
- Vorhandene Hilfsfunktionen für PRAGMA-Abfragen wiederverwenden, falls sie in `tests/test_transactions.py` oder verwandten Tests bereits existieren.

## Nicht Teil dieses Arbeitspakets

- UI zum Anzeigen oder Bearbeiten von Splits
- API-Endpunkte für Splits
- Kompletter Bearbeitungsworkflow für Transaktions-Splitting
- Fachliche Entscheidung, ob `created_at` und `updated_at` anders modelliert werden sollen
- Änderungen an Mail-/Dokumenten-Zuordnungen
- Neue Architektur für Splits

## Akzeptanzkriterien

- Ein Test schlägt fehl, wenn eine v13-Datenbank nicht auf v14 migriert oder `transaction_splits` nicht korrekt angelegt wird.
- Der Test läuft im bestehenden Test-Setup mit `python -m unittest discover -s tests -v`.
- Nach der Migration sind die Kernobjekte weiterhin vorhanden und die neue Split-Tabelle entspricht der im Code erwarteten Struktur.

## Hinweise für den Umsetzungs-Agenten

- Der Test sollte möglichst einen echten Altzustand nachbilden und nicht nur gegen die aktuelle Schemaerzeugung prüfen.
- Da `_initialize_schema` migrationsgesteuert anhand von `schema_info.version` arbeitet, ist ein temporäres SQLite-File mit vorbereiteter v13-Struktur wahrscheinlich der passendste Weg.
- Die Split-Tabelle wird nicht über die normalisierte View abgebildet; deshalb direkt per `PRAGMA table_info(transaction_splits)` und ggf. `PRAGMA foreign_key_list(transaction_splits)` prüfen.
- Die bestehenden Funktionen `list_transaction_splits` und `replace_transaction_splits` zeigen, welche Spalten die aktuelle Implementierung erwartet.

## Manuelle Testhinweise

- Optional lokal eine temporäre Datenbank mit Schema-Version 13 erzeugen und anschließend über die normale Öffnungslogik laden.
- Danach per SQLite-Inspektion prüfen, dass `transaction_splits` vorhanden ist und die erwarteten Spalten trägt.

## Offene Fragen

- Falls in `tests/test_transactions.py` bereits ein etabliertes Muster für historische Schema-Migrationen existiert, sollte dieses exakt wiederverwendet werden.
