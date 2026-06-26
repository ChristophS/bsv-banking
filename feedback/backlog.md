# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Deckelliste-Zuordnung mit Dateipfad-Auswahl und automatische 100%-Zuordnung nachschärfen

**Priorität:** hoch

**Grund:** Benötigt einen eigenen Blick auf den Prämien-/Deckellisten-Workflow und wahrscheinlich zusätzliche Kontextdateien, um die betroffenen UI- und Zuordnungsstellen repo-konkret zu ändern.

**Feedback:**

- Bei der Zuordnung zur Deckelliste will ich den Dateipfad auswählen können. Der kann aber auch vorausgewählt sein
- Die 100% Übereisntimmung zwischen Deckelliste und Spielerprämien werden nicht automatisch zugeordnet. Warum?
- Es gibt Fälle da werden bei den Prämien valide Zahlungsdaten gefunden, bei der Deckelliste aber nicht, warum?

## 2. Manuelle Gegenposition als Overlay mit Dropdown-Vorschlägen für Klassifikationsfelder

**Priorität:** hoch

**Grund:** Das betrifft einen separaten UI-Flow für Vorgänge und Transaktionen und sollte mit den konkreten Detail- und Formular-Komponenten des Dashboards sauber geplant werden.

**Feedback:**

- Bei einer manuellen Gegenposition sind Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre Pflicht. Bitte da wie so oft auch ein Dropdown mit bereits eingetragenen Werten in diesen Feldern (aus Transaktionen) aber auch der Möglichkeit etwas manuell anzulegen
- Bitte die manuelle Gegenposition als Pop-Up bzw Overlay, da man sonst weit runter scrollen muss

## 3. Transaktionen mit bereits abgeschlossenen Vorgängen ausblendbar machen

**Priorität:** mittel

**Grund:** Eigenes UI- und API-Filterthema; sollte getrennt vom Mail-Thema umgesetzt werden.

**Feedback:**

- Bitte einen Filter bei Transaktionen, dass Transaktionen, die zu einem bereits abgeschlossenen Vorgang gehören ein- und ausgeblendet werden können

## 4. Umbuchungs-Transaktionstyp als zweitransaktionalen Vorgang modellieren

**Priorität:** mittel

**Grund:** Erfordert fachliche Klärung der Vorgangs- und Transaktionslogik und sollte als eigenes, kontrolliertes Arbeitspaket geplant werden.

**Feedback:**

- Es gibt den Transaktionstyp "Umbuchung". Die läuft immer als Oberkategorie "Sonstiges" - Unterkategorie "Umbuchung" - Sphäre "Ideeller Bereich". Das wird immer als Vorgang mit 2 Transaktionen angelegt. Position und Gegenposition. Bitte überlege wie man das sinnvoll umsetzen kann

## 5. Dokumente direkt aus Mail ohne Vorgang speichern

**Priorität:** mittel

**Grund:** Berührt Mail-, Beleg- und Vorgangslogik sowie Speicherung und Zuordnung; dafür ist mehr Kontext nötig als für ein kleines Folgepaket.

**Feedback:**

- Ich hätte gerne die Möglichkeit Dokumente aus einer Mail direkt zu speichern ohne einen Vorgang zu erstellen
