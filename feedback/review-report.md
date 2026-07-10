# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der Diff ist ausreichend aussagekräftig und erfüllt die fachlichen Muss-Anforderungen ohne erkennbare blockierende Probleme.

## Zusammenfassung

Die Umsetzung ergänzt zentrale Datenbankfunktionen zum Lesen und atomaren Ersetzen von Transaktionssplits, erweitert die Detail-API und stellt einen PUT-Endpunkt sowie einen einfachen Split-Editor im Dashboard bereit. Serverseitige Summenvalidierung, positive und negative Beträge, Entfernen leerer Split-Listen und Tests sind abgedeckt; der Branch-Zustand ist sauber.

## Review-Ergebnis

**Accepted: true**

Die Umsetzung erfüllt das Arbeitspaket „Split-Grundlagen im Dashboard sichtbar und validierbar machen“ fachlich und technisch.

## Geprüfte Anforderungen

- `transaction_store.database.list_transaction_splits()` lädt Splits einer Transaktion in stabiler Reihenfolge über `ORDER BY created_at, rowid`.
- `transaction_store.database.replace_transaction_splits()` ersetzt Split-Listen zentral und atomar per SQLite-Savepoint.
- Nicht-leere Split-Listen werden vor dem Löschen/Ersetzen exakt gegen `transactions.amount_minor` validiert. Dadurch funktionieren positive und negative Transaktionsbeträge korrekt, solange die Split-Beträge entsprechend vorzeichenrichtig summieren.
- Leere Split-Listen sind erlaubt und entfernen vorhandene Splits vollständig.
- Die Transaktionsdetail-API serialisiert vorhandene Splits inklusive Betrag, Beschreibung, Klassifikationsfeldern, optionaler `vorgangs_id` sowie Zeitstempeln.
- Der neue Endpunkt `PUT /api/transactions/<id>/splits` speichert Split-Listen und liefert für Summenfehler `400` sowie für unbekannte Transaktionen `404`.
- Das Frontend ergänzt in der Detailansicht einen einfachen bearbeitbaren Split-Bereich mit Hinzufügen, Entfernen, Bearbeiten und Speichern von Split-Zeilen.
- Die Differenz zur Originaltransaktion wird sichtbar gemacht und der Speichern-Button bei nicht ausgeglichener nicht-leerer Split-Liste deaktiviert.
- Es wurden keine neuen Tabellen eingeführt; die bestehende Tabelle `transaction_splits` wird genutzt.
- Bestehende Ansichten für Transaktionen ohne Splits bleiben durch leere Split-Listen kompatibel.

## Tests und Branch-Zustand

Der Implementation Report dokumentiert erfolgreiche Läufe von:

- `pytest tests/test_dashboard.py`
- `pytest tests/test_transactions.py`
- `node --check banking_dashboard/static/app.js`

Der GitHub-Compare ist sauber: `ahead_by=1`, `behind_by=0`, keine Abweichungen zwischen Runner- und GitHub-Dateiliste.

## Nicht-blockierende Hinweise

- Der Payload-Parser erwartet exakt `{ "splits": [...] }`. Das ist für den implementierten Client ausreichend, könnte aber bei nicht-Objekt-Payloads oder zusätzlichen Feldern klarer mit `400 Bad Request` reagieren.
- Wenn ein Client fremde oder doppelte `split_id`-Werte mitsendet, kann das aktuell in einen Datenbankfehler laufen. Langfristig wäre eine explizite Validierung oder serverseitige ID-Neuvergabe robuster.
- Die Frontend-Betragsparser-Logik behandelt nicht parsebare Eingaben als `0`. Eine direkte Feldvalidierung wäre nutzerfreundlicher, ist aber durch die serverseitige Summenprüfung nicht kritisch.
