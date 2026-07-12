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

- SCHEMA_VERSION, Migrationszuordnung und neue Migration in transaction_store/database.py
- Neue Tabelle sowie gekapselte CRUD- und Validierungsfunktionen für Spendenempfänger in transaction_store/database.py
- Optionale typisierte Empfänger-Datenstruktur in transaction_store/models.py
- Öffentliche Exporte vorhandener Store-Funktionen in transaction_store/__init__.py
- Temporäre SQLite-Tests für Schema, Migration, Speichern, Aktualisieren, Auslesen und Validierung in tests/test_transactions.py

## Muss umgesetzt werden

- Die Schema-Version kontrolliert erhöhen und eine vorwärtskompatible Migration für eine lokale Empfängertabelle ergänzen.
- Eine Tabelle für Spendenempfänger mit stabiler Empfänger-ID, nichtleerem Namen beziehungsweise Organisationsnamen sowie strukturierten Anschriftsfeldern anlegen.
- Erstell- und Aktualisierungszeitpunkte speichern.
- Gekapselte Datenzugriffsfunktionen zum Anlegen, Aktualisieren und geordneten Auflisten lokaler Empfänger implementieren.
- Vor dem Speichern mindestens stabile nichtleere Empfänger-ID und nichtleeren Namen validieren sowie Text- und Adresswerte sinnvoll normalisieren.
- Unit-Tests mit temporären SQLite-Datenbanken für Neuanlage, Migration von Schema 17, Speichern, Aktualisieren, geordnetes Auslesen und verständliche Validierungsfehler ergänzen.
- Sicherstellen, dass bestehende Transaktions-, Vorgangs-, Beleg- und Split-Tabellen einschließlich ihrer Verknüpfungen unverändert funktionsfähig bleiben.

## Soll umgesetzt werden

- Feldnamen wählen, die natürliche Personen und Organisationen gleichermaßen abbilden können.
- Die Rückgabewerte der Datenzugriffsfunktionen über eine klare Datenstruktur statt über ungekapselte SQL-Zeilen bereitstellen.
- Die Sortierung der Empfängerliste für eine spätere Dashboard-Verwendung deterministisch festlegen.

## Nicht Teil dieses Arbeitspakets

- Dashboard-Ansicht oder HTTP-API zur Pflege von Empfängeradressen.
- Erzeugung, Vorschau, Export, Ablage oder Versand von Spendenbescheinigungen.
- Automatische Zuordnung von Transaktionen, Belegen oder Vorgängen zu Empfängern.
- Direkte Beziehungen zwischen Empfängern und Transaktionen; spätere fachliche Zuordnungen müssen über Vorgänge erfolgen.
- DFBnet-Zugriff, Browser-Automatisierung, Credential-Verarbeitung oder andere externe Integrationen.
- Import lokaler oder produktiver Adress-, Bank- oder DFBnet-Daten.

## Akzeptanzkriterien

- Eine neue SQLite-Datenbank wird ohne manuelle Schritte initialisiert und enthält die Empfänger-Persistenz.
- Eine Datenbank auf Schema-Version 17 wird beim Öffnen ohne Verlust vorhandener Transaktionsdaten auf das neue Schema migriert.
- Ein lokaler Empfänger mit Name und strukturierten Anschriftsdaten kann angelegt, aktualisiert und wieder ausgelesen werden.
- Die Empfängerliste wird deterministisch geordnet zurückgegeben.
- Ungültige Empfänger ohne nichtleere ID oder ohne nichtleeren Namen werden nicht gespeichert und liefern einen verständlichen Fehler.
- Bestehende Transaktions-, Vorgangs-, Beleg- und Split-Funktionen bleiben durch die Tests nachweislich funktionsfähig.
- Alle neuen Tests laufen ausschließlich mit temporären Datenbanken sowie synthetischen Daten, ohne Netzwerk, Browser, Secrets oder produktive Daten.

## Hinweise für den Umsetzungs-Agenten

- Das vorhandene Schema-Migrationsmuster in transaction_store/database.py verwenden; keine bestehende Tabelle umstrukturieren.
- Empfänger bleiben Stammdaten ohne direkte Transaktionsverknüpfung. Die spätere Dokumentzuordnung wird ausschließlich auf der vorhandenen Vorgangsarchitektur aufbauen.
- Für Zeitstempel das bereits verwendete UTC-Format und für IDs das bestehende stabile Präfix-Konzept verwenden.
- Keine lokalen Belegordner, Konfigurationsdateien oder Secret-Dateien einlesen.

## Manuelle Testhinweise

- Eine neue temporäre Datenbank öffnen und das Vorhandensein der Empfängertabelle sowie der erwarteten Spalten prüfen.
- Eine Beispielorganisation und eine natürliche Beispielperson mit Anschrift anlegen, ändern und erneut auslesen.
- Eine Datenbank mit Schema-Version 17 und vorhandenen Transaktionsdaten öffnen und prüfen, dass die Migration erfolgreich durchläuft.
- Leere Empfänger-ID und leeren Empfängernamen testen und die Fehlermeldungen prüfen.

## Offene Fragen

- Welche rechtlich und fachlich erforderlichen Empfängerfelder sollen für die spätere Bescheinigung verpflichtend sein, insbesondere Land, Anrede und Namensaufteilung?
- Soll die spätere Bescheinigung einen unveränderlichen Adress-Snapshot speichern, damit nachträgliche Stammdatenänderungen alte Bescheinigungen nicht beeinflussen?
