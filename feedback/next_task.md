# Nächstes Arbeitspaket

## Titel

Split-Grundlagen im Dashboard sichtbar und validierbar machen

## Ziel

Die bereits vorhandene Tabelle `transaction_splits` in einen kleinen, nutzbaren Vorbereitungs-Workflow überführen: Split-Daten pro Transaktion im Dashboard lesbar machen und einfache Split-Erfassung mit Summenvalidierung ermöglichen, ohne den vollständigen Rechnungs-/Mehrvorgangs-Workflow schon umzusetzen.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_dashboard.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- transaction_store/database.py: kleine Repository-/Hilfsfunktionen zum Lesen, Anlegen und Ersetzen von `transaction_splits` ergänzen; Summenvalidierung gegen `transactions.amount_minor` zentral umsetzen.
- banking_dashboard/server.py: Transaktionsdetail-API um Split-Daten erweitern und einen kleinen POST/PUT-Endpunkt für Split-Speicherung bereitstellen.
- banking_dashboard/static/app.js: Transaktionsdetailansicht um einen einfachen Split-Bereich ergänzen, der bestehende Splits anzeigt und bearbeitbar macht.
- tests/test_dashboard.py: API- und Dashboard-Verhalten für Split-Anzeige und Split-Speicherung absichern.
- tests/test_transactions.py: datenbanknahe Validierung und Persistenz der Split-Summen testen.

## Muss umgesetzt werden

- Eine repo-interne Datenzugriffsfunktion ergänzen, die alle Splits einer Transaktion in stabiler Reihenfolge lädt.
- Eine Speicherfunktion ergänzen, die die Split-Liste einer Transaktion atomar ersetzt und vorher validiert, dass die Summe der `amount_minor` exakt dem Originalbetrag der Transaktion entspricht.
- Die Split-Erfassung sowohl für positive als auch negative Transaktionsbeträge korrekt validieren.
- Die Transaktionsdetail-Antwort im Dashboard so erweitern, dass vorhandene Splits mit ihren Klassifikationsfeldern, Beschreibung und optionaler `vorgangs_id` zurückgegeben werden.
- Einen kleinen API-Endpunkt für Split-Speicherung bereitstellen, der bei fehlerhafter Summe oder unbekannter Transaktion klaren 4xx-Fehler liefert.
- Im Frontend in der Transaktionsdetailansicht einen einfachen bearbeitbaren Split-Bereich bereitstellen: Zeilen hinzufügen, löschen, Betrag und Klassifikationsfelder erfassen, dann speichern.
- Im Frontend die verbleibende Differenz zur Originaltransaktion sichtbar machen und Speichern bei nicht ausgeglichener Summe verhindern oder klar fehlschlagen lassen.

## Soll umgesetzt werden

- Bei leeren Split-Listen die Splits vollständig entfernen können.
- Vorhandene `created_at`/`updated_at` der Tabelle zunächst einfach mitlaufen lassen, ohne daraus ein eigenes UI-Feature zu machen.
- Falls bereits passende Serialisierungshelfer im Server existieren, Split-Ausgabe daran angleichen statt neues Formatwildwuchs einzuführen.

## Nicht Teil dieses Arbeitspakets

- Vollständiger fachlicher Workflow 'eine Transaktion, mehrere Rechnungen, Rechnungen mit eigenen Teilkategorien'.
- Komfortfunktionen zur Dokumentzuordnung pro Split oder pro Rechnung.
- Automatische Vorgangserzeugung oder komplexe Neuverknüpfung von Splits mit mehreren Vorgängen.
- Neue Tabellen für Rechnungen oder Split-Historien.
- Backlog-Punkt 'mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen'.
- Backlog-Punkt 'Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration'.
- Expliziter Migrationstest 13->14 und die Modellfrage zu `created_at`/`updated_at` als separates Folgepaket.

## Akzeptanzkriterien

- Für eine Transaktion mit gespeicherten `transaction_splits` liefert die Transaktionsdetail-API die Split-Liste inklusive Beträgen und Klassifikationsfeldern zurück.
- Gültige Split-Liste, deren Summe exakt dem Originalbetrag entspricht, wird gespeichert und ist nach erneutem Laden unverändert sichtbar.
- Ungültige Split-Liste mit Summendifferenz wird serverseitig abgewiesen.
- Die Speicherung arbeitet ohne neue Tabellen und nutzt ausschließlich die bestehende Tabelle `transaction_splits`.
- Bestehende Transaktions- und Vorgangsansichten funktionieren weiterhin für Transaktionen ohne Splits.

## Hinweise für den Umsetzungs-Agenten

- Dieses Paket ist bewusst ein Vorbereitungsschritt des großen Split-Backlogpunkts: Ziel ist nicht der komplette Fachworkflow, sondern ein belastbarer minimaler CRUD- und Validierungsweg auf der vorhandenen Tabelle.
- Da `transaction_splits.vorgangs_id` bereits existiert, kann das Feld in API und UI mitgeführt werden, muss aber nicht funktional ausgeschöpft werden; keine automatische Vorgangslogik daraus ableiten.
- Die Summenprüfung sollte zentral im Backend stattfinden, nicht nur im Frontend.
- Wenn die Detail-API heute Transaktionsdaten serialisiert, dort Split-Daten anhängen statt einen isolierten Parallel-Detailfluss zu schaffen.
- Falls `models.py` bereits Datentypen für Dashboard-Antworten enthält, Split-Strukturen dort konsistent ergänzen; falls nicht, kein großes neues Modellkonzept bauen.

## Manuelle Testhinweise

- Dashboard öffnen, Transaktion auswählen, Split-Bereich prüfen.
- Zwei Split-Zeilen anlegen, deren Summe genau dem Transaktionsbetrag entspricht, speichern und Detailansicht neu laden.
- Danach absichtlich eine falsche Summe speichern und prüfen, dass eine verständliche Fehlermeldung erscheint.
- Mit einer Ausgabe-Transaktion (negativer Betrag) und einer Einnahme-Transaktion (positiver Betrag) testen.
- Prüfen, dass Transaktionen ohne Splits weiterhin unverändert dargestellt werden.

## Offene Fragen

- Soll bei einer vollständig gesplitteten Transaktion die Transaktionsklassifikation auf Root-Ebene später leer bleiben dürfen oder vorerst unabhängig von den Splits bestehen bleiben? Für dieses Paket sollte die bestehende Root-Klassifikation unverändert bleiben.
- Soll die UI Beträge in Euro mit Vorzeichen erfassen und erst serverseitig in `amount_minor` umrechnen, oder existiert bereits ein etablierter Formatierungs-/Parsing-Helper im Frontend, der wiederverwendet werden sollte?
