# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die Umsetzung erfüllt die Anforderungen an Persistenz, Laden/Speichern, Summenvalidierung, unbekannte Transaktionen, API-Erweiterung und Tests; der Branch-Zustand ist sauber.

## Zusammenfassung

Die bestehende Split-Grundlage wurde um eine explizite stabile Reihenfolge ergänzt und Schema, Migration, Modelle, Serialisierung, Persistenzlogik sowie API-/Persistenztests wurden passend angepasst. Die Akzeptanzkriterien sind fachlich erfüllt; es gibt keine blockierenden Probleme.

# Review Report

## Ergebnis

**Accepted:** true

## Prüfung gegen das Arbeitspaket

Die Umsetzung erfüllt die geforderte Split-Grundlage für Transaktionen.

### Datenmodell und Migration

- `transaction_splits` erhält mit `sort_order` eine explizite Reihenfolgespalte.
- Die Schema-Version wird von 14 auf 15 angehoben.
- Die Migration `v14 -> v15` ergänzt die Spalte für bestehende Tabellen und backfillt vorhandene Split-Zeilen aus der bisherigen SQLite-Reihenfolge.
- Ein zusätzlicher Index auf `(transaction_id, sort_order)` unterstützt das stabile Laden pro Transaktion.
- Die bestehende Kopplung an `transactions(transaction_id)` bleibt erhalten; es wird keine neue zentrale Fachentität neben Vorgängen/Transaktionen eingeführt.

### Persistenzlogik

- `list_transaction_splits` lädt Splits stabil nach `sort_order, created_at, rowid`.
- `replace_transaction_splits` ersetzt die Splits weiterhin atomar über einen Savepoint.
- Beim Ersetzen wird die Reihenfolge aus der eingereichten Liste abgeleitet.
- Die bestehende Validierung gegen unbekannte Transaktionen und gegen abweichende Split-Summen bleibt erhalten.
- Leere Split-Listen bleiben möglich, wodurch Splits vollständig entfernt werden können; das ist mit dem Hinweis vereinbar, keine künstlichen Default-Splits anzulegen.

### API und Serialisierung

- Die Split-Serialisierung liefert nun `sort_order` sowie das deutsche Aliasfeld `reihenfolge` aus.
- Der Payload-Parser setzt die Reihenfolge aus der Listensequenz.
- Die bestehende kleine Read/Write-API für `/api/transactions/<id>/splits` bleibt passend zum Arbeitspaket.

### Tests

- Die Tests wurden um Schema-/Migrationsprüfung für `sort_order`, stabile Reihenfolge beim Speichern/Laden und API-Antworten ergänzt.
- Laut Implementation Report wurden `tests/test_transactions.py` und `tests/test_dashboard.py` erfolgreich ausgeführt.

### Branch-/Compare-Zustand

- `compare_status`: `ahead`
- `ahead_by`: 1
- `behind_by`: 0
- `total_commits`: 1
- Keine Abweichungen zwischen Runner- und GitHub-Compare-Dateien.

## Hinweise

Die nachgeladene `additional_repo_context` wirkte an einzelnen Stellen wie ein Stand vor Anwendung des Diffs. Da der GitHub-Diff laut Review-Regeln maßgeblich ist und die Änderungen dort konsistent sowie ausreichend prüfbar sind, blockiert das die Entscheidung nicht.

## Blockierende Probleme

Keine.
