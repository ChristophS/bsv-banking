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

- banking_dashboard/static/app.js: Mail-Import-State um Laden, Speichern, Rendern und Mitsenden ausgewählter transaction_ids erweitern.
- banking_dashboard/static/app.js: Bestehenden Import-Request fuer /api/mail/<inbox_id>/vorgang-import so anpassen, dass links.transaction_ids nur bei Auswahl mitgesendet oder als leere Liste uebergeben werden.
- banking_dashboard/static/app.js: Bestehende Anzeige des Importergebnisses bzw. der geladenen Vorgangsansicht nutzen, damit die verknuepften Transaktionen nach Erfolg sichtbar werden.
- banking_dashboard/static/index.html: Im bestehenden Mail-Import-Bereich eine kleine Mehrfachauswahl oder Checkbox-Liste fuer vorhandene Transaktionen ergaenzen, ohne den restlichen Flow umzubauen.
- banking_dashboard/server.py: Nur falls noetig kleine Absicherung oder Fehlerpfad bestaetigen; keine neue Fachlogik oder neue Endpunkte einfuehren.
- tests/test_dashboard.py: API-Tests fuer Mail-Import mit und ohne links.transaction_ids sowie mit ungueltiger transaction_id ergaenzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Import-UI eine Auswahl vorhandener Transaktionen anbieten, mindestens als einfache Mehrfachauswahl aus candidates.transactions.
- Beim Start des Importdialogs oder an passender bestehender Stelle die Transaktionskandidaten aus /api/vorgaenge/link-candidates laden und fuer den Mail-Import auf transactions begrenzen.
- Die vom Nutzer gewaehlteten IDs als links.transaction_ids an POST /api/mail/<inbox_id>/vorgang-import mitsenden.
- Sicherstellen, dass ein Import ohne Transaktionsauswahl unveraendert weiter funktioniert.
- Ungueltige oder nicht vorhandene transaction_ids duerfen nicht still ignoriert werden; der bestehende 4xx-Fehlerpfad soll in Tests abgesichert und in der UI sichtbar gemacht werden.
- Nach erfolgreichem Import muss der zurueckgelieferte Vorgang sowohl die Mail als auch die ausgewaehlten Transaktionen enthalten.

## Soll umgesetzt werden

- Wenn ohne groesseren Zusatzaufwand moeglich, die ausgewaehlten Transaktionen direkt in der Import-Bestaetigung oder der anschliessend angezeigten Vorgangsansicht sichtbar machen, indem die bereits gelieferte vorgang-Response weiterverwendet wird.
- Die Kandidatenliste im Frontend knapp, aber informativ darstellen, z. B. mit Label, Datum, Betrag und optional Klassifikationshinweisen aus classification_missing oder classification_status.

## Nicht Teil dieses Arbeitspakets

- Inline-Bearbeitung von Transaktions-Klassifikationsfeldern direkt in derselben Importmaske.
- Generischer Ein-Klick-Workflow fuer manuelle Vorgangserstellung, Klassifikation und Abschluss.
- Aufteilung mehrerer Dokumente einer Mail auf unterschiedliche Transaktionen innerhalb eines Vorgangs.
- Neue automatische Abschlusslogik.
- Groessere Dashboard-Usability-Ueberarbeitung.

## Akzeptanzkriterien

- Beim Mail-Import kann mindestens eine vorhandene Transaktion ausgewaehlt werden.
- Der POST auf /api/mail/<inbox_id>/vorgang-import akzeptiert links.transaction_ids im bestehenden Flow und erzeugt den Vorgang mit genau diesen Verknuepfungen.
- Der erzeugte Vorgang zeigt in der Import-Response oder der danach geladenen Detailansicht sowohl die verknuepfte Mail als auch die ausgewaehlten Transaktionen.
- Ein Import ohne transaction_ids bleibt erfolgreich und regressionsfrei.
- Eine ungueltige oder nicht vorhandene transaction_id fuehrt zu einem sauberen 4xx-Fehler statt zu inkonsistenter oder still ignorierter Verknuepfung.

## Hinweise für den Umsetzungs-Agenten

- In server.py ist die fachliche Verdrahtung fuer links.transaction_ids bereits vorhanden: _mail_vorgang_import liest _list_of_strings(links.get('transaction_ids', [])) und uebergibt diese an create_vorgang().
- Die Existenzpruefung sollte bewusst ueber _replace_vorgang_links()/_replace_link_rows() laufen; dort wird bereits gegen transactions validiert und bei fehlenden IDs LookupError ausgeloest.
- Der GET-Endpunkt /api/vorgaenge/link-candidates liefert den kompletten Kandidatenkatalog. Fuer dieses Paket sollte im Frontend nur candidates.transactions verwendet werden, ohne Vermischung mit Mails, To-Dos, Belegen oder Terminen.
- Falls die UI bereits einen Import-State fuer Dokumente, To-Dos und Termine hat, transaction_ids dort analog als weiteres links-Feld einhaengen statt einen separaten Parallel-Flow zu bauen.
- Da _mail_vorgang_import nach erfolgreichem Import den detailierten Vorgang zurueckgibt, sollte moeglichst diese Response weiterverwendet werden, statt sofort zusaetzliche Reload-Requests einzubauen.
- Im Fehlerfall mit ungueltiger transaction_id wird der LookupError im RequestHandler aktuell als 404 mit Fehlertext serialisiert; die Tests sollten diesen bestehenden 4xx-Pfad absichern statt eine neue Fehlersemantik zu verlangen.

## Manuelle Testhinweise

- Im Dashboard eine Mail oeffnen, den Import starten, eine vorhandene Transaktion auswaehlen und importieren.
- Nach dem Import den erzeugten Vorgang pruefen: Mail und ausgewaehlte Transaktion muessen gemeinsam sichtbar sein.
- Den gleichen Flow mit mehreren ausgewaehlten Transaktionen testen.
- Den gleichen Flow ohne Transaktionsauswahl erneut testen; er muss wie bisher funktionieren.
- Negativtest per API oder UI: nicht existente transaction_id mitsenden und pruefen, dass ein sauberer Fehler angezeigt wird.

## Offene Fragen

- Soll die UI eine einfache Checkbox-/Mehrfachauswahlliste aller geladenen Transaktionskandidaten zeigen, oder ist im bestehenden Dialog bereits ein natuerlicher Platz fuer eine kompakte Kandidatenbox vorgesehen?
- Falls /api/vorgaenge/link-candidates bis zu 250 Transaktionen liefert: reicht fuer dieses kleine Paket eine ungefilterte Liste, oder braucht die UI minimal eine clientseitige Vorfilterung nach Label?
