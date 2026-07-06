# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Transaktionen splitten und Teilbeträge mehreren Kategorien oder Rechnungen zuordnen

**Priorität:** hoch

**Grund:** Größerer Eingriff in Datenmodell, Zuordnungen, UI und Auswertungen; nicht klein genug für das nächste kontrollierte Paket.

**Feedback:**

- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 2. Bestehende Transaktion einem vorhandenen Vorgang zuordnen und passende Vorgänge vorschlagen

**Priorität:** hoch

**Grund:** Separater Zuordnungs- und Vorschlags-Flow; bestehende Kandidaten-/Suggestion-Logik ist vorhanden, aber als eigenes Paket sauberer.

**Feedback:**

- ich kann aus den Transaktionen heraus zwar einen Vorgang erstellen, aber nicht eine Transaktion einen Vorgang zuordnen. Wäre cool, wenn dann auch ein Vorschlag kommen könnte welcher Vorgang passend wäre

## 3. Vorgangsübersicht nach Status priorisieren

**Priorität:** mittel

**Grund:** Klar abgrenzbar, aber hinter dem ausgewählten hochprioren Dokument-Öffnungsproblem zurückgestellt.

**Feedback:**

- Vorhandenes next_task: Vorgangsübersicht nach Status priorisieren

## 4. Mehrere Anhänge einer Mail in der Vorgangsanlage sichtbar und nutzbar machen

**Priorität:** hoch

**Grund:** Anderer Mail-/Dokumenten-Flow; sollte separat umgesetzt und getestet werden.

**Feedback:**

- Wenn ich einen neuen Vorgang anlege kann ich nur das erste Dokument einer Mail in der Vorschau sehen

## 5. Button-Text und Position beim Vorgangsanlegen aus Mail verbessern

**Priorität:** mittel

**Grund:** UX-Verbesserung, aber nicht so arbeitskritisch wie der Dokument-Öffnungsfall.

**Feedback:**

- Wenn ich einen Vorgang erstelle kommt das Feld zum wirklichen Erstellen des Vorgangs immer ganz unten das ist oft unpraktikabel wenn man immer runterscrollen muss. und "Bestätigt importieren" ist auch ein komischer Name. Bitte "Vorgang anlegen" oder so, bzw vlt sogar, wenn das Häkchen bei Vorgang abschließen ist, auch "Vorgang abschließen"

## 6. Manuelles To-Do-Anlegen auch ohne Vorschlag ermöglichen

**Priorität:** hoch

**Grund:** Separater Erfassungsflow für Mail-/Vorgangsanlage; eigenes kleines Paket möglich.

**Feedback:**

- Wenn ich einen Vorgang erstelle und mir kein ToDo vorgeschlagen wird (vlt auch bei anderen Entitäten), dann kann ich auch kein ToDO erstellen. Das ist nicht sinnvoll. Ich will im Zweifel auch manuell ToDos erstellen können

## 7. Aktuellste Transaktionen im mailbasierten Vorgangsanlegen verfügbar machen

**Priorität:** hoch

**Grund:** Eigener Kandidaten-/Refresh-Flow zwischen Mail-Import-UI und aktuellen Transaktionsdaten.

**Feedback:**

- Ich habe die transaktionen aktualisiert. wenn ich aber aus einer Mail heraus einen Vorgang erstelle kann ich die ganz aktuellen Transaktionen nicht verknüpfen. Die werden mir gar nicht angezeigt

## 8. Fehlbuchungs-Flow für Nullung mit Gegenbetrag und direktem Abschluss

**Priorität:** hoch

**Grund:** Eigener fachlicher Spezialfall mit Abschlusslogik und Validierungsfolgen; besser separat.

**Feedback:**

- Ich habe aktuelle eine Fehlbuchung. Diese muss zusammen mit dem Gegenbetrag einfach genullt und abgeschlossen werden können. Fehlbuchungen haben immer: Vorgangstyp "Sonstige", Oberkategorie "Sonstige" Unterkategorie "Fehlbuchung", Sphäre "leer" und können sofort als abgeschlossen markiert werden

## 9. Mail-Senden: Zeilenumbrüche erhalten und Empfängerauswahl ermöglichen

**Priorität:** hoch

**Grund:** Separater Compose-/Reply-Flow im Mailmodul.

**Feedback:**

- Wenn ich direkt aus dem Tool eine Mail sende, dann werden zeilenumbrüche ignoriert. Ich kann auch nicht auswählen an wen.

## 10. Verknüpfte oder abgeschlossene Vorgangs-Mails automatisch als gelesen markieren

**Priorität:** mittel

**Grund:** Teilweise besteht schon Abschluss-Logik; der erweiterte Fall 'bereits bei Verknüpfung' bleibt ein eigenes Restpaket.

**Feedback:**

- Wenn ein Vorgang abgeschlossen ist, sollen zugehörige Mails automatisch als gelesen markiert werden. Bzw nicht nur bei abgeschlossenem Vorgang, sondern auch bei verknüpften (offenen) Vorgang.

## 11. Dashboard-Startseite mit anstehenden Terminen, To-Dos, offenen Vorgängen und Alles-synchronisieren

**Priorität:** mittel

**Grund:** Größerer Oberflächenpunkt mit mehreren Widgets und Startseitenlogik.

**Feedback:**

- Gut wäre, wenn man beim Start ein Dashboard hätte mit anstehenden Terminen, ToDos, offene Vorgänge, usw. UND einen Button mit "alles synchronisieren" Also Mails, Transaktionen vor allem

## 12. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere Dokument-/Zuordnungs-Erweiterung; sollte nicht mit dem einfachen Originaldokument-Öffnen vermischt werden.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 13. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Neues größeres Modul mit Konzeptionsbedarf, klar außerhalb eines kleinen Folgepakets.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.
