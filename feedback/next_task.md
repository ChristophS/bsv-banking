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

- banking_dashboard/static/app.js: Mail-Import-Dialog/State um Laden, Rendern, Auswählen und Mitsenden von transaction_ids erweitern.
- banking_dashboard/static/index.html: kleine UI-Ergänzung im bestehenden Mail-Import-Bereich für Mehrfachauswahl vorhandener Transaktionen.
- banking_dashboard/server.py: nur falls nötig kleine Absicherung oder Response-/Fehlerpfad unverändert belassen; keine neue Fachlogik einführen.
- tests/test_dashboard.py: API-Tests für erfolgreichen Import mit und ohne links.transaction_ids sowie Negativfall mit ungültiger transaction_id ergänzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Import-UI eine Möglichkeit anbieten, mindestens eine vorhandene Transaktion auszuwählen.
- Die Auswahl als links.transaction_ids an POST /api/mail/<inbox_id>/vorgang-import mitsenden.
- Sicherstellen, dass ein Import ohne Transaktionsauswahl unverändert weiter funktioniert.
- Ungültige oder nicht vorhandene transaction_ids müssen als sauberer 4xx-Fehler sichtbar werden und dürfen nicht still ignoriert werden.
- Nach erfolgreichem Import muss der erzeugte Vorgang die verknüpfte Mail und die ausgewählten Transaktionen enthalten.

## Soll umgesetzt werden

- Wenn ohne großen Zusatzaufwand möglich, die Transaktionsliste im Importdialog aus /api/vorgaenge/link-candidates laden statt neue Backend-Endpunkte einzuführen.
- Nach erfolgreichem Import die verknüpften Transaktionen in der Bestätigung oder direkt in der geladenen Vorgangsansicht sichtbar machen, sofern der bestehende UI-Flow das bereits nahelegt.

## Nicht Teil dieses Arbeitspakets

- Inline-Bearbeitung von Transaktions-Klassifikationsfeldern direkt in derselben Importmaske
- Generischer Ein-Klick-Workflow für manuelle Vorgangserstellung, Klassifikation und Abschluss
- Aufteilung mehrerer Dokumente einer Mail auf unterschiedliche Transaktionen innerhalb eines Vorgangs
- Neue automatische Abschlusslogik
- Größere Dashboard-Usability-Überarbeitung

## Akzeptanzkriterien

- Beim Mail-Import kann mindestens eine vorhandene Transaktion ausgewählt und mit dem neuen Vorgang verknüpft werden.
- Der POST auf /api/mail/<inbox_id>/vorgang-import akzeptiert links.transaction_ids und erzeugt den Vorgang mit genau diesen Verknüpfungen.
- Im erzeugten Vorgang sind Mail und ausgewählte Transaktionen gemeinsam sichtbar.
- Ein Import ohne transaction_ids bleibt erfolgreich und regressionsfrei.
- Ungültige oder nicht vorhandene transaction_ids führen zu einem sauberen 4xx-Fehler statt zu Inkonsistenzen.

## Hinweise für den Umsetzungs-Agenten

- Der Schwerpunkt liegt voraussichtlich im Frontend und in Tests; server.py enthält die fachliche Verdrahtung bereits weitgehend.
- Nicht _list_of_strings(...) erweitern, um Existenzprüfungen nachzubauen; der bestehende Prüfpfad in DashboardDataStore._replace_vorgang_links() bzw. _replace_link_rows() soll bewusst genutzt werden.
- Für die UI reicht wahrscheinlich eine einfache Mehrfachauswahl aus candidates.transactions mit id, label, date, amount und ggf. Klassifikationshinweisen.
- Nach erfolgreichem Import möglichst die bereits gelieferte response.vorgang-Struktur weiterverwenden, statt sofort zusätzliche Reload-Requests einzubauen.
- Darauf achten, dass beim Laden von Link-Kandidaten keine unnötige Vermischung mit anderen Entitätstypen entsteht; für dieses Paket ist nur transactions relevant.

## Manuelle Testhinweise

- Im Dashboard eine Mail öffnen, den Import starten, eine oder mehrere vorhandene Transaktionen auswählen und importieren.
- Nach dem Import den erzeugten Vorgang prüfen: Mail und ausgewählte Transaktionen müssen beide sichtbar sein.
- Den gleichen Flow ohne Transaktionsauswahl erneut testen; er muss wie bisher funktionieren.
- Negativtest per UI oder API: eine nicht existente transaction_id mitsenden und prüfen, dass ein sauberer Fehler angezeigt wird.

## Offene Fragen

- Soll die UI nur eine einfache Liste bzw. Mehrfachauswahl der ersten Kandidaten anzeigen, oder ist bereits eine kleine Filterung im Frontend sinnvoll?
- An welcher bestehenden Stelle im Mail-Import-Dialog ist die Transaktionsauswahl am sinnvollsten platzierbar, ohne den Flow zu überladen?
