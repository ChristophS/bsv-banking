# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Klassifikationsvorschläge für Split-Zeilen kontextabhängig bereitstellen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.2

**Priorität:** hoch

**Grund:** Nach der sichtbaren Statusableitung sollen Split-Zeilen dieselben fachlich sinnvollen Vorschläge für Transaktionstyp, Ober- und Unterkategorie sowie Sphäre erhalten wie der bestehende Klassifikationsflow, ohne bereits gespeicherte Eingaben zu überschreiben.

**Feedback:**

- existing_backlog
- bekannte Epic-Zuordnung für Split-Klassifikation und Vorschlagslisten

## 2. Split-Klassifikation in Vorgangsstatus und Abschlusslogik integrieren

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.3

**Priorität:** hoch

**Grund:** Ein Vorgang mit klassifizierten Teilbeträgen muss fachlich konsistent bewertet werden. Dies ist erst nach stabiler Split-Statusableitung und Eingabeunterstützung sinnvoll und darf bestehende manuelle Vorgangsstatus nicht überschreiben.

**Feedback:**

- existing_backlog
- bekannte Epic-Zuordnung für Split-Statusableitung

## 3. Split-Zeilen regelgestützt klassifizieren

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.4

**Priorität:** mittel

**Grund:** Die vorhandene Regelverwaltung soll erst nach stabilen Split-Feldern, Statussemantik und Vorgangsfolgen gezielt für unklassifizierte Split-Zeilen erweitert werden. Manuelle oder teilweise Eingaben müssen dabei weiterhin gegen automatische Überschreibung geschützt sein.

**Feedback:**

- existing_backlog
- Klassifikation einzelner Splits ist Teil der bekannten Split-Epic-Zuordnung

## 4. Transaktionen fachlich auf mehrere Rechnungen und Teilrechnungen aufteilen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 4

**Priorität:** hoch

**Grund:** Komplexerer Folgeausbau des Split-Epics für mehrere Rechnungen und Teilrechnungen auf Basis stabiler Split-Persistenz, UI und Statuslogik. Die Zuordnung muss über die bestehenden Vorgänge und Vorgang-Beleg-Verknüpfungen erfolgen.

**Feedback:**

- existing_backlog
- Ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können.
- Eine Transaktion - eine Rechnung - Teilsummen auf mehrere Kategorien/Unterkategorien.
- Eine Transaktion - mehrere Rechnungen, im Extremfall mit verschiedenen Kategorien/Unterkategorien innerhalb der Rechnungen.

## 5. Bestehende Mail-Anhänge und Dokumente eines Vorgangs transparent ermitteln

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente innerhalb eines Vorgangs zuordnen

**Epic-Ziel:** Mehrere Dokumente aus einer Mail über Vorgänge nachvollziehbar unterschiedlichen Transaktionen zuordnen, ohne direkte Dokument-Transaktionsbeziehungen einzuführen.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Für die spätere unterschiedliche Zuordnung mehrerer Dokumente einer Mail müssen zunächst die bereits bestehenden Mail-, Beleg- und Vorgangsverknüpfungen in einer gemeinsamen Vorgangsansicht lesbar zusammengeführt werden.

**Feedback:**

- existing_backlog
- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang.

## 6. Mail-Dokumente über Vorgänge den passenden Transaktionen zuordnen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente innerhalb eines Vorgangs zuordnen

**Epic-Ziel:** Mehrere Dokumente aus einer Mail über Vorgänge nachvollziehbar unterschiedlichen Transaktionen zuordnen, ohne direkte Dokument-Transaktionsbeziehungen einzuführen.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Auf Basis einer transparenten Vorgangsansicht soll für jedes Dokument eine gezielte Zuordnung über den passenden Vorgang möglich werden. Direkte Beziehungen zwischen Belegen und Transaktionen sind architektonisch ausgeschlossen.

**Feedback:**

- existing_backlog
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

## 7. Zuordnungsworkflow für mehrere Mail-Dokumente und Transaktionen prüfen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente innerhalb eines Vorgangs zuordnen

**Epic-Ziel:** Mehrere Dokumente aus einer Mail über Vorgänge nachvollziehbar unterschiedlichen Transaktionen zuordnen, ohne direkte Dokument-Transaktionsbeziehungen einzuführen.

**Teilpaket:** Teil 3

**Priorität:** niedrig

**Grund:** Nach der Einzelzuordnung muss der Workflow für mehrere Dokumente und mehrere Transaktionen im selben Vorgang mit konsistenter Anzeige, Entfernen und Wiederherstellen von Vorgangsverknüpfungen abgesichert werden.

**Feedback:**

- existing_backlog
- Das Ganze ist ein Vorgang.

## 8. Adressdatenbasis für Spendenbescheinigungen und bisherige Empfänger planen und anlegen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Adress- und Vereinsdaten unterstützen

**Epic-Ziel:** Spendenempfänger strukturiert verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen, wobei eine spätere DFBnet-Vereinsintegration sicher und getrennt bleibt.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Eine wiederverwendbare, datensparsame Adressdatenbasis ist die Voraussetzung für Bescheinigungen. Sie muss separat vom bestehenden Transaktions-, Beleg- und Vorgangsmodell ergänzt werden, ohne produktive externe Daten abzurufen.

**Feedback:**

- existing_backlog
- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern.

## 9. Lokale Spendenbescheinigung aus Adress- und Vorgangsdaten erzeugen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Adress- und Vereinsdaten unterstützen

**Epic-Ziel:** Spendenempfänger strukturiert verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen, wobei eine spätere DFBnet-Vereinsintegration sicher und getrennt bleibt.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Nach einer stabilen Empfängerdatenbasis kann ein überprüfbarer lokaler Entwurf für Spendenbescheinigungen erzeugt werden. Die fachliche Herkunft von Beträgen und Belegen bleibt über die bestehenden Vorgänge nachvollziehbar.

**Feedback:**

- existing_backlog
- Dann auch eine automatische Erzeugung der Spendenbescheinigung.

## 10. DFBnet-Vereinsdaten für Spendenbescheinigungen als getrennte, sichere Integration konzipieren

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Adress- und Vereinsdaten unterstützen

**Epic-Ziel:** Spendenempfänger strukturiert verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen, wobei eine spätere DFBnet-Vereinsintegration sicher und getrennt bleibt.

**Teilpaket:** Teil 3

**Priorität:** niedrig

**Grund:** Die erwähnte DFBnet-Abhängigkeit ist ein eigenständiger externer Integrationsschritt. Vor einer Umsetzung müssen zulässige Daten, manueller Ablauf, lokale Speicherung und Mock-basierte Tests abgegrenzt werden; es dürfen keine produktiven Aktionen automatisiert werden.

**Feedback:**

- existing_backlog
- Das wird etwas kompliziert, da es über DFBnet Verein läuft.
