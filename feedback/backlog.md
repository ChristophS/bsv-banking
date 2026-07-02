# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Spam-Score bleibt häufig bei 0 Prozent analysieren und korrigieren

**Priorität:** hoch

**Grund:** Eigenes Mail-Processing-Thema mit separater Ursachenanalyse in mail_integration und zugehörigen Tests; nicht Teil des kleinen UI-Pakets.

**Feedback:**

- Spam score ist immernoch oft auf 0%

## 2. Ein-Klick-Workflow für Vorgangserstellung, Klassifikation und Abschluss

**Priorität:** hoch

**Grund:** Größerer, fachlich übergreifender Workflow über Vorgangserstellung, Transaktionsklassifikation und Statussteuerung; für ein kleines kontrolliertes Paket zu breit.

**Feedback:**

- Wenn ich einen Vorgang erstelle und es sind schon alle informationen da, dann will ich einen Vorgang direkt anlegen und erledigen koennen in einem Klick. Dazu gehoert auch, dass ich wenn eine Transaktion verknuepft ist bei dieser transaktion direkt die Parameter (Typ, Oberkategorie, unterkategorie, etc ) eintragen kann.

## 3. Mail direkt einem bestehenden Vorgang zuordnen

**Priorität:** hoch

**Grund:** Wichtiger eigener Flow im Mail-Reiter mit bestehender inbox_vorgaenge-API, aber separate UI-Umsetzung und Interaktionslogik.

**Feedback:**

- Ich moechte erne aus dem Mailreiter heraus eine Mail einem Vorgang zuordnen koennen.

## 4. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Komplexeres Modellierungs- und UX-Thema; aktuelle Architektur verknüpft Belege direkt mit Vorgängen, nicht mit Transaktionen.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Ueberlege wie man geschickt damit umgehen kann

## 5. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Großes neues Fachmodul mit externer Integration und eigenem Datenmodell; nicht klein genug für das nächste Arbeitspaket.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfaengern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas komplizierter, da es ueber DFBnet Vrein laeuft. ...

## 6. Dashboard-Usability schrittweise verbessern ohne Funktionsverlust

**Priorität:** mittel

**Grund:** Querschnittsthema; das aktuelle Paket adressiert davon gezielt nur den manuellen Vorgangsabschluss.

**Feedback:**

- Man merkt deutlich, dass das Tool gewachsen ist. Es ist stellenweise sehr unintuitiv oder unuebersichtlich. Vlt kannst du das verbessern ohne, dass Funktionalitaeten verloren gehen.
