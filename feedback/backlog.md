# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Transaktionen splitten und Teilbeträge mehreren Kategorien oder Rechnungen zuordnen

**Priorität:** hoch

**Grund:** Großer Eingriff in Datenmodell, Zuordnungen, UI und Auswertungen; nicht klein genug für das nächste kontrollierte Paket.

**Feedback:**

- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 2. Button-Text und Position beim Vorgangsanlegen aus Mail verbessern

**Priorität:** mittel

**Grund:** Kleiner separater UI-Punkt; sinnvoll, aber nicht so wichtig wie der jetzt ausgewählte arbeitsnahe Mail-Sende-Fehler.

**Feedback:**

- Wenn ich einen Vorgang erstelle kommt das Feld zum wirklichen Erstellen des Vorgangs immer ganz unten das ist oft unpraktikabel wenn man immer runterscrollen muss. und "Bestätigt importieren" ist auch ein komischer Name. Bitte "Vorgang anlegen" oder so, bzw vlt sogar, wenn das Häkchen bei Vorgang abschließen ist, auch "Vorgang abschließen"

## 3. Aktuellste Transaktionen im mailbasierten Vorgangsanlegen verfügbar machen

**Priorität:** hoch

**Grund:** Eigenständiger Kandidaten-/Refresh-Flow im Mail-Vorgangsanlegen und daher getrennt vom Reply-/Senden-Paket behandeln.

**Feedback:**

- Ich habe die transaktionen aktualisiert. wenn ich aber aus einer Mail heraus einen Vorgang erstelle kann ich die ganz aktuellen Transaktionen nicht verknüpfen. Die werden mir gar nicht angezeigt

## 4. Fehlbuchungs-Flow für Nullung mit Gegenbetrag und direktem Abschluss

**Priorität:** hoch

**Grund:** Eigenständiger fachlicher Sonderfall mit Abschlussvalidierung und Klassifikationsregeln; separat umsetzen.

**Feedback:**

- Ich habe aktuelle eine Fehlbuchung. Diese muss zusammen mit dem Gegenbetrag einfach genullt und abgeschlossen werden können. Fehlbuchungen haben immer: Vorgangstyp "Sonstige", Oberkategorie "Sonstige" Unterkategorie "Fehlbuchung", Sphäre "leer" und können sofort als abgeschlossen markiert werden

## 5. Dashboard-Startseite mit anstehenden Terminen, To-Dos, offenen Vorgängen und Alles-synchronisieren

**Priorität:** mittel

**Grund:** Größeres Oberflächenthema mit mehreren Widgets und Zusammenführung bestehender Bereiche; nicht klein genug für dieses Paket.

**Feedback:**

- Gut wäre, wenn man beim Start ein Dashboard hätte mit anstehenden Terminen, ToDos, offene Vorgänge, usw. UND einen Button mit "alles synchronisieren" Also Mails, Transaktionen vor allem

## 6. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere Erweiterung der Zuordnungslogik zwischen Mail, Belegen, Vorgängen und Transaktionen; bewusst getrennt halten.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 7. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Neues größeres Modul mit Konzeptionsbedarf; klar außerhalb eines kleinen nächsten Implementierungspakets.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.

## 8. Unbekannte Transaktions-ID per HTTP zusätzlich testen

**Priorität:** niedrig

**Grund:** Nützliche Absicherung, aber unabhängig vom ausgewählten Paket und mit niedrigerer Priorität.

**Feedback:**

- Optional zusätzlichen HTTP-Test für unbekannte Transaktions-ID ergänzen.
