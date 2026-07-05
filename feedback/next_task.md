# Nächstes Arbeitspaket

## Titel

Mail-Import um Auswahl vorhandener Transaktionen erweitern

## Ziel

Im bestehenden Mail-Import soll der Nutzer vorhandene Transaktionen auswählen und direkt mit dem neu angelegten Vorgang verknüpfen können. Der vorhandene Import-Flow bleibt erhalten und wird nur gezielt um die Übergabe von links.transaction_ids ergänzt.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Import-Dialog/Flow um Laden, Anzeigen, Auswählen und Mitsenden von links.transaction_ids erweitern.
- banking_dashboard/static/index.html: Kleine UI-Ergänzung im Mail-Import-Bereich für Transaktionsauswahl, ohne den bestehenden Ablauf neu zu bauen.
- banking_dashboard/server.py: Bestehenden Importpfad nur absichern bzw. unverändert nutzen; insbesondere sicherstellen, dass invalid transaction_ids weiterhin als 4xx sichtbar bleiben.
- tests/test_dashboard.py: API-Tests für /api/mail/<inbox_id>/vorgang-import mit und ohne links.transaction_ids sowie Negativfall ergänzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Import-UI eine Möglichkeit anbieten, mindestens eine vorhandene Transaktion auszuwählen.
- Die Auswahl als links.transaction_ids an POST /api/mail/<inbox_id>/vorgang-import mitsenden.
- Sicherstellen, dass ein Import ohne Transaktionsauswahl unverändert weiter funktioniert.
- Ungültige oder nicht vorhandene transaction_ids müssen als sauberer Fehler zurückgegeben werden, statt still ignoriert zu werden.
- Nach erfolgreichem Import muss der erzeugte Vorgang die verknüpfte Mail und die ausgewählten Transaktionen enthalten.

## Soll umgesetzt werden

- Wenn ohne großen Zusatzaufwand möglich, im Importdialog vorhandene Kandidaten aus /api/vorgaenge/link-candidates verwenden statt neue Backend-Logik einzuführen.
- Nach erfolgreichem Import die verknüpften Transaktionen in der Bestätigung oder geladenen Detailansicht sichtbar machen, sofern der bestehende UI-Flow das bereits nahelegt.

## Nicht Teil dieses Arbeitspakets

- Inline-Bearbeitung von Transaktions-Klassifikationsfeldern direkt in derselben Importmaske.
- Ein generischer Ein-Klick-Workflow für manuelle Vorgangserstellung, Klassifikation und Abschluss.
- Aufteilung mehrerer Dokumente einer Mail auf unterschiedliche Transaktionen innerhalb eines Vorgangs.
- Neue automatische Abschlusslogik oder weitergehende Fachlogik.
- Größere Dashboard-Usability-Überarbeitung.

## Akzeptanzkriterien

- Beim Mail-Import kann mindestens eine vorhandene Transaktion ausgewählt und mit dem neuen Vorgang verknüpft werden.
- Der POST auf /api/mail/<inbox_id>/vorgang-import akzeptiert links.transaction_ids und erzeugt den Vorgang mit genau diesen Verknüpfungen.
- Im erzeugten Vorgang sind Mail und ausgewählte Transaktionen gemeinsam sichtbar.
- Ein Import ohne transaction_ids bleibt erfolgreich und regressionsfrei.
- Ungültige oder nicht vorhandene transaction_ids führen zu einem sauberen 4xx-Fehler statt zu Inkonsistenzen.

## Hinweise für den Umsetzungs-Agenten

- In server.py ist die fachliche Verdrahtung bereits vorhanden: _mail_vorgang_import(...) liest links.transaction_ids via _list_of_strings(...) und reicht sie an create_vorgang(...) weiter. Der Schwerpunkt liegt daher im Frontend und in Tests, nicht in neuer Backend-Fachlogik.
- Die Existenzprüfung der transaction_ids passiert nicht in _list_of_strings(...), sondern in DashboardDataStore._replace_vorgang_links() bzw. _replace_link_rows(); dort erzeugen fehlende IDs ein LookupError mit 404-Antwort. Diesen bestehenden Pfad bewusst testen statt zu umgehen.
- Die Kandidaten-API /api/vorgaenge/link-candidates liefert candidates.transactions mit id, label, date, amount und Klassifikationsmetadaten; für dieses Paket reicht voraussichtlich eine einfache Mehrfachauswahl aus dieser Liste.
- Nach dem Import liefert der Endpunkt bereits den vollständigen Vorgang unter response.vorgang zurück. Diese Antwort möglichst direkt für Anzeige/Bestätigung nutzen statt zusätzlichen Nachladeverkehr einzubauen.

## Manuelle Testhinweise

- Im Dashboard eine Mail öffnen, den Import starten, eine oder mehrere vorhandene Transaktionen auswählen und importieren.
- Nach dem Import den erzeugten Vorgang prüfen: Mail und ausgewählte Transaktionen müssen beide sichtbar sein.
- Den gleichen Flow ohne Transaktionsauswahl erneut testen; er muss wie bisher funktionieren.
- Negativtest per UI oder API: eine nicht existente transaction_id mitsenden und prüfen, dass ein sauberer Fehler angezeigt wird.

## Offene Fragen

- Soll die UI nur die ersten vorhandenen Kandidaten aus /api/vorgaenge/link-candidates anzeigen oder zusätzlich eine einfache Filterung im Frontend anbieten?
- An welcher bestehenden Stelle im Mail-Import-Dialog ist die Transaktionsauswahl am sinnvollsten platzierbar, ohne den Flow zu überladen?
