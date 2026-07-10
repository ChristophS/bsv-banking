# Nächstes Arbeitspaket

## Titel

Dashboard-Grundlage für Transaktions-Splits nutzbar machen

## Ziel

Die bereits vorhandene Split-Persistenz im Dashboard so sichtbar und bedienbar machen, dass Splits in der Transaktionsdetailansicht angezeigt, bearbeitet und mit klaren Fehlermeldungen gespeichert werden können. Dies ist die kleine technische Grundlage für den späteren vollständigen Split-Workflow.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- transaction_store/database.py
- transaction_store/models.py
- tests/test_dashboard.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/index.html: Bereich in der Transaktionsdetailansicht für Split-Anzeige und Bearbeitung ergänzen.
- banking_dashboard/static/app.js: Laden der vorhandenen Splits aus den Transaktionsdetails, Formularzustand für mehrere Split-Zeilen, PUT-Request an /api/transactions/<id>/splits, Anzeige von Validierungs- und Serverfehlern.
- banking_dashboard/server.py: Falls nötig kleine Ergänzungen an Fehlermeldungen oder Response-Form, aber keine neue Architektur; Kernendpunkt ist bereits vorhanden.
- transaction_store/database.py: Nur falls sich bei Tests zeigt, dass Validierungsfehler zu unklar sind oder Randfälle in replace_transaction_splits noch nicht sauber abgefangen werden.
- tests/test_dashboard.py: API- und Dashboard-bezogene Tests für Split-Anzeige und Speicherung ergänzen.
- tests/test_transactions.py: Persistenz- oder Validierungsverhalten der Split-Ersetzung absichern, falls noch nicht abgedeckt.

## Muss umgesetzt werden

- In der Transaktionsdetailansicht vorhandene Splits sichtbar machen, inklusive Betrag, Beschreibung, Klassifikationsfeldern und optionaler vorgangs_id, soweit bereits vom Backend geliefert.
- Eine einfache Bearbeitungsmöglichkeit für mehrere Split-Zeilen im bestehenden UI ergänzen, inklusive Hinzufügen und Entfernen von Zeilen.
- Beim Speichern die bestehende PUT-API verwenden und nach Erfolg die Transaktionsdetails neu laden oder den lokalen Detailzustand konsistent aktualisieren.
- Fehlermeldungen aus dem Backend im UI sichtbar machen, insbesondere bei ungültiger Payload oder fachlicher Validierung.
- Mindestens einen Test ergänzen, der nachweist, dass Split-Daten in transaction detail zurückkommen und per PUT gespeichert werden können.

## Soll umgesetzt werden

- Betragsfelder im UI klar als Euro darstellen, intern aber an das Backend als betrag_cent senden, passend zur bestehenden API.
- Vor dem Senden einfache Client-Validierung ergänzen, zum Beispiel Pflicht auf ganzzahlige Centbeträge bzw. keine komplett leeren Split-Zeilen.
- Im UI kenntlich machen, dass es sich um eine Grundlage handelt und noch kein vollständiger Rechnungs- oder Mehrvorgangs-Workflow umgesetzt wird.

## Nicht Teil dieses Arbeitspakets

- Automatische Aufteilung einer Transaktion auf mehrere Vorgänge anhand von Dokumenten oder Mails.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen zuordnen.
- Spendenbescheinigungs-Modul oder DFBnet-Vereinsintegration.
- Migrationstest von Schema-Version 13 auf 14.
- Entscheidung, ob TransactionSplit created_at/updated_at fachlich erweitert oder verändert werden soll, sofern nicht für diese UI-Nutzung zwingend notwendig.

## Akzeptanzkriterien

- Beim Laden einer Transaktion mit vorhandenen Splits enthält die Detailansicht diese Split-Liste sichtbar im Dashboard.
- Ein Nutzer kann in der Detailansicht mindestens zwei Split-Zeilen erfassen, speichern und nach erneutem Laden unverändert wiedersehen.
- Ein Nutzer kann bestehende Splits komplett ersetzen, indem die UI den vorhandenen Replace-Mechanismus nutzt.
- Ungültige Requests führen nicht zu stillem Scheitern; stattdessen zeigt die Oberfläche eine verständliche Fehlermeldung.
- Vorhandene Transaktionsklassifikation, Vorgangsanzeige und andere Detailbereiche bleiben funktionsfähig.

## Hinweise für den Umsetzungs-Agenten

- Die bestehende Serverlogik serialisiert Splits bereits mit betrag/betrag_cent, Klassifikationsfeldern, vorgangs_id sowie erstellt_am/aktualisiert_am; die UI sollte genau diese Felder konsumieren statt ein eigenes Format zu erfinden.
- Da der Endpunkt replace_transaction_splits semantisch vollständiges Ersetzen bedeutet, sollte das Frontend immer die vollständige aktuelle Split-Liste senden und nicht versuchen, einzelne Splits inkrementell zu patchen.
- Wenn die Datenbanklogik bereits Summen- oder Konsistenzvalidierung macht, sollte das Frontend diese Fehlermeldungen möglichst direkt anzeigen statt eigene Fachlogik zu duplizieren.
- Transaktionsdetails werden bereits zentral über /api/transactions/<id> geladen; die Split-UI möglichst in diesen bestehenden Detailflow einhängen.
- Falls Tests Fixtures mit transaction_splits noch nicht anlegen, bestehende Testdatenbank-Helfer in tests/test_dashboard.py bzw. tests/test_transactions.py erweitern statt neue Testinfrastruktur zu bauen.

## Manuelle Testhinweise

- Dashboard starten, eine Transaktion öffnen und prüfen, ob ein leerer oder befüllter Split-Bereich sichtbar ist.
- Zwei Splits mit unterschiedlichen Kategorien anlegen, speichern, Detailansicht schließen und neu öffnen und die Persistenz prüfen.
- Einen offensichtlichen Fehler provozieren, zum Beispiel ungültigen Betrag oder fachlich unzulässige Summe, und prüfen, ob die Fehlermeldung im UI erscheint.
- Prüfen, dass die normale Klassifikationsbearbeitung derselben Transaktion weiterhin funktioniert.

## Offene Fragen

- Welche fachliche Validierung erzwingt replace_transaction_splits aktuell genau, insbesondere ob die Summe der Split-Beträge exakt dem Transaktionsbetrag entsprechen muss. Falls diese Regel bereits implementiert ist, sollte die UI-Texthilfe daran angepasst werden; falls nicht, bleibt die Validierung zunächst backendgeführt.
- Soll vorgangs_id in dieser ersten UI-Version frei editierbar sein oder nur angezeigt werden? Für das kleine Paket ist Anzeige ausreichend, Bearbeitung nur falls im bestehenden UI mit vertretbarem Aufwand anschließbar.
