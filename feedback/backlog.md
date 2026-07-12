# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Dokumente einer Mail innerhalb eines Vorgangs gezielt Transaktionsbezügen zuordnen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Eine Mail mit mehreren Dokumenten und unterschiedlichen Transaktionsbezügen benötigt einen eigenen Vorgangs-, Beleg- und Auswahlflow; direkte Beziehungen zwischen Belegen und Transaktionen dürfen dabei nicht eingeführt werden.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 2. Vorgangsbasierte Auswahl-API für Mail-Dokumentzuordnungen bereitstellen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Nach der fachlichen Zuordnungsdarstellung benötigt die Oberfläche eine klar begrenzte API, um vorhandene Vorgangs-, Transaktions- und Belegverknüpfungen sicher abzufragen und zu ändern.

**Feedback:**

- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

## 3. Mail-Detailansicht für die vorgangsbasierte Dokumentzuordnung umsetzen

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 3

**Priorität:** mittel

**Grund:** Die Zuordnung soll nach stabiler fachlicher Grundlage und API im bestehenden Mail- und Vorgangs-UI bedienbar werden.

**Feedback:**

- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

## 4. Adressdatenbestand für Spendenbescheinigungen fachlich und persistent anlegen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Ein stabiler lokaler Empfänger- und Adressbestand ist die Grundlage für spätere Bescheinigungen und muss vor Dokumenterzeugung sowie externer Vereinsintegration abgegrenzt werden.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern.

## 5. Spendenbescheinigungen aus lokalen Empfänger- und Vorgangsdaten erzeugen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Auf Basis eines geprüften Adressbestands soll die eigentliche Dokumenterzeugung als separater, nachvollziehbarer lokaler Schritt erfolgen.

**Feedback:**

- Dann auch eine automatische Erzeugung der Spendenbescheinigung.

## 6. DFBnet-Vereinsdaten für Spendenbescheinigungen als getrennte Leseintegration prüfen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 3

**Priorität:** niedrig

**Grund:** Die DFBnet-Abhängigkeit ist ein eigener externer Integrationsschritt und darf erst nach lokaler Daten- und Dokumentgrundlage mit Mocks oder Fixtures sowie ohne produktive Schreibaktionen umgesetzt werden.

**Feedback:**

- Das wird etwas kompliziert, da es über DFBnet Verein läuft.