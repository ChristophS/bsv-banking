# Backlog

**Planungsstatus:** strukturiert

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Dashboard als Startseite mit freier Tab-Navigation gestalten

**Epic-ID:** epic-dashboard-navigation

**Epic-Titel:** Dashboard-Navigation und fachliche Übersichten entlasten

**Epic-Ziel:** Das Dashboard soll je Fachbereich unmittelbar die relevanten Inhalte zeigen, ohne dauerhaft sichtbare globale Blöcke als Sichtblocker.

**Teilpaket:** Teil 1

**Priorität:** hoch

**Grund:** Die offene Arbeit steht derzeit dauerhaft oben und blockiert beim Wechsel der Tabs die Sicht auf weitere Inhalte. Sie soll eher auf einer eigenen Startseite erscheinen.

**Feedback:**

- Die offene Arbeit steht zwar immer oben. Das sollte aber eher eine Startseite sein.
- Wenn ich die Tabs wechsle, blockiert das die Sicht und ich muss erst nach unten scrollen.

## 2. Transaktionsansicht ohne dominanten Saldokorrektur-Block anzeigen

**Epic-ID:** epic-dashboard-navigation

**Epic-Titel:** Dashboard-Navigation und fachliche Übersichten entlasten

**Epic-Ziel:** Das Dashboard soll je Fachbereich unmittelbar die relevanten Inhalte zeigen, ohne dauerhaft sichtbare globale Blöcke als Sichtblocker.

**Teilpaket:** Teil 2

**Priorität:** hoch

**Grund:** Beim Öffnen von Transaktionen sollen die Transaktionen sofort sichtbar sein. Saldokorrekturen sollen die eigentliche Transaktionsliste nicht verdrängen; das Datum des Datenstands soll erkennbar sein.

**Feedback:**

- Die Saldokorrekturen unter Transaktionen sind ein großer Sichtblocker.
- Wenn ich auf Transaktionen gehe, will ich sofort die Transaktionen sehen.
- Am besten noch mit dem Datum des Standes der Daten.

## 3. Mail als gelesen markieren trotz MailboxConcurrency-Fehler ermöglichen

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1

**Priorität:** hoch

**Grund:** Das Markieren einer Mail als gelesen schlägt mit einer MailboxConcurrency-Fehlermeldung fehl und benötigt eine robuste, begrenzte Verarbeitung ohne echte externe Mail-Aktionen in Tests.

**Feedback:**

- Ich wollte eine Mail als gelesen markieren. Das ging nicht.
- Application is over its MailboxConcurrency limit.

## 4. Nicht mehr vorhandene Mails aus der Übersicht entfernen

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 2

**Priorität:** hoch

**Grund:** Wenn eine Mail außerhalb der Anwendung gelöscht wurde und beim Öffnen nicht mehr im Store gefunden wird, soll die Übersicht den veralteten Eintrag umgehend entfernen statt einen Fehler anzuzeigen.

**Feedback:**

- The specified object was not found in the store.
- The process failed to get the correct properties.
- Wenn die Mail anderweitig gelöscht wurde, sollte sie umgehend aus der Übersicht gelöscht werden.

## 5. Vorgang beim Anlegen optional direkt abschließen

**Epic-ID:** epic-vorgangsabschluss

**Epic-Titel:** Vorgänge beim Erstellen kontrolliert abschließen

**Epic-Ziel:** Vorgänge sollen bei ihrer Erstellung optional direkt in den abgeschlossenen Status überführt werden können, ohne die bestehende vorgangsbasierte Struktur zu umgehen.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Bei der Erstellung eines Vorgangs soll zusätzlich die fachliche Option verfügbar sein, den Vorgang in einem Schritt anzulegen und abzuschließen.

**Feedback:**

- Bei der Erstellung eines Vorgangs sollte es auch die Option geben: Vorgang anlegen und abschließen.
