# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Split-Editor in der Transaktionsdetailansicht des Dashboards umsetzen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 2

**Priorität:** hoch

**Grund:** Nach der Persistenz- und API-Grundlage wird eine kleine UI benötigt, um Split-Zeilen interaktiv anzulegen, zu bearbeiten und zu löschen.

**Feedback:**

- existing_backlog
- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können.

## 2. Klassifikation, Vorschläge und Statusableitung für Split-Zeilen fachlich vervollständigen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3

**Priorität:** hoch

**Grund:** Auf der technischen Split-Grundlage müssen die fachlichen Klassifikations- und Statusregeln für einzelne Teilbeträge sauber in die bestehende Logik integriert werden.

**Feedback:**

- existing_backlog
- bekannte Epic-Zuordnung für Split-Klassifikation, Statusableitung und Vorschlagslisten

## 3. Transaktionen fachlich auf mehrere Rechnungen und Teilrechnungen aufteilen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 4

**Priorität:** hoch

**Grund:** Weiterführender Ausbau desselben Split-Vorhabens mit komplexeren Zuordnungsfällen auf Basis der Split-Klassifikation; sollte erst nach stabiler fachlicher Split-Statuslogik umgesetzt werden.

**Feedback:**

- existing_backlog
- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 4. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Eigenständiger Mail-/Dokumenten-/Vorgangsflow mit separatem Zuordnungs- und UI-Bedarf; unabhängig vom Split-Epic.

**Feedback:**

- existing_backlog
- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 5. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Großes eigenständiges Vorhaben mit Datenmodell-, Dokumenten- und externer Integrationskomplexität; sollte zunächst separat fachlich konzipiert werden.

**Feedback:**

- existing_backlog
- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.
