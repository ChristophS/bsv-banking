# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. DFBnet-Ergebnisliste robuster auslesen und Retry-Verhalten prüfen

**Priorität:** hoch

**Grund:** Betroffen sind externe DFBnet-Abfragen und Fehlerbehandlung, nicht die manuelle Gegenpositions-UI.

**Feedback:**

- Wenn bei den Prämien Spieltage fehlen: Kannst du das nicht eifnach retryen oder so? manchmal gehen die, manchmal nicht: BSV - Damen: fehlende Spieltage 12, 18. Bitte DFBnet-Ergebnisliste/Pagination pruefen.
- Bei Zahlungsdaten abrufen kam auch beim ersten Mal: Die DFBnet-Mitgliedersuche wurde nicht gefunden.    (Beim zweiten mal gings)

## 2. Dateipfad in der Deckellisten-Zuordnung auswählbar machen

**Priorität:** mittel

**Grund:** Betraf die Deckellisten-Zuordnung und Dateiauswahl, nicht die Gegenpositions-Erfassung.

**Feedback:**

- Bei der Zuordnung zur Deckelliste will ich den Dateipfad auswählen können. Der kann aber auch vorausgewählt sein

## 3. Automatische Zuordnung bei 100% Übereinstimmung zwischen Deckelliste und Spielerprämien

**Priorität:** hoch

**Grund:** Das ist ein eigener Zuordnungs- und Matching-Workflow außerhalb der manuellen Gegenposition.

**Feedback:**

- Die 100% Übereisntimmung zwischen Deckelliste und Spielerprämien werden nicht automatisch zugeordnet. Warum?

## 4. Abweichende Trefferlage zwischen Prämien und Deckelliste analysieren

**Priorität:** mittel

**Grund:** Das ist eine Analyse- und Matching-Frage für Prämien/Deckelliste, nicht Teil der UI-Erweiterung für Gegenpositionen.

**Feedback:**

- Es gibt Fälle da werden bei den Prämien valide Zahlungsdaten gefunden, bei der Deckelliste aber nicht, warum?

## 5. Transaktionen nach abgeschlossenen Vorgängen filterbar machen

**Priorität:** mittel

**Grund:** Eigenes Listen-/Filterthema für Transaktionen, unabhängig vom Overlay für Gegenpositionen.

**Feedback:**

- Bitte einen Filter bei Transaktionen, dass Transaktionen, die zu einem bereits abgeschlossenen Vorgang gehören ein- und ausgeblendet werden können

## 6. Umbuchungen als zweitransaktionale Vorgänge sinnvoll abbilden

**Priorität:** hoch

**Grund:** Das ist ein fachlicher Sonderfall für automatische Modellierung und Vorgangslogik und braucht mehr Kontext als das kleine Overlay-Paket.

**Feedback:**

- Es gibt den Transaktionstyp "Umbuchung". Die läuft immer als Oberkategorie "Sonstiges" - Unterkategorie "Umbuchung" - Sphäre "Ideeller Bereich". Das wird immer als Vorgang mit 2 Transaktionen angelegt. Position und Gegenposition. Bitte überlege wie man das sinnvoll umsetzen kann

## 7. Dokumente aus E-Mails ohne Vorgangserstellung speichern

**Priorität:** mittel

**Grund:** Betreffend Mail-/Dokumentenfluss und Speicherung, nicht die manuelle Gegenpositions-UI.

**Feedback:**

- Ich hätte gerne die Möglichkeit Dokumente aus einer Mail direkt zu speichern ohne einen Vorgang zu erstellen

## 8. Spam-Erkennung verbessern

**Priorität:** hoch

**Grund:** Eigenes Klassifikations- und Scoring-Thema, nicht Teil der Gegenpositions-Erfassung.

**Feedback:**

- Jetzt sind alle Spam-Scores bei 0%. Es scheint, dass die Spamerkennung nicht gut funktioniert.

## 9. Gelesen-Status auf den gesamten Mailverlauf übertragen

**Priorität:** mittel

**Grund:** Das betrifft Mail-Statuslogik und Verlaufssynchronisation, nicht die Gegenpositions-UI.

**Feedback:**

- Auch wenn ich eine Mail mit Gelesen markiere, soll der gesamte Verlauf als "Gelesen" markiert werden
