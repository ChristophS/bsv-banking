# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der Diff ist ausreichend aussagekräftig; der neue Test deckt die geforderten Migrationsaspekte für Schema-Version 13 auf 14 fachlich ab.

## Zusammenfassung

Akzeptiert: Es wurde ein gezielter unittest für die Migration von Schema-Version 13 auf 14 ergänzt, der Versionserhöhung, Existenz und Spalten der Tabelle transaction_splits, Foreign Keys, Index sowie Erhalt bestehender Kernobjekte prüft.

## Review-Ergebnis

**Entscheidung:** Accepted

## Geprüfte Anforderungen

- Es wurde ein automatisierter Test in `tests/test_transactions.py` ergänzt.
- Der Test erzeugt eine temporäre SQLite-Datenbank, befüllt sie mit Account, Transaktion, Vorgang und Transaktion-Vorgang-Verknüpfung, entfernt anschließend `transaction_splits` und setzt `schema_info.version` auf `13`.
- Danach wird die normale Öffnungs-/Initialisierungslogik über `connect_database(path)` erneut ausgeführt.
- Der Test prüft, dass `schema_info.version` nach der Migration auf `14` steht.
- Der Test prüft, dass `transaction_splits` existiert.
- Der Test prüft die erwarteten Spalten einschließlich `split_id`, `transaction_id`, `amount_minor`, `description`, `transaction_type`, `top_category`, `sub_category`, `sphere`, `professional_description`, `vorgangs_id`, `created_at` und `updated_at`.
- Der Test prüft per `PRAGMA foreign_key_list(transaction_splits)` die Beziehungen für `transaction_id` zu `transactions(transaction_id)` und `vorgangs_id` zu `vorgaenge(vorgangs_id)`.
- Der Soll-Punkt zum Index `idx_transaction_splits_transaction_id` wurde ebenfalls umgesetzt.
- Der Test prüft zusätzlich, dass bestehende Kernobjekte nach der Migration erhalten bleiben.

## Technische Bewertung

Die Änderung ist auf den erwarteten Scope beschränkt: Es wurde nur ein Test ergänzt, keine Produktivlogik, keine UI, keine externen Dienste und keine fachfremden Umbauten. Der Branch-Zustand ist laut Compare sauber (`ahead_by=1`, `behind_by=0`, keine Abweichungen zwischen Runner und GitHub Compare).

Der Ansatz, den v13-Zustand aus einer aktuellen Testdatenbank abzuleiten, `transaction_splits` zu entfernen und die Version zurückzusetzen, ist für das konkrete Ziel ausreichend: Der Test schlägt fehl, wenn die Migration die Split-Tabelle nicht erstellt, die Version nicht anhebt oder die erwartete Struktur nicht bereitstellt.

## Blockierende Probleme

Keine.

## Nicht-blockierende Hinweise

- Eine noch historisch exaktere v13-Testfixture könnte langfristig sinnvoll sein, ist aber für dieses Arbeitspaket nicht erforderlich.
