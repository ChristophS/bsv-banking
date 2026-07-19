# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Umsetzung erfüllt die Muss-Anforderungen: Erwartbare Fehler für extern entfernte Mails werden erkannt, der lokale Inbox-Datensatz inklusive abhängiger Daten und In-Memory-Zustand wird entfernt, der HTTP-Endpunkt kennzeichnet den Fall separat und die Oberfläche entfernt den Eintrag ohne technischen Fehler. Unerwartete Mailfehler werden weitergereicht. Die Idempotenz ist durch den anschließenden lokalen Lookup ohne erneuten Backend-Abruf abgesichert. Branch und GitHub-Compare sind konsistent und die ergänzten Tests decken Löschung, Idempotenz und unerwartete Fehler ab.

# Technischer Review

## Entscheidung

**Akzeptiert.**

## Geprüfte Anforderungen

- Erwartbare Fehlerbilder für nicht mehr vorhandene externe Mailobjekte werden in `_is_missing_external_mail_error` erkannt.
- Beim erwartbaren Fehler wird der lokale Inbox-Datensatz über die bestehende `InboxMailStore.mark_deleted`-Logik entfernt. Durch die vorhandenen Foreign-Key-Beziehungen werden abhängige Datensätze mit entfernt.
- Der aktive Managerzustand für Nachrichten, Spam-Scores und Signaturen wird über `_remove_from_active_state` bereinigt.
- `StaleMailRemovedError` wird im HTTP-Endpunkt separat behandelt und als `404` mit `stale_mail_removed: true` ausgegeben.
- Die Mailoberfläche erkennt diese Antwort, entfernt den Eintrag aus `state.mails`, leert die Detailansicht und rendert die Liste ohne technischen Fehler.
- Unerwartete Fehler werden nicht pauschal verschluckt, sondern erneut ausgelöst und durch die bestehende Fehlerbehandlung verarbeitet.
- Die zweite Aktualisierung nach erfolgreicher lokaler Entfernung löst keinen zweiten Backend-Aufruf und keinen zweiten Löschvorgang aus, weil der lokale Datensatz nicht mehr aufgelöst werden kann.

## Tests

Die neuen Tests decken ab:

- extern gelöschte Mail führt zur Entfernung aus dem lokalen Inbox-Bestand,
- anschließender erneuter Zugriff bleibt fehlerfrei im Sinne der Idempotenz und ruft das Backend nicht erneut auf,
- unerwarteter Mailfehler bleibt ein `MailIntegrationError` und lässt den lokalen Bestand bestehen.

Der Implementation Report meldet außerdem 182 bestandene Tests und 7 übersprungene optionale Browser-/Umgebungstests. Der GitHub-Compare ist `ahead` um einen Commit, ohne fehlende oder zusätzliche Dateien gegenüber dem Runner-Stand.

## Architektur und Scope

Die Änderung verwendet bestehende Store-, Manager- und HTTP-Strukturen. Es wurde kein paralleles Mailmodell eingeführt und es erfolgen keine externen Löschaktionen. Die zusätzliche Frontend-Anpassung ist für das Akzeptanzkriterium zur fehlerfreien Benutzeroberfläche erforderlich. Die Änderung am Implementierungsbericht ist im Rahmen des Coding-Agenten-Reports unkritisch.

## Nicht blockierende Hinweise

Die Erkennung behandelt `LookupError` insgesamt als Hinweis auf ein fehlendes externes Objekt. Das ist für die bestehende Backend-Semantik plausibel, könnte aber langfristig durch explizitere externe Fehlerklassen oder Fehlercodes weiter eingegrenzt werden. Ein zusätzlicher HTTP-/UI-Test würde die bereits vorhandene fachliche Testabdeckung noch vervollständigen.
