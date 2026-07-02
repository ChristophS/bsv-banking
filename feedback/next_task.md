# Nächstes Arbeitspaket

## Titel

Mail-Import um Auswahl vorhandener Transaktionen erweitern

## Ziel

Im bestehenden Mail-Import soll der Nutzer vorhandene Transaktionen auswählen und direkt mit dem neu angelegten Vorgang verknüpfen können. Der bestehende Import-Flow bleibt dabei erhalten und wird nur gezielt um die Übergabe von transaction_ids ergänzt.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Import-Dialog/Flow um Auswahl und Mitgabe von links.transaction_ids erweitern.
- banking_dashboard/static/index.html: Kleine UI-Ergänzung für die Anzeige/Auswahl verknüpfbarer Transaktionen im Mail-Import.
- banking_dashboard/server.py: Mail-Import-Endpoint auf robuste Validierung und Weitergabe von transaction_ids prüfen.
- tests/test_dashboard.py: API- und Integrations-Tests für Mail-Import mit transaction_ids ergänzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Import-UI eine Möglichkeit anbieten, vorhandene Transaktionen auszuwählen.
- Die ausgewählten Transaktionen als links.transaction_ids an den bestehenden Import-Endpunkt übergeben.
- Sicherstellen, dass der Import ohne ausgewählte Transaktionen weiterhin unverändert funktioniert.
- Ungültige transaction_ids müssen über die vorhandene Validierung sauber abgewiesen werden.

## Soll umgesetzt werden

- Nach erfolgreichem Import die verknüpften Transaktionen im Ergebnis oder in der Detailansicht sichtbar machen, sofern der bestehende Flow das einfach hergibt.
- Wenn im UI ohne großen Aufwand möglich, vorhandene Vorschlagsdaten aus dem Backend statt einer neuen Suchlogik nutzen.

## Nicht Teil dieses Arbeitspakets

- Direkte Bearbeitung von Transaktions-Klassifikationsfeldern innerhalb derselben Importmaske.
- Ein neuer generischer One-Click-Workflow für manuelle Vorgangserstellung aus beliebigen UI-Bereichen.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Automatisches Abschließen über neue Fachlogik hinaus.
- Große Dashboard-Usability-Überarbeitungen.

## Akzeptanzkriterien

- Beim Mail-Import kann mindestens eine vorhandene Transaktion ausgewählt und mit dem neuen Vorgang verknüpft werden.
- Der POST auf /api/mail/<inbox_id>/vorgang-import akzeptiert links.transaction_ids weiterhin und erzeugt den Vorgang mit genau diesen Verknüpfungen.
- Im erzeugten Vorgang sind Mail und ausgewählte Transaktionen gemeinsam sichtbar.
- Ein Import ohne transaction_ids bleibt erfolgreich und regressionsfrei.
- Ungültige oder nicht vorhandene transaction_ids führen zu einem sauberen Fehler statt zu stillen Inkonsistenzen.

## Hinweise für den Umsetzungs-Agenten

- Der Backend-Pfad _mail_vorgang_import(...) in server.py unterstützt links.transaction_ids bereits; der Hauptaufwand liegt voraussichtlich im Frontend-Flow.
- Für die Auswahl vorhandener Transaktionen zuerst prüfen, ob der bestehende Kandidatenkatalog /api/vorgaenge/link-candidates für den Mail-Import ausreicht.
- Die bestehende Rückgabe von create_vorgang(...) bzw. vorgang_detail(...) enthält bereits Transaktionsdetails und kann für die UI-Bestätigung wiederverwendet werden.
- Keine Sonderbehandlung für automatisch erzeugte Standardvorgänge entfernen oder umgehen.

## Manuelle Testhinweise

- Im Dashboard eine Mail öffnen, den Import starten, eine oder mehrere bestehende Transaktionen auswählen und importieren.
- Nach dem Import den erzeugten Vorgang öffnen und prüfen, dass Mail und Transaktionen verknüpft sind.
- Prüfen, dass derselbe Flow ohne Transaktionsauswahl weiterhin funktioniert.

## Offene Fragen

- Welcher bestehende UI-Baustein im Mail-Import ist am geeignetsten für die Transaktionsauswahl?
- Soll die UI nur Vorschläge anzeigen oder zusätzlich freie Auswahl aus allen verfügbaren Transaktionen erlauben?
