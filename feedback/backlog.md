# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Spam-Score untersuchen und stabilisieren

**Priorität:** hoch

**Grund:** Eigenes Thema im Mail-Scoring und Cache-Verhalten; benötigt gezielten Kontext aus dem Mail-Scoring-Teil des Repos.

**Feedback:**

- Spam score ist immernoch oft auf 0%

## 2. Vorschläge für Verknüpfungen weniger aufdringlich und besser priorisiert darstellen

**Priorität:** hoch

**Grund:** Separates UX-Thema rund um Vorschlagslogik und Frontend-Darstellung; sollte als eigenes Paket umgesetzt werden.

**Feedback:**

- Der Vorschlag von weitere Mails verknüpfen ist richtig schlecht. Ich verbringe viel zu viel Zeit damit die Vorschläge wegzuklicken. Vielleicht wäre sogar nur ein priorisiertes Sortieren von Vorschlägen (in allen Feldern) sinnvoll und nicht direkt anklicken

## 3. Vorgang direkt beim Anlegen inklusive Transaktionsklassifikation und Abschluss speichern

**Priorität:** hoch

**Grund:** Eigenes kleineres Backend-/Frontend-Paket rund um den kombinierten Create-/Classify-/Complete-Flow; bleibt separat, damit das aktuelle Paket klein bleibt.

**Feedback:**

- Wenn ich einen Vorgang erstelle und es sind schon alle informationen da, dann will ich einen Vorgang direkt anlegen und erledigen können in einem Klick. Dazu gehört auch, dass ich wenn eine Transaktion verknüpft ist bei dieser transaktion direkt die Parameter (Typ, Oberkategorie, unterkategorie, etc ) eintragen kann.

## 4. Mail im Mail-Reiter direkt einem bestehenden Vorgang zuordnen

**Priorität:** hoch

**Grund:** Eigenständige UI-/Workflow-Erweiterung im Mail-Reiter, die nicht Teil der aktuellen UI-Aufräumaufgabe ist.

**Feedback:**

- Ich möchte erne aus dem Mailreiter heraus eine Mail einem Vorgang zuordnen können.

## 5. Konzept für eine Mail mit mehreren Dokumenten zu unterschiedlichen Transaktionen innerhalb eines Vorgangs

**Priorität:** mittel

**Grund:** Fachlich komplexer Zuordnungsflow mit mehreren Entitäten; benötigt separates Konzept und saubere Zerlegung.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege wie man geschickt damit umgehen kann

## 6. Spendenbescheinigungen und Spender-/Adressdatenbank konzipieren

**Priorität:** mittel

**Grund:** Großes neues Fachmodul mit externer Automation, Datenmodell und Dokumenterzeugung; deutlich außerhalb des aktuellen Pakets.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas komplizierter, da es über DFBnet Vrein läuft. Ich hätte da gerne ein eigenes Interface mit Vorschlägen aus der Mail (Vorgang etc) falls etwas vorhanden ist und mit einem Dropdown (mit manueller Eingabe) der Spender aus der Datenbank.
- Das Erstellen einer Spendenbescheinigung läuft so: Auf DFBnet Verein einloggen ... Das entsprechende PDF speichern

## 7. Dashboard-Informationsarchitektur schrittweise vereinfachen

**Priorität:** mittel

**Grund:** Breites UX-Thema; sollte in mehrere kleine, messbare Pakete zerlegt werden.

**Feedback:**

- Man merkt deutlich, dass das Tool gewachsen ist. Es ist stellenweise sehr unintuitiv oder unübersichtlich. Vlt kannst du das verbessern ohne, dass Funktionalitäten verloren gehen.
