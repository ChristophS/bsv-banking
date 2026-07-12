# Backlog

## 1. Klassifikationsvorschläge im Split-Editor an bestehende Kategorien koppeln

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.2

**Priorität:** hoch

**Grund:** Nach der Statusgrundlage benötigen einzelne Split-Zeilen dieselben nutzbaren Vorschläge und Kategorieabhängigkeiten wie die bestehende Transaktionsklassifikation.

**Feedback:**

- existing_backlog
- bekannte Epic-Zuordnung für Split-Klassifikation, Statusableitung und Vorschlagslisten

## 2. Vorgangsstatus unter Berücksichtigung klassifizierter Split-Zeilen ableiten

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.3

**Priorität:** hoch

**Grund:** Die fachliche Statusberechnung soll nach stabiler Split-Klassifikation gezielt in die bestehende vorgangsbasierte Abschlusslogik integriert werden, ohne manuelle Statuswerte zu überschreiben.

**Feedback:**

- existing_backlog
- Klassifikation, Vorschläge und Statusableitung für Split-Zeilen fachlich vervollständigen

## 3. Split-Zeilen innerhalb eines Vorgangs Rechnungen und Teilrechnungen zuordnen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 4

**Priorität:** hoch

**Grund:** Der komplexe Folgeausbau soll eine Transaktion mit mehreren Rechnungen und Rechnungen mit mehreren Kategorien über die bestehende Vorgangs-, Beleg- und Verknüpfungsarchitektur abbilden.

**Feedback:**

- existing_backlog
- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können.

## 4. Dokumente einer Mail innerhalb eines Vorgangs gezielt Transaktionsbezügen zuordnen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Eine Mail mit mehreren Dokumenten und unterschiedlichen Transaktionsbezügen benötigt einen eigenen Vorgangs-, Beleg- und Auswahlflow; direkte Beziehungen zwischen Belegen und Transaktionen dürfen dabei nicht eingeführt werden.

**Feedback:**

- existing_backlog
- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 5. Vorgangsbasierte Auswahl-API für Mail-Dokumentzuordnungen bereitstellen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Nach der fachlichen Zuordnungsdarstellung benötigt die Oberfläche eine klar begrenzte API, um vorhandene Vorgangs-, Transaktions- und Belegverknüpfungen sicher abzufragen und zu ändern.

**Feedback:**

- existing_backlog
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

## 6. Mail-Detailansicht für die vorgangsbasierte Dokumentzuordnung umsetzen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 3

**Priorität:** mittel

**Grund:** Die Zuordnung soll nach stabiler fachlicher Grundlage und API im bestehenden Mail- und Vorgangs-UI bedienbar werden.

**Feedback:**

- existing_backlog
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

## 7. Adressdatenbestand für Spendenbescheinigungen fachlich und persistent anlegen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Ein stabiler lokaler Empfänger- und Adressbestand ist die Grundlage für spätere Bescheinigungen und muss vor Dokumenterzeugung sowie externer Vereinsintegration abgegrenzt werden.

**Feedback:**

- existing_backlog
- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern.

## 8. Spendenbescheinigungen aus lokalen Empfänger- und Vorgangsdaten erzeugen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Auf Basis eines geprüften Adressbestands soll die eigentliche Dokumenterzeugung als separater, nachvollziehbarer lokaler Schritt erfolgen.

**Feedback:**

- existing_backlog
- Dann auch eine automatische Erzeugung der Spendenbescheinigung.

## 9. DFBnet-Vereinsdaten für Spendenbescheinigungen als getrennte Leseintegration prüfen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 3

**Priorität:** niedrig

**Grund:** Die DFBnet-Abhängigkeit ist ein eigener externer Integrationsschritt und darf erst nach lokaler Daten- und Dokumentgrundlage mit Mocks oder Fixtures sowie ohne produktive Schreibaktionen umgesetzt werden.

**Feedback:**

- existing_backlog
- Das wird etwas kompliziert, da es über DFBnet Verein läuft.
