# Backlog

**Planungsstatus:** strukturiert

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Spielerprämien bis zur auszahlungsfähigen Prüfung und Bereitstellung fertigstellen

**Epic-ID:** epic-player-premiums

**Epic-Titel:** Spielerprämien vollständig und zuverlässig ermitteln

**Epic-Ziel:** Spielerprämien für alle relevanten Mannschaften und Spieltage vollständig aus den verfügbaren Ergebnisdaten ermitteln, prüfen und für die weitere Vorgangsbearbeitung bereitstellen.

**Teilpaket:** Teil 2

**Priorität:** hoch

**Grund:** Nach der vollständigen Ergebniserfassung muss noch die zuverlässige Bereitstellung für die weitere Auszahlungsvorbereitung abgesichert werden.

**Feedback:**

- Alles was mit Spielerprämien zu tun hat, hat absolut höchste Priorität. Die müssen raus.

## 2. Offene Arbeit als eigene Startseite statt als dauernder Sichtblock

**Priorität:** mittel

**Grund:** Die offene Arbeit soll weiterhin prominent erreichbar sein, aber nicht jede andere Registerkarte nach unten verdrängen.

**Feedback:**

- Die offene Arbeit steht zwar immer oben. Das sollte aber eher eine Startseite sein.
- Wenn ich die Tabs wechsle blockiert das die Sicht und ich muss erst runter scrollen um mehr zu sehen.

## 3. Saldokorrekturen aus der Transaktionsansicht herausnehmen und Datenstand anzeigen

**Priorität:** mittel

**Grund:** Beim Öffnen von Transaktionen sollen sofort die Transaktionen sichtbar sein; Saldokorrekturen nehmen derzeit zu viel Platz ein. Zusätzlich soll der Stand der Kontodaten mit Datum erkennbar sein.

**Feedback:**

- Saldokorrekturen unter Transaktionen sind ein großer Sichtblocker.
- Auf Transaktionen will ich sofort die Transaktionen sehen.
- Am besten noch mit dem Datum des Standes der Daten.

## 4. Mail als gelesen markieren trotz MailboxConcurrency-Fehler ermöglichen

**Priorität:** hoch

**Grund:** Das Markieren als gelesen schlägt wegen des MailboxConcurrency-Limits fehl und verhindert eine zentrale Mailbearbeitung.

**Feedback:**

- Ich wollte eine Mail als gelesen markieren. Das ging nicht.
- Application is over its MailboxConcurrency limit.

## 5. Nicht mehr vorhandene Mails automatisch aus der Übersicht entfernen

**Priorität:** hoch

**Grund:** Wenn Outlook oder ein anderes Gerät eine Mail bereits gelöscht hat, soll ein Object-not-found-Fehler nicht dauerhaft in der Übersicht erscheinen.

**Feedback:**

- The specified object was not found in the store.
- The process failed to get the correct properties.
- Wenn er nichts findet, sollte sie umgehend aus der Übersicht gelöscht werden.

## 6. Vorgang beim Erstellen direkt abschließen können

**Priorität:** mittel

**Grund:** Die Erstellung eines Vorgangs soll eine Option für „Vorgang anlegen und abschließen“ anbieten, sofern die bestehenden Abschlussregeln erfüllt sind.

**Feedback:**

- Bei der Erstellung eines Vorgangs sollte es auch die Option geben: "Vorgang anlegen und abschließen"
