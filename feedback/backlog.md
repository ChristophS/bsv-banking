# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Transaktionen splitten und Teilbeträge mehreren Kategorien oder Rechnungen zuordnen

**Priorität:** hoch

**Grund:** Großer Eingriff in Datenmodell, Zuordnungen, UI und Auswertungen; nicht klein genug für das nächste kontrollierte Paket.

**Feedback:**

- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 2. Mehrere Anhänge einer Mail in der Vorgangsanlage sichtbar und nutzbar machen

**Priorität:** hoch

**Grund:** Eigener Mail-/Dokumenten-UI-Flow; sinnvoll separat nach dem Kandidaten-Refresh-Problem.

**Feedback:**

- Wenn ich einen neuen Vorgang anlege kann ich nur das erste Dokument einer Mail in der Vorschau sehen

## 3. Button-Text und Position beim Vorgangsanlegen aus Mail verbessern

**Priorität:** mittel

**Grund:** UI-/UX-Verbesserung, aber weniger kritisch als die Verfügbarkeit aktueller Transaktionen im Arbeitsflow.

**Feedback:**

- Wenn ich einen Vorgang erstelle kommt das Feld zum wirklichen Erstellen des Vorgangs immer ganz unten das ist oft unpraktikabel wenn man immer runterscrollen muss. und "Bestätigt importieren" ist auch ein komischer Name. Bitte "Vorgang anlegen" oder so, bzw vlt sogar, wenn das Häkchen bei Vorgang abschließen ist, auch "Vorgang abschließen"

## 4. Fehlbuchungs-Flow für Nullung mit Gegenbetrag und direktem Abschluss

**Priorität:** hoch

**Grund:** Fachlicher Spezialfall mit eigener Validierungs- und Abschlusslogik; separat umsetzbar.

**Feedback:**

- Ich habe aktuelle eine Fehlbuchung. Diese muss zusammen mit dem Gegenbetrag einfach genullt und abgeschlossen werden können. Fehlbuchungen haben immer: Vorgangstyp "Sonstige", Oberkategorie "Sonstige" Unterkategorie "Fehlbuchung", Sphäre "leer" und können sofort als abgeschlossen markiert werden

## 5. Mail-Senden: Zeilenumbrüche erhalten und Empfängerauswahl ermöglichen

**Priorität:** hoch

**Grund:** Eigenständiger Compose-/Reply-Flow im Mailmodul.

**Feedback:**

- Wenn ich direkt aus dem Tool eine Mail sende, dann werden zeilenumbrüche ignoriert. Ich kann auch nicht auswählen an wen.

## 6. Dashboard-Startseite mit anstehenden Terminen, To-Dos, offenen Vorgängen und Alles-synchronisieren

**Priorität:** mittel

**Grund:** Größerer Oberflächenpunkt mit mehreren Widgets und Startseitenlogik; kein kleines Folgepaket.

**Feedback:**

- Gut wäre, wenn man beim Start ein Dashboard hätte mit anstehenden Terminen, ToDos, offene Vorgänge, usw. UND einen Button mit "alles synchronisieren" Also Mails, Transaktionen vor allem

## 7. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere Dokument-/Zuordnungs-Erweiterung mit fachlichen Folgefragen; nicht Teil des kleinen Pakets.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 8. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Neues größeres Modul mit Konzeptionsbedarf.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.

## 9. Unbekannte Transaktions-ID per HTTP zusätzlich testen

**Priorität:** niedrig

**Grund:** Nützliche Absicherung, aber nicht blockierend und kleiner Nebenpunkt.

**Feedback:**

- Optional zusätzlichen HTTP-Test für unbekannte Transaktions-ID ergänzen.
