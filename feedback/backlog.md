# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Spam-Score bleibt häufig bei 0 Prozent analysieren und korrigieren

**Priorität:** hoch

**Grund:** Eigenes Mail-Processing-Thema mit Backend-/Caching-Logik; unabhängig von der UI-Erweiterung zur Mail-Vorgangszuordnung.

**Feedback:**

- Spam score ist immernoch oft auf 0%

## 2. Ein-Klick-Workflow für Vorgangserstellung, Klassifikation und Abschluss

**Priorität:** hoch

**Grund:** Größerer Workflow über Vorgangsanlage, Transaktionsklassifikation und Abschlusslogik; für ein kleines kontrolliertes Paket zu breit.

**Feedback:**

- Wenn ich einen Vorgang erstelle und es sind schon alle informationen da, dann will ich einen Vorgang direkt anlegen und erledigen können in einem Klick. Dazu gehört auch, dass ich wenn eine Transaktion verknüpft ist bei dieser transaktion direkt die Parameter (Typ, Oberkategorie, unterkategorie, etc ) eintragen kann.

## 3. Manuellen Abschluss von Vorgängen intuitiver machen

**Priorität:** hoch

**Grund:** Eigenes UI-/Usability-Thema in der Vorgangsansicht; sollte separat angepasst und getestet werden.

**Feedback:**

- Aktuell kann ich auch keine Vorgänge manuell schließen. Sie können nur über Abschlussregeln geschlossen werden. Ach doch das geht, aber der Button ist irgendwie mittendrin. Sehr unintuitiv

## 4. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Komplexerer Modellierungs- und UI-Workflow; berührt die aktuelle Architektur, weil Belege heute an Vorgänge und nicht direkt an Transaktionen hängen.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege wie man geschickt damit umgehen kann

## 5. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Großes neues Fachmodul mit externer Integration; klar außerhalb eines kleinen Umsetzungspakets.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas komplizierter, da es über DFBnet Vrein läuft. ...

## 6. Dashboard-Usability schrittweise verbessern ohne Funktionsverlust

**Priorität:** mittel

**Grund:** Querschnittsthema ohne klar begrenzte Einzeländerung; sollte in mehrere kleine UI-Pakete zerlegt werden.

**Feedback:**

- Man merkt deutlich, dass das Tool gewachsen ist. Es ist stellenweise sehr unintuitiv oder unübersichtlich. Vlt kannst du das verbessern ohne, dass Funktionalitäten verloren gehen.
