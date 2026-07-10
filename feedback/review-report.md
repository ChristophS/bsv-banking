# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der maßgebliche GitHub-Diff erfüllt die Muss-Anforderungen: Split-Read/Write-API ist angebunden, die kanonischen Modellfelder werden serialisiert/akzeptiert, die UI zeigt und speichert Splits inklusive Reload nach erfolgreichem Speichern, und Tests decken Roundtrip sowie Fehlerfall ab.

## Zusammenfassung

Die Dashboard-Anbindung für transaction_splits wurde fachlich passend umgesetzt. API, UI und Tests bilden den vorhandenen Persistenz-Roundtrip ab; Summenvalidierung bleibt bei replace_transaction_splits. Es gibt keine blockierenden Befunde.

# Review Report

## Ergebnis

**Accepted:** true

## Geprüfter Umfang

Geprüft wurden die Anforderungen aus dem Arbeitspaket gegen den GitHub-Diff und den nachgeladenen Kontext zu Server, Frontend, Persistenzmodell und Tests.

## Umsetzung

Die Umsetzung bindet die vorhandene `transaction_splits`-Persistenz im Dashboard an:

- `GET /api/transactions/<id>/splits` liest Splits einer Transaktion über `list_transaction_splits()` und liefert einen stabilen JSON-Zustand.
- `PUT /api/transactions/<id>/splits` war im bestehenden Kontext bereits vorhanden und nutzt weiterhin `replace_transaction_splits()` für das vollständige Ersetzen inklusive zentraler Summenvalidierung und Atomarität.
- Die Split-Serialisierung wurde um die geforderten kanonischen Modellfelder ergänzt: `transaction_id`, `amount_minor`, `description`, `transaction_type`, `top_category`, `sub_category`, `sphere`, `professional_description`, `created_at`, `updated_at`; `split_id` und `vorgangs_id` bleiben enthalten.
- Das Payload-Mapping akzeptiert nun neben den bisherigen deutschen Alias-Feldern auch die kanonischen Modellfeldnamen.
- Das Frontend liest beide Feldfamilien, sendet beim Speichern kanonische Felder, zeigt Split-ID und Zeitstempel an und baut den Detailzustand nach erfolgreichem Speichern aus der Serverantwort neu auf.
- Die bestehende Backend-Validierung der Split-Summe wird nicht dupliziert oder widersprüchlich ersetzt; die UI verhindert zusätzlich nicht ausgeglichene nicht-leere Split-Listen und zeigt den Summenstatus verständlich an.
- Tests in `tests/test_dashboard.py` decken Detail-Serialisierung, direkten Split-GET-Endpunkt, erfolgreichen Write-Roundtrip und ungültige Summen mit unveränderter Persistenz ab. Bestehende Persistenztests in `tests/test_transactions.py` sichern den Store-Roundtrip und die Atomarität ab.

## Bewertung gegen Akzeptanzkriterien

- Leerer Split-Zustand: erfüllt über `transaction_detail`/UI-Abschnitt und stabil leere Liste.
- Vorhandene Splits sichtbar: erfüllt inklusive der geforderten Felder und Metadaten.
- Gültige Split-Liste speichern und wieder ausliefern: erfüllt über `PUT` mit anschließendem Detail-Reload aus der Serverantwort.
- Ungültige Split-Summe ohne Teilpersistenz: erfüllt durch `replace_transaction_splits()`; HTTP-Test prüft 400 und unveränderte Splits.
- Persistenzregeln bleiben zentral: erfüllt, keine widersprüchliche Backend-Validierung im Dashboard-Code erkennbar.
- Automatisierte Tests: erfüllt.

## Hinweise

Der nachgeladene `additional_repo_context` für einige geänderte Dateien wirkt teilweise nicht auf dem gleichen Stand wie der GitHub-Diff. Da der GitHub-Diff als maßgebliche Quelle gilt und die Kontextausschnitte ausreichen, um die Einbettung zu bewerten, blockiert dies die Entscheidung nicht.

## Blockierende Probleme

Keine.

## Nicht-blockierende Vorschläge

- Einen expliziten API-Test für `GET /api/transactions/<id>/splits` bei einer Transaktion ohne Splits ergänzen.
- Den UI-Leerzustand optional mit einem klaren Text wie „Noch keine Splits erfasst“ im Split-Editor selbst anzeigen.
