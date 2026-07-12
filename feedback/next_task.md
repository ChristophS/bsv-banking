# Nächstes Arbeitspaket

## Titel

Lokalen Adressdatenbestand für Spendenempfänger persistent anlegen

## Epic

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 1

## Ziel

Eine migrationsfähige, lokale Persistenzgrundlage für Spendenempfänger mit vollständigen Adressdaten schaffen, damit spätere Spendenbescheinigungen nachvollziehbar aus Empfänger- und Vorgangsdaten erstellt werden können.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/__init__.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- Schema-Version und Migrationen in transaction_store/database.py
- Neue Tabelle und Datenzugriffsfunktionen für lokale Spendenempfänger in transaction_store/database.py
- Optionale typisierte Datenstruktur in transaction_store/models.py
- Unit-Tests für Migration, Speichern, Lesen und Validierung in tests/test_transactions.py

## Muss umgesetzt werden

- Eine migrationsfähige lokale Tabelle für Spendenempfänger anlegen, mit stabiler Empfänger-ID sowie mindestens Name beziehungsweise Organisation und strukturierten Anschriftfeldern.
- Datenzugriffsfunktionen zum Anlegen, Aktualisieren und geordneten Auflisten lokaler Empfänger implementieren.
- Eingaben vor dem Speichern validieren, insbesondere nichtleere stabile IDs und einen nichtleeren Empfängernamen; Adressfelder dürfen nur sinnvoll normalisiert gespeichert werden.
- Die Erweiterung in die bestehende SQLite-Initialisierung und das bestehende Migrationsverfahren integrieren, ohne vorhandene Tabellen oder Verknüpfungen umzubauen.
- Unit-Tests mit temporärer SQLite-Datenbank für Neuanlage, Migration bestehender Datenbanken, Speichern, Aktualisieren, Auslesen und Validierungsfehler ergänzen.

## Soll umgesetzt werden

- Die Feldnamen so wählen, dass sie für natürliche Personen und Organisationen gleichermaßen geeignet sind.
- Erstell- und Aktualisierungszeitpunkte speichern, damit spätere Bescheinigungen den verwendeten lokalen Datenbestand nachvollziehbar referenzieren können.
- Die Datenzugriffsfunktionen so kapseln, dass ein späterer API- oder Dashboard-Schritt keine direkten SQL-Abfragen duplizieren muss.

## Nicht Teil dieses Arbeitspakets

- Dashboard-Ansicht oder API zur Pflege von Empfängeradressen.
- Erzeugung, Vorschau, Export oder Versand von Spendenbescheinigungen.
- Automatische Zuordnung von Transaktionen, Belegen oder Vorgängen zu Empfängern.
- Direkte Beziehungen zwischen Empfängern und Transaktionen außerhalb der bestehenden Vorgangsarchitektur.
- DFBnet-Zugriff, Browser-Automatisierung, Credential-Verarbeitung oder sonstige externe Integrationen.
- Import produktiver Adress-, Bank- oder DFBnet-Daten.

## Akzeptanzkriterien

- Eine neue Datenbank kann ohne manuelle Schritte initialisiert werden und enthält die Empfänger-Persistenz.
- Eine Datenbank auf dem bisherigen Schema wird beim Öffnen zuverlässig auf das neue Schema migriert.
- Ein lokaler Empfänger mit Name und Anschrift kann gespeichert, aktualisiert und wieder ausgelesen werden.
- Ungültige Empfänger ohne erforderlichen Namen werden nicht gespeichert und liefern einen verständlichen Fehler.
- Bestehende Transaktions-, Vorgangs-, Beleg- und Split-Tabellen sowie ihre Verknüpfungen bleiben unverändert funktionsfähig.
- Die neuen Tests laufen ohne Netzwerk, Browser, Secrets oder produktive Daten erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Die Empfängerdaten bleiben lokal in der gemeinsamen Transaktionsdatenbank und folgen dem vorhandenen SQLite-Migrationsmuster.
- Noch keine direkte Transaktion-zu-Empfänger-Beziehung einführen; eine spätere fachliche Zuordnung muss über bestehende Vorgänge und deren Verknüpfungsstrukturen geplant werden.
- Keine Daten aus lokalen Verzeichnissen, Secrets-Dateien oder externen Systemen einlesen.
- Für Tests ausschließlich temporäre Datenbanken und synthetische Empfängerdaten verwenden.

## Manuelle Testhinweise

- Eine neue temporäre Datenbank öffnen und prüfen, dass die Empfängertabelle angelegt wird.
- Einen Beispielspender beziehungsweise eine Beispielorganisation mit Anschrift anlegen, ändern und erneut auslesen.
- Eine Datenbank mit altem Schema öffnen und prüfen, dass die Migration ohne Verlust bestehender Transaktionsdaten durchläuft.
- Prüfen, dass ein leerer Empfängername abgewiesen wird.

## Offene Fragen

- Welche rechtlich und fachlich erforderlichen Empfängerfelder sollen für die spätere Bescheinigung verpflichtend sein, insbesondere Land, Anrede und Namensaufteilung?
- Soll die spätere Bescheinigung einen unveränderlichen Adress-Snapshot speichern, damit nachträgliche Stammdatenänderungen alte Bescheinigungen nicht beeinflussen?
