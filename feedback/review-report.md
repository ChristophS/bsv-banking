# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die geladenen API- und Testdateien reichen für die finale Prüfung aus. Der GitHub-Compare ist mit einem Commit vor main und ohne Abweichungen zum Runner verwendbar.

## Zusammenfassung

Die Vorgangsdetailansicht lädt und bearbeitet Mail-Dokumentzuordnungen über die bestehenden Endpunkte. Die Auswahl ist auf Transaktionen des aktuellen Vorgangs begrenzt, unterstützt die explizite Aufhebung und lädt nach erfolgreichem Speichern konsistent neu.

# Review

## Ergebnis

**Freigegeben.**

## Prüfung der Anforderungen

- `loadVorgangWorkspace` lädt die bestehende Ressource `GET /api/vorgaenge/<vorgangs_id>/mail-dokumentzuordnungen` parallel zu den vorhandenen Vorgangsdaten.
- Der neue Editor zeigt jeden vom vorgangsspezifischen Endpoint gelieferten Beleg mit Dateiname und verfügbaren Metadaten. Mail-Anhänge werden anhand von `mail_inbox_id` und `mail_attachment_index` gekennzeichnet.
- Die Optionen werden ausschließlich aus `assignmentPayload.transaktionen` aufgebaut. Der Server liefert diese aus `transaktion_vorgaenge` für genau den angeforderten Vorgang und validiert PUT-Zuordnungen erneut gegen diesen Vorgang.
- Die erste Option `Keine spezifische Transaktion` besitzt den Leerwert und wird beim Speichern korrekt als `transaktions_id: null` serialisiert.
- Beim Speichern werden alle sichtbaren Selects als vollständige Liste unter `zuordnungen` per PUT an den vorhandenen Endpoint gesendet.
- Nach erfolgreichem PUT wird der vollständige Vorgangs-Workspace neu geladen. Bei Fehlern bleibt die lokale Auswahl sichtbar, der Status wird als Fehler angezeigt und die globale Fehlermeldung wird gesetzt; ein Erfolg wird nicht dargestellt.
- Unveränderte Werte aktivieren den Speichern-Button nicht. Für keine Dokumente und für Vorgänge ohne verknüpfte Transaktionen existieren klare Leerzustände.

## Architektur und Scope

Die Umsetzung verwendet ausschließlich die vorhandene vorgangsbasierte API und die bestehende Persistenz über `vorgang_belege.vorgangsbezug_id` beziehungsweise `transaktion_vorgaenge.bezugs_id`. Es wurden weder Tabellen, Migrationen noch eine direkte Transaktion-Beleg-Beziehung ergänzt. Externe Mail-, Banking-, Graph- oder Login-Aktionen wurden nicht eingeführt.

## Tests

Die vorhandene lokale HTTP-Prüfung `test_mail_document_assignment_api_validates_vorgang_context` deckt das Laden per GET, erfolgreiches und idempotentes Speichern per PUT, ungültige Beleg- und Transaktions-IDs, vorgangsfremde Transaktionen, widersprüchliche Vorgangs-IDs, unbekannte Payload-Felder sowie den unveränderten bestätigten Stand nach Fehlern ab. Sie verwendet ausschließlich lokale Testdaten und Fakes.

Laut Implementation Report liefen zusätzlich `node --check banking_dashboard/static/app.js`, die Dashboard-Suite mit 112 bestandenen und 6 übersprungenen Tests sowie `git diff --check` erfolgreich.

## Compare-Status

Der Branch ist gegenüber `main` um einen Commit voraus, nicht hinter `main`, und die vom Runner validierten beziehungsweise gestagten Dateien entsprechen dem GitHub-Compare. Es bestehen keine Compare-Abweichungen.
