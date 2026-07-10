# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Klassifikation, Vorschläge und Statusableitung für Split-Zeilen fachlich vervollständigen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3

**Priorität:** hoch

**Grund:** Nach dem Split-Editor muss die fachliche Logik für einzelne Teilbeträge in die bestehende Klassifikation und Statusberechnung integriert werden.

**Feedback:**

- existing_backlog
- bekannte Epic-Zuordnung für Split-Klassifikation, Statusableitung und Vorschlagslisten

## 2. Transaktionen fachlich auf mehrere Rechnungen und Teilrechnungen aufteilen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 4

**Priorität:** hoch

**Grund:** Komplexerer Folgeausbau des Split-Epics für mehrere Rechnungen und Teilrechnungen auf Basis stabiler Split-Persistenz, UI und Statuslogik.

**Feedback:**

- existing_backlog
- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 3. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Eigenständiger Mail-/Dokumenten-/Vorgangsflow mit separatem Zuordnungs- und UI-Bedarf, unabhängig vom Split-Epic.

**Feedback:**

- existing_backlog
- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 4. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Großes eigenständiges Vorhaben mit Datenmodell-, Dokumenten- und externer Integrationskomplexität; sollte zunächst fachlich und technisch in Teilpakete zerlegt werden.

**Feedback:**

- existing_backlog
- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.