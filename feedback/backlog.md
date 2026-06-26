# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. DFBnet-Spielerprämien robuster laden: Retry und Pagination prüfen

**Priorität:** hoch

**Grund:** Eigenes DFBnet-/Playwright-Thema und unabhängig vom Transaktionsfilter.

**Feedback:**

- Wenn bei den Prämien Spieltage fehlen: Kannst du das nicht eifnach retryen oder so? manchmal gehen die, manchmal nicht: BSV - Damen: fehlende Spieltage 12, 18. Bitte DFBnet-Ergebnisliste/Pagination pruefen.

## 2. DFBnet-Mitgliedersuche beim Zahlungsdatenabruf stabilisieren

**Priorität:** hoch

**Grund:** Separates Stabilitätsproblem im Zahlungsdatenabruf.

**Feedback:**

- Bei Zahlungsdaten abrufen kam auch beim ersten Mal: Die DFBnet-Mitgliedersuche wurde nicht gefunden.    (Beim zweiten mal gings)

## 3. Deckellisten-Dateipfad in der Zahlungsdatenprüfung auswählbar machen

**Priorität:** mittel

**Grund:** Eigenes UI-Thema in der Zahlungsdaten-/Deckellisten-Ansicht.

**Feedback:**

- Bei der Zuordnung zur Deckelliste will ich den Dateipfad auswählen können. Der kann aber auch vorausgewählt sein

## 4. Automatische Zuordnung bei 100%-Übereinstimmung zwischen Deckelliste und Spielerprämien prüfen

**Priorität:** hoch

**Grund:** Eigener Abgleichs-/Matching-Fix außerhalb des Transaktionsfilters.

**Feedback:**

- Die 100% Übereisntimmung zwischen Deckelliste und Spielerprämien werden nicht automatisch zugeordnet. Warum?

## 5. Unterschiede bei gefundenen Zahlungsdaten zwischen Prämien und Deckelliste untersuchen

**Priorität:** hoch

**Grund:** Separates Analyse- und Bugfix-Thema im Zahlungsdaten-Matching.

**Feedback:**

- Es gibt Fälle da werden bei den Prämien valide Zahlungsdaten gefunden, bei der Deckelliste aber nicht, warum?

## 6. Manuelle Gegenposition: Pflichtfelder mit bestehenden Klassifikationswerten als Vorschläge

**Priorität:** mittel

**Grund:** Eigenes Formular- und Klassifikationspaket; nicht Teil des Listenfilters.

**Feedback:**

- Bei einer manuellen Gegenposition sind Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre Pflicht. Bitte da wie so oft auch ein Dropdown mit bereits eingetragenen Werten in diesen Feldern (aus Transaktionen) aber auch der Möglichkeit etwas manuell anzulegen

## 7. Manuelle Gegenposition als Overlay/Popup anzeigen

**Priorität:** mittel

**Grund:** UI-Komfortthema für Gegenpositionen, abhängig vom Formular-Workflow.

**Feedback:**

- Bitte die manuelle Gegenposition als Pop-Up bzw Overlay, da man sonst weit runter scrollen muss

## 8. Umbuchungen als Vorgang mit Position und Gegenposition modellieren

**Priorität:** hoch

**Grund:** Fachlich größeres Vorgangs-/Transaktionsthema mit eigener Modellierungsfrage.

**Feedback:**

- Es gibt den Transaktionstyp "Umbuchung". Die läuft immer als Oberkategorie "Sonstiges" - Unterkategorie "Umbuchung" - Sphäre "Ideeller Bereich". Das wird immer als Vorgang mit 2 Transaktionen angelegt. Position und Gegenposition. Bitte überlege wie man das sinnvoll umsetzen kann

## 9. Mail-Anhänge direkt als Dokument speichern, ohne Vorgang zu erstellen

**Priorität:** mittel

**Grund:** Eigenes Mail-/Dokumententhema mit separaten Anpassungen.

**Feedback:**

- Ich hätte gerne die Möglichkeit Dokumente aus einer Mail direkt zu speichern ohne einen Vorgang zu erstellen

## 10. Spam-Score-Berechnung prüfen, wenn alle Mails 0% anzeigen

**Priorität:** hoch

**Grund:** Separates Mail-Processing-/Spam-Erkennungsthema.

**Feedback:**

- Jetzt sind alle Spam-Scores bei 0%. Es scheint, dass die Spamerkennung nicht gut funktioniert.

## 11. Gelesen-Markieren auf gesamten Mailverlauf anwenden

**Priorität:** hoch

**Grund:** Mail-Verlaufsaktion und nicht Teil des Transaktionsfilters.

**Feedback:**

- Auch wenn ich eine Mail mit Gelesen markiere, soll der gesamte Verlauf als "Gelesen" markiert werden
