# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Explizite Exception-Klassen beziehungsweise strukturierte Fehlercodes für externe Mailobjekte statt textbasierter Erkennung ergänzen

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1.1

**Priorität:** mittel

**Grund:** Die Erkennung fehlender externer Mailobjekte soll für die Mail-Synchronisation klarer und robuster von anderen Lookup- oder temporären Fehlern unterscheidbar sein.

**Feedback:**

- Die Erkennung für fehlende externe Mailobjekte sollte über explizite Exception-Klassen oder strukturierte Fehlercodes erfolgen, statt nur textbasierte beziehungsweise generische Lookup-Fehler auszuwerten.

## 2. Automatisierten HTTP- oder Browser-Test für stale_mail_removed und die Entfernung aus der sichtbaren Mailübersicht hinzufügen

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1.2

**Priorität:** mittel

**Grund:** Die fachliche Abdeckung des Falls stale_mail_removed und der anschließenden Entfernung des Eintrags aus der sichtbaren Mailübersicht soll vervollständigt werden.

**Feedback:**

- Es sollte ein automatisierter HTTP- oder Browser-Test ergänzt werden, der den Fall stale_mail_removed sowie die Entfernung des Eintrags aus der sichtbaren Mailübersicht abdeckt.