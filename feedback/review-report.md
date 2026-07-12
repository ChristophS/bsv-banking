# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die nachgeladenen Dateien bestätigen die vorhandene Schema- und Trigger-Grundlage sowie die 400/404-Fehlerbehandlung. Der Diff implementiert die API vollständig innerhalb der vorgangsbasierten Verknüpfungen und der Branch ist sauber vor main.

## Zusammenfassung

Die GET-/PUT-API für Mail-Dokumentzuordnungen wurde mit strikter Payload- und Kontextvalidierung umgesetzt. Sie verwendet ausschließlich vorgang_belege und transaktion_vorgaenge samt opaker bezugs_id, ohne eine direkte Transaktion-Beleg-Beziehung einzuführen.

# Review Report

## Ergebnis

**Accepted:** ja

## Geprüfter Umfang

- `banking_dashboard/server.py`
- `tests/test_dashboard.py`
- Nachgeladener Kontext aus `transaction_store/database.py`
- GitHub-Compare-Status: Branch ist `ahead` um 2 Commits und nicht hinter `main`.

## Umsetzung

Die neue API ist unter folgendem bestehenden Vorgangsnamensraum abgegrenzt:

- `GET /api/vorgaenge/{vorgangs_id}/mail-dokumentzuordnungen`
- `PUT /api/vorgaenge/{vorgangs_id}/mail-dokumentzuordnungen`

Der lesende Endpunkt liefert den Vorgang, dessen verknüpfte Transaktionen einschließlich lesbarer Transaktionsinformationen, die über `vorgang_belege` verfügbaren Dokumente sowie die aktuell über `vorgangsbezug_id` aufgelösten Transaktionszuordnungen.

Der schreibende Endpunkt validiert:

- den adressierten Vorgang,
- erlaubte Top-Level- und Elementfelder,
- Payload- und URL-Vorgangs-ID auf Widerspruch,
- Typ und Inhalt der Zuordnungsliste,
- Beleg-IDs einschließlich Zugehörigkeit zum Vorgang,
- Transaktions-IDs einschließlich Existenz und Zugehörigkeit zum Vorgang,
- doppelt übermittelte Beleg-IDs.

`ValueError` wird im PUT-Handler als HTTP 400 und `LookupError` als HTTP 404 zurückgegeben. Damit entsprechen die neuen Endpunkte der etablierten Fehlerstruktur.

## Architektur und Persistenz

Die Zuordnung wird nicht als direkte Beziehung zwischen `transactions` und `belege` persistiert. Stattdessen wird ausschließlich `vorgang_belege.vorgangsbezug_id` auf die opake, eindeutige `transaktion_vorgaenge.bezugs_id` gesetzt. Der GET-Endpunkt löst die fachlich benötigte Transaktions-ID erst über den Join im Vorgangskontext auf.

Der nachgeladene Datenbankkontext bestätigt:

- `transaktion_vorgaenge.bezugs_id` wird nachinitialisiert und eindeutig indiziert.
- `vorgang_belege` enthält keine direkte `transaktions_id`-Spalte.
- Der bestehende Löschtrigger leert nur den abhängigen opaken Vorgangsbezug, wenn der zugrunde liegende Transaktion-Vorgang-Link entfernt wird.

Die Anpassung der Link-Ersetzung ist fachlich erforderlich: Unveränderte Transaktion- und Beleglinks werden nicht mehr gelöscht und erneut erstellt. Dadurch bleiben stabile `bezugs_id`-Werte und gespeicherte Dokumentauswahlen bei einem Vorgangs-Update erhalten. Entfernte Transaktionslinks lösen weiterhin den vorgesehenen Trigger zur Bereinigung ihrer Dokumentbezüge aus.

## Tests

Die ergänzten Dashboard-Tests decken erfolgreichen Abruf und Änderung, idempotentes erneutes Speichern, unbekannte Beleg- und Transaktions-IDs, kontextfremde Transaktionen, widersprüchliche Vorgangs-IDs, unbekannte Payload-Felder, die Unverändertheit nach fehlerhaften Requests sowie die Abwesenheit einer direkten `transaktions_id` in `vorgang_belege` ab. Ein weiterer Regressionstest prüft die Erhaltung der auflösbaren Zuordnung nach `update_vorgang`.

Laut Umsetzungsbericht laufen die Dashboard-, Mail- und Transaktionstests lokal ohne produktive Daten oder externe Dienste. Die Änderungen enthalten keine externen Banking-, Mail-, Graph- oder Login-Aktionen.

## Nicht-blockierende Hinweise

- Ein expliziter Test für einen nicht vorhandenen Vorgang würde die Testabdeckung der Anforderung noch vollständiger sichtbar machen.
- Die partielle PUT-Semantik für nicht gesendete Belege sollte für künftige API-Clients dokumentiert werden.
