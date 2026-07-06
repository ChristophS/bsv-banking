# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Mehrere Anhänge einer Mail in der Vorgangsanlage sichtbar und nutzbar machen

**Priorität:** hoch

**Grund:** Eigenständiger Dokument-/Preview-Flow im Mail-Import; bewusst nicht mit der kleinen Sortieränderung vermischen.

**Feedback:**

- Wenn ich einen neuen Vorgang anlege kann ich nur das erste Dokument einer Mail in der Vorschau sehen

## 2. Button-Text und Position beim Vorgangsanlegen aus Mail verbessern

**Priorität:** mittel

**Grund:** Reine UX-Anpassung im Importformular; separater UI-Flow.

**Feedback:**

- Wenn ich einen Vorgang erstelle kommt das Feld zum wirklichen Erstellen des Vorgangs immer ganz unten das ist oft unpraktikabel wenn man immer runterscrollen muss. und "Bestätigt importieren" ist auch ein komischer Name. Bitte "Vorgang anlegen" oder so, bzw vlt sogar, wenn das Häkchen bei Vorgang abschließen ist, auch "Vorgang abschließen"

## 3. Manuelles To-Do-Anlegen auch ohne Vorschlag ermöglichen

**Priorität:** hoch

**Grund:** Eigener To-Do-Erfassungsfluss im Mail-/Entitäten-Import, getrennt von der Sortierung.

**Feedback:**

- Wenn ich einen Vorgang erstelle und mir kein ToDo vorgeschlagen wird (vlt auch bei anderen Entitäten), dann kann ich auch kein ToDO erstellen. Das ist nicht sinnvoll. Ich will im Zweifel auch manuell ToDos erstellen können

## 4. Aktuellste Transaktionen im Mail-basierten Vorgangsanlegen verfügbar machen

**Priorität:** hoch

**Grund:** Betrifft Refresh-/Kandidatenlogik im Importflow und vermutlich Datenneuladen in Mail/Vorgang-Verknüpfung.

**Feedback:**

- Ich habe die transaktionen aktualisiert. wenn ich aber aus einer Mail heraus einen Vorgang erstelle kann ich die ganz aktuellen Transaktionen nicht verknüpfen. Die werden mir gar nicht angezeigt

## 5. Fehlbuchungs-Flow für Nullung mit Gegenbetrag und direktem Abschluss

**Priorität:** hoch

**Grund:** Eigenständiger Fachfall mit Abschluss- und Klassifikationslogik; zu groß für dieses kleine Paket.

**Feedback:**

- Ich habe aktuelle eine Fehlbuchung. Diese muss zusammen mit dem Gegenbetrag einfach genullt und abgeschlossen werden können. Fehlbuchungen haben immer: Vorgangstyp "Sonstige", Oberkategorie "Sonstige" Unterkategorie "Fehlbuchung", Sphäre "leer" und können sofort als abgeschlossen markiert werden

## 6. Mail-Senden: Zeilenumbrüche erhalten und Empfängerauswahl ermöglichen

**Priorität:** hoch

**Grund:** Separater Compose-/Reply-Flow mit Backend-Payload und UI-Anpassungen.

**Feedback:**

- Wenn ich direkt aus dem Tool eine Mail sende, dann werden zeilenumbrüche ignoriert. Ich kann auch nicht auswählen an wen.

## 7. Verknüpfte oder abgeschlossene Vorgangs-Mails automatisch als gelesen markieren

**Priorität:** mittel

**Grund:** Übergreifender Mail-/Vorgangsstatus-Workflow; getrennt von der Listen-Sortierung.

**Feedback:**

- Wenn ein Vorgang abgeschlossen ist, sollen zugehörige Mails automatisch als gelesen markiert werden. Bzw nicht nur bei abgeschlossenem Vorgang, sondern auch bei verknüpften (offenen) Vorgang.

## 8. Dashboard-Startseite mit anstehenden Terminen, To-Dos, offenen Vorgängen und Alles-synchronisieren

**Priorität:** mittel

**Grund:** Größere Startseiten- und Synchronisations-Erweiterung mit mehreren Datenquellen.

**Feedback:**

- Gut wäre, wenn man beim Start ein Dashboard hätte mit anstehenden Terminen, ToDos, offene Vorgänge, usw. UND einen Button mit "alles synchronisieren" Also Mails, Transaktionen vor allem

## 9. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere fachliche Erweiterung über Dokumenthandling und Zuordnungslogik; nicht Teil des kleinen Sortierpakets.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 10. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Eigenständiges größeres Modul mit zusätzlichem Datenmodell und externer Integration.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.
