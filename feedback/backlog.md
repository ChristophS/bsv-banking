# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Adressdatenbestand für Spendenbescheinigungen fachlich und persistent anlegen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 1

**Priorität:** mittel

**Grund:** Ein stabiler lokaler Empfänger- und Adressbestand ist die Grundlage für spätere Bescheinigungen und muss vor Dokumenterzeugung sowie externer Vereinsintegration abgegrenzt werden.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern.

## 2. Spendenbescheinigungen aus lokalen Empfänger- und Vorgangsdaten erzeugen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Auf Basis eines geprüften Adressbestands soll die eigentliche Dokumenterzeugung als separater, nachvollziehbarer lokaler Schritt erfolgen.

**Feedback:**

- Dann auch eine automatische Erzeugung der Spendenbescheinigung.

## 3. DFBnet-Vereinsdaten für Spendenbescheinigungen als getrennte Leseintegration prüfen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 3

**Priorität:** niedrig

**Grund:** Die DFBnet-Abhängigkeit ist ein eigener externer Integrationsschritt und darf erst nach lokaler Daten- und Dokumentgrundlage mit Mocks oder Fixtures sowie ohne produktive Schreibaktionen umgesetzt werden.

**Feedback:**

- Das wird etwas kompliziert, da es über DFBnet Verein läuft.