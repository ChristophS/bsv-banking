# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Transaktionen splitten und Teilbeträge mehreren Kategorien oder Rechnungen zuordnen

**Priorität:** hoch

**Grund:** Großer Eingriff in Datenmodell, Zuordnungen, UI und Auswertungen; nicht klein genug für das nächste kontrollierte Arbeitspaket.

**Feedback:**

- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 2. Fehlbuchungs-Flow für Nullung mit Gegenbetrag und direktem Abschluss

**Priorität:** hoch

**Grund:** Eigenständiger fachlicher Sonderfall mit Abschlussregeln und Validierungsfolgen; besser als separates Paket umsetzen.

**Feedback:**

- Ich habe aktuelle eine Fehlbuchung. Diese muss zusammen mit dem Gegenbetrag einfach genullt und abgeschlossen werden können. Fehlbuchungen haben immer: Vorgangstyp "Sonstige", Oberkategorie "Sonstige" Unterkategorie "Fehlbuchung", Sphäre "leer" und können sofort als abgeschlossen markiert werden

## 3. Dashboard-Startseite mit anstehenden Terminen, To-Dos, offenen Vorgängen und Alles-synchronisieren

**Priorität:** mittel

**Grund:** Größeres Oberflächenthema mit Startseitenstruktur und mehreren Widgets; nicht klein genug für dieses Paket.

**Feedback:**

- Gut wäre, wenn man beim Start ein Dashboard hätte mit anstehenden Terminen, ToDos, offene Vorgänge, usw. UND einen Button mit "alles synchronisieren" Also Mails, Transaktionen vor allem

## 4. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere Erweiterung der bestehenden Zuordnungslogik zwischen Mail, Vorgängen, Dokumenten und Transaktionen.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 5. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Neues größeres Modul mit erheblichem Konzeptionsbedarf und externer Integration.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.

## 6. Unbekannte Transaktions-ID per HTTP zusätzlich testen

**Priorität:** niedrig

**Grund:** Nützliche zusätzliche Absicherung, aber unabhängig vom gewählten UI-Arbeitspaket.

**Feedback:**

- Optional zusätzlichen HTTP-Test für unbekannte Transaktions-ID ergänzen.
