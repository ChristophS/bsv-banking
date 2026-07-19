# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Vorgang beim Anlegen optional direkt abschließen

**Epic-ID:** epic-vorgangsabschluss

**Epic-Titel:** Vorgänge beim Erstellen kontrolliert abschließen

**Epic-Ziel:** Vorgänge sollen bei ihrer Erstellung optional direkt in den abgeschlossenen Status überführt werden können, ohne die bestehende vorgangsbasierte Struktur zu umgehen.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Beim Erstellen eines Vorgangs soll zusätzlich die fachliche Option verfügbar sein, den Vorgang in einem Schritt anzulegen und abzuschließen.

**Feedback:**

- Bei der Erstellung eines Vorgangs sollte es auch die Option geben: Vorgang anlegen und abschließen.

## 2. Explizite Exception-Klassen beziehungsweise strukturierte Fehlercodes für externe Mailobjekte statt textbasierter Erkennung ergänzen

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1.1

**Priorität:** mittel

**Grund:** Die aktuelle Erkennung fehlender externer Mailobjekte basiert laut Review noch auf generischer Lookup-Fehlerbehandlung; das sollte für die Mail-Synchronisation robuster und klarer abgrenzbar gemacht werden.

**Feedback:**

- Die Erkennung für fehlende externe Mailobjekte sollte über explizite Exception-Klassen oder strukturierte Fehlercodes erfolgen, statt nur textbasierte beziehungsweise generische Lookup-Fehler auszuwerten.

## 3. Automatisierten HTTP- oder Browser-Test für stale_mail_removed und die Entfernung aus der sichtbaren Mailübersicht hinzufügen

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1.2

**Priorität:** mittel

**Grund:** Der Review weist darauf hin, dass die fachliche UI-/HTTP-Abdeckung für den Fall stale_mail_removed noch weiter vervollständigt werden kann.

**Feedback:**

- Es sollte ein automatisierter HTTP- oder Browser-Test ergänzt werden, der den Fall `stale_mail_removed` sowie die Entfernung des Eintrags aus der sichtbaren Mailübersicht abdeckt.