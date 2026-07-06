# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Transaktionen splitten und Teilbeträge mehreren Kategorien oder Rechnungen zuordnen

**Priorität:** hoch

**Grund:** Großer Eingriff in Datenmodell, Zuordnungen, UI und Auswertungen; nicht klein genug für dieses Folgepaket.

**Feedback:**

- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 2. Bestehende Transaktion einem vorhandenen Vorgang zuordnen und passende Vorgänge vorschlagen

**Priorität:** hoch

**Grund:** Eigenständiger Zuordnungs-Flow; vorhandene Vorschlagslogik ist erkennbar, sollte aber separat umgesetzt werden.

**Feedback:**

- ich kann aus den Transaktionen heraus zwar einen Vorgang erstellen, aber nicht eine Transaktion einen Vorgang zuordnen. Wäre cool, wenn dann auch ein Vorschlag kommen könnte welcher Vorgang passend wäre

## 3. Vorgangsübersicht nach Status priorisieren

**Priorität:** mittel

**Grund:** Klar abgrenzbar, aber weniger arbeitskritisch als der gewählte Mail-/Vorgangs-Fix.

**Feedback:**

- Vorhandenes next_task: Vorgangsübersicht nach Status priorisieren

## 4. Mehrere Anhänge einer Mail in der Vorgangsanlage sichtbar und nutzbar machen

**Priorität:** hoch

**Grund:** Separater Mail-/Dokumenten-Flow mit UI-Auswirkungen; nicht Teil dieses kleinen Pakets.

**Feedback:**

- Wenn ich einen neuen Vorgang anlege kann ich nur das erste Dokument einer Mail in der Vorschau sehen

## 5. Button-Text und Position beim Vorgangsanlegen aus Mail verbessern

**Priorität:** mittel

**Grund:** UI-/UX-Verbesserung, aber nicht so dringlich wie der gewählte Funktionsfix.

**Feedback:**

- Wenn ich einen Vorgang erstelle kommt das Feld zum wirklichen Erstellen des Vorgangs immer ganz unten das ist oft unpraktikabel wenn man immer runterscrollen muss. und "Bestätigt importieren" ist auch ein komischer Name. Bitte "Vorgang anlegen" oder so, bzw vlt sogar, wenn das Häkchen bei Vorgang abschließen ist, auch "Vorgang abschließen"

## 6. Manuelles To-Do-Anlegen auch ohne Vorschlag ermöglichen

**Priorität:** hoch

**Grund:** Kleines eigenes Paket im Vorgangsanlage-Flow, aber nicht das aktuell gewählte Prioritätsthema.

**Feedback:**

- Wenn ich einen Vorgang erstelle und mir kein ToDo vorgeschlagen wird (vlt auch bei anderen Entitäten), dann kann ich auch kein ToDO erstellen. Das ist nicht sinnvoll. Ich will im Zweifel auch manuell ToDos erstellen können

## 7. Aktuellste Transaktionen im mailbasierten Vorgangsanlegen verfügbar machen

**Priorität:** hoch

**Grund:** Eigenständiger Kandidaten-/Refresh-Flow zwischen Mail-Import-UI und Transaktionsdaten.

**Feedback:**

- Ich habe die transaktionen aktualisiert. wenn ich aber aus einer Mail heraus einen Vorgang erstelle kann ich die ganz aktuellen Transaktionen nicht verknüpfen. Die werden mir gar nicht angezeigt

## 8. Fehlbuchungs-Flow für Nullung mit Gegenbetrag und direktem Abschluss

**Priorität:** hoch

**Grund:** Eigener fachlicher Spezialfall mit Validierungs- und Abschlusslogik; separat behandeln.

**Feedback:**

- Ich habe aktuelle eine Fehlbuchung. Diese muss zusammen mit dem Gegenbetrag einfach genullt und abgeschlossen werden können. Fehlbuchungen haben immer: Vorgangstyp "Sonstige", Oberkategorie "Sonstige" Unterkategorie "Fehlbuchung", Sphäre "leer" und können sofort als abgeschlossen markiert werden

## 9. Mail-Senden: Zeilenumbrüche erhalten und Empfängerauswahl ermöglichen

**Priorität:** hoch

**Grund:** Separater Compose-/Reply-Flow im Mailmodul.

**Feedback:**

- Wenn ich direkt aus dem Tool eine Mail sende, dann werden zeilenumbrüche ignoriert. Ich kann auch nicht auswählen an wen.

## 10. Dashboard-Startseite mit anstehenden Terminen, To-Dos, offenen Vorgängen und Alles-synchronisieren

**Priorität:** mittel

**Grund:** Größerer Oberflächenpunkt mit mehreren Widgets und Startseitenlogik.

**Feedback:**

- Gut wäre, wenn man beim Start ein Dashboard hätte mit anstehenden Terminen, ToDos, offene Vorgänge, usw. UND einen Button mit "alles synchronisieren" Also Mails, Transaktionen vor allem

## 11. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere Dokument-/Zuordnungs-Erweiterung; nicht Teil des aktuellen kleinen Pakets.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 12. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Neues größeres Modul mit Konzeptionsbedarf; klar außerhalb eines kleinen nächsten Arbeitspakets.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.
