# Nächstes Arbeitspaket

## Titel

Mail-Import um Auswahl vorhandener Transaktionen erweitern

## Ziel

Im bestehenden Mail-Import soll der Nutzer vorhandene Transaktionen aus dem bereits vorhandenen Kandidatenkatalog auswählen und beim Import als links.transaction_ids an den bestehenden POST /api/mail/<inbox_id>/vorgang-import mitsenden, sodass der neu angelegte Vorgang direkt mit Mail und ausgewählten Transaktionen verknüpft wird.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Import-State um transaction_ids erweitern, Kandidaten laden, Auswahl speichern, Rendern der Auswahl und Mitsenden im Import-Request.
- banking_dashboard/static/app.js: Fehleranzeige im bestehenden Import-Flow so nutzen oder ergänzen, dass 4xx-Fehler bei ungültigen transaction_ids sichtbar werden.
- banking_dashboard/static/index.html: Im bestehenden Mail-Import-Bereich eine kleine Mehrfachauswahl oder Checkbox-Liste für vorhandene Transaktionen ergänzen, ohne den restlichen Flow umzubauen.
- banking_dashboard/server.py: Nur kleine Absicherung oder Tests-relevante Fehlerbestätigung, falls nötig; keine neue Fachlogik und keine neuen Endpunkte einführen.
- tests/test_dashboard.py: API-Tests für Mail-Import mit und ohne links.transaction_ids sowie mit ungültiger transaction_id ergänzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Import-UI eine Auswahl vorhandener Transaktionen anbieten, mindestens als einfache Mehrfachauswahl aus candidates.transactions.
- Beim Start des Importdialogs oder an passender bestehender Stelle die Transaktionskandidaten aus /api/vorgaenge/link-candidates laden und im Mail-Import auf candidates.transactions begrenzen.
- Die vom Nutzer ausgewählten IDs als links.transaction_ids an POST /api/mail/<inbox_id>/vorgang-import mitsenden.
- Sicherstellen, dass ein Import ohne Transaktionsauswahl unverändert weiter funktioniert.
- Sicherstellen, dass ungültige oder nicht vorhandene transaction_ids nicht still ignoriert werden, sondern im bestehenden 4xx-Fehlerpfad landen und in der UI sichtbar werden.
- Nach erfolgreichem Import muss der zurückgelieferte Vorgang sowohl die Mail als auch die ausgewählten Transaktionen enthalten.

## Soll umgesetzt werden

- Die Kandidatenliste im Frontend knapp, aber informativ darstellen, z. B. mit Label, Datum, Betrag und optional Klassifikationshinweisen aus classification_missing oder classification_status.
- Wenn ohne größeren Zusatzaufwand möglich, die ausgewählten Transaktionen direkt in der Import-Bestätigung oder der anschließenden angezeigten Vorgangsansicht sichtbar machen, indem die bereits gelieferte vorgang-Response weiterverwendet wird.

## Nicht Teil dieses Arbeitspakets

- Inline-Bearbeitung von Transaktions-Klassifikationsfeldern direkt in derselben Importmaske.
- Generischer Ein-Klick-Workflow für manuelle Vorgangserstellung, Klassifikation und Abschluss.
- Aufteilung mehrerer Dokumente einer Mail auf unterschiedliche Transaktionen innerhalb eines Vorgangs.
- Neue automatische Abschlusslogik.
- Größere Dashboard-Usability-Überarbeitung.

## Akzeptanzkriterien

- Beim Mail-Import kann mindestens eine vorhandene Transaktion ausgewählt werden.
- Der POST auf /api/mail/<inbox_id>/vorgang-import akzeptiert links.transaction_ids im bestehenden Flow und erzeugt den Vorgang mit genau diesen Verknüpfungen.
- Der erzeugte Vorgang zeigt in der Import-Response oder der danach geladenen Detailansicht sowohl die verknüpfte Mail als auch die ausgewählten Transaktionen.
- Ein Import ohne transaction_ids bleibt erfolgreich und regressionsfrei.
- Eine ungültige oder nicht vorhandene transaction_id führt zu einem sauberen 4xx-Fehler statt zu inkonsistenter oder still ignorierter Verknüpfung.

## Hinweise für den Umsetzungs-Agenten

- In server.py ist die fachliche Verdrahtung für links.transaction_ids bereits vorhanden: _mail_vorgang_import liest _list_of_strings(links.get('transaction_ids', [])) und übergibt diese an create_vorgang().
- Die Existenzprüfung sollte bewusst über _replace_vorgang_links() beziehungsweise _replace_link_rows() laufen; dort wird bereits gegen transactions validiert und bei fehlenden IDs LookupError ausgelöst.
- Der GET-Endpunkt /api/vorgaenge/link-candidates liefert den kompletten Kandidatenkatalog. Für dieses Paket sollte im Frontend nur candidates.transactions verwendet werden, ohne Vermischung mit Mails, To-Dos, Belegen oder Terminen.
- Falls die UI bereits einen Import-State für Dokumente, To-Dos und Termine hat, transaction_ids dort analog als weiteres links-Feld einhängen statt einen separaten Parallel-Flow zu bauen.
- Da _mail_vorgang_import nach erfolgreichem Import den detaillierten Vorgang zurückgibt, sollte möglichst diese Response weiterverwendet werden, statt sofort zusätzliche Reload-Requests einzubauen.
- Im Fehlerfall mit ungültiger transaction_id wird der LookupError im RequestHandler aktuell als 404 mit Fehlertext serialisiert; die Tests sollten diesen bestehenden 4xx-Pfad absichern statt eine neue Fehlersemantik zu verlangen.

## Manuelle Testhinweise

- Im Dashboard eine Mail öffnen, den Import starten, eine vorhandene Transaktion auswählen und importieren.
- Nach dem Import den erzeugten Vorgang prüfen: Mail und ausgewählte Transaktion müssen gemeinsam sichtbar sein.
- Den gleichen Flow mit mehreren ausgewählten Transaktionen testen.
- Den gleichen Flow ohne Transaktionsauswahl erneut testen; er muss wie bisher funktionieren.
- Negativtest per API oder UI: nicht existente transaction_id mitsenden und prüfen, dass ein sauberer Fehler angezeigt wird.

## Offene Fragen

- Soll die UI eine einfache Checkbox-/Mehrfachauswahlliste aller geladenen Transaktionskandidaten zeigen, oder ist im bestehenden Dialog bereits ein natürlicher Platz für eine kompakte Kandidatenbox vorgesehen?
- Falls /api/vorgaenge/link-candidates bis zu 250 Transaktionen liefert: reicht für dieses kleine Paket eine ungefilterte Liste, oder braucht die UI minimal eine clientseitige Vorfilterung nach Label?
