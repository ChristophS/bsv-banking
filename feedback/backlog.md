# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Spendenbescheinigungen aus lokalen Empfänger- und Vorgangsdaten erzeugen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Nach der stabilen lokalen Empfänger-Persistenz soll die eigentliche Dokumenterzeugung als eigener, nachvollziehbarer Schritt umgesetzt werden. Die Zuordnung muss dabei die bestehende Vorgangsarchitektur verwenden.

**Feedback:**

- Dann auch eine automatische Erzeugung der Spendenbescheinigung.

## 2. DFBnet-Vereinsdaten für Spendenbescheinigungen als getrennte Leseintegration prüfen

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 3

**Priorität:** niedrig

**Grund:** Eine mögliche DFBnet-Abhängigkeit ist ein eigenständiger externer Integrationsschritt. Sie darf erst nach lokaler Empfänger- und Dokumentgrundlage mit Mocks oder Fixtures und ohne produktive Schreibaktionen bewertet und umgesetzt werden.

**Feedback:**

- Das wird etwas kompliziert, da es über DFBnet Verein läuft.
