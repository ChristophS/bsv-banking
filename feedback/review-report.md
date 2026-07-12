# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der nachgeladene Kontext bestätigt die Migrationsreihenfolge, die bestehende Inbox-/Vorgangsarchitektur und die Test-Fixture. Die Umsetzung erfüllt die fachlichen Anforderungen ohne direkte Beleg-Transaktions-Beziehung.

## Zusammenfassung

Akzeptiert: Mail-Dokumente werden über einen opaken Bezug auf bestehende transaktion_vorgaenge-Einträge einem bereits mit dem Vorgang verknüpften Transaktionsbezug zugeordnet. Validierung, idempotentes Speichern, Auslesen und Migration sind vorhanden; die Tests decken den Zwei-Dokumente-/Zwei-Transaktionen-Fall sowie zentrale Fehlerfälle ab.

# Review Report

## Ergebnis

**Accepted:** ja

## Geprüfter Umfang

- Arbeitspaket: vorgangsbasierte Grundlage zur Zuordnung von Mail-Dokumenten zu Transaktionsbezügen
- Maßgeblicher Commit: `31503eb18d720a2ca460793a0f849c367f39cc84`
- Branch-Zustand: `ahead` um 2 Commits, nicht hinter `main`

## Umsetzung

Die Umsetzung ergänzt eine interne Zuordnungsrepräsentation im `InboxMailStore`:

- `assign_document_transaction_reference(...)` prüft Mail, Anhang, Vorgang, Transaktion, Mail-Vorgangs-Verknüpfung, Beleg-Vorgangs-Verknüpfung und die vorhandene Verknüpfung in `transaktion_vorgaenge`.
- In `vorgang_belege` wird keine Transaktions-ID gespeichert. Stattdessen referenziert `vorgangsbezug_id` einen opaken `bezugs_id` der vorhandenen Tabelle `transaktion_vorgaenge`.
- Beim Auslesen wird die Transaktions-ID ausschließlich per Join über den Vorgang und dessen vorhandene Transaktionsverknüpfung aufgelöst.
- Der eindeutige partielle Index auf `(mail_inbox_id, mail_attachment_index)` verhindert mehrere Belegzuordnungen für dasselbe Mail-Dokument und ermöglicht idempotentes Wiederholen derselben Speicherung.
- Der Lösch-Trigger entfernt einen nicht mehr auflösbaren Vorgangsbezug, wenn die zugehörige `transaktion_vorgaenge`-Zeile gelöscht wird.

## Architektur- und Datenintegritätsbewertung

Die vorgangsbasierte Architektur wird eingehalten:

- Es wurde keine direkte Beleg-Transaktions- oder Mail-Anhang-Transaktions-Tabelle eingeführt.
- Die persistierte Dokumentzuordnung enthält keinen Wert aus `transactions.transaction_id`.
- Eine angebotene bzw. gespeicherte Transaktion ist nur über einen existierenden Datensatz in `transaktion_vorgaenge` für den gewählten Vorgang erreichbar.
- Die Migration auf Schema-Version 17 ergänzt die benötigten Spalten, hinterlegt fehlende opake Bezugs-IDs für Bestandsverknüpfungen und entfernt die zuvor beanstandete direkte Spalte `transaktionsbezug_id`, falls sie in einer Version-16-Datenbank vorhanden ist.

## Tests

Die ergänzten Tests verwenden SQLite-Testdaten und lokale Mail-Fixtures. Sie decken insbesondere ab:

- zwei Anhänge derselben Mail,
- zwei unterschiedliche Belege,
- zwei unterschiedliche, mit demselben Vorgang verknüpfte Transaktionen,
- idempotentes Wiederholen einer gültigen Zuordnung,
- unbekannte Mail-Dokumente, Vorgänge und Transaktionen,
- das Fehlen einer direkten Spalte `transaktionsbezug_id`,
- das Auslesen der Transaktions-ID ausschließlich über den opaken Vorgangsbezug,
- das Verhalten nach Entfernen einer `transaktion_vorgaenge`-Verknüpfung.

Der Implementierungsbericht dokumentiert zudem erfolgreiche Testläufe für Mail-Integration, Dashboard und Migrations-/Transaktionstests. Die im Diff sichtbaren Änderungen und der geladene Kontext sind damit konsistent.

## Fazit

Die Akzeptanzkriterien des Teilpakets sind erfüllt. Die Lösung schafft eine auslesbare, serverseitig validierte und idempotente Grundlage für die spätere API- und UI-Umsetzung, ohne die zentrale Vorgangsarchitektur zu umgehen.
