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

- banking_dashboard/static/app.js: Mail-Import-State um links.transaction_ids erweitern, Kandidaten beim Öffnen/Laden holen, Auswahl halten und in den bestehenden Request-Payload integrieren.
- banking_dashboard/static/app.js: Renderlogik im Mail-Import um einen kleinen Auswahlbereich für candidates.transactions ergänzen; Anzeige knapp mit Label/Datum/Betrag/Klassifikationshinweis.
- banking_dashboard/static/index.html: im bestehenden Mail-Import-Bereich einen Container/Platzhalter für die Transaktionsauswahl ergänzen, ohne Dialogstruktur neu zu bauen.
- banking_dashboard/server.py: voraussichtlich keine große Fachlogik nötig; nur falls Tests eine kleine Absicherung oder Fehlersichtbarkeit am Import-Endpunkt verlangen.
- tests/test_dashboard.py: API-Tests für Import mit transaction_ids, ohne transaction_ids und mit ungültiger transaction_id ergänzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Import-UI eine Auswahl vorhandener Transaktionen anbieten, mindestens als einfache Mehrfachauswahl oder Checkbox-Liste auf Basis von candidates.transactions.
- Beim Öffnen oder Initialisieren des Mail-Import-Dialogs die Daten aus /api/vorgaenge/link-candidates laden und im Import-UI ausschließlich candidates.transactions verwenden.
- Die vom Nutzer ausgewählten IDs als links.transaction_ids an POST /api/mail/<inbox_id>/vorgang-import mitsenden.
- Sicherstellen, dass ein Import ohne ausgewählte Transaktionen unverändert erfolgreich bleibt.
- Sicherstellen, dass ungültige oder nicht existente transaction_ids nicht still ignoriert werden, sondern in den bestehenden 4xx-Fehlerpfad laufen und im Frontend sichtbar werden.
- Nach erfolgreichem Import muss der zurückgelieferte Vorgang die verknüpfte Mail und die ausgewählten Transaktionen enthalten.

## Soll umgesetzt werden

- Die Transaktionskandidaten im Frontend knapp, aber informativ darstellen, z. B. mit Label, Datum, Betrag und sichtbarem Hinweis auf fehlende oder vorhandene Klassifikation.
- Wenn im bestehenden UI ohne Zusatzaufwand möglich, die ausgewählten Transaktionen direkt in der Import-Bestätigung bzw. der danach angezeigten Vorgangsansicht sichtbar machen, indem die vorhandene vorgang-Response genutzt wird.

## Nicht Teil dieses Arbeitspakets

- Inline-Bearbeitung von Klassifikationsfeldern einer ausgewählten Transaktion direkt im Mail-Import.
- Generischer Ein-Klick-Workflow für manuelle Vorgangserstellung, Klassifikation und Abschluss.
- Zuordnung verschiedener Dokumente einer Mail zu unterschiedlichen Transaktionen innerhalb desselben Vorgangs.
- Neue automatische Abschlusslogik oder Änderungen an Completion-Regeln.
- Größere UX- oder Layout-Überarbeitung des Dashboards.

## Akzeptanzkriterien

- Beim Mail-Import kann mindestens eine vorhandene Transaktion ausgewählt werden.
- Der POST auf /api/mail/<inbox_id>/vorgang-import akzeptiert im bestehenden Flow links.transaction_ids und erzeugt den Vorgang mit genau diesen Transaktionsverknüpfungen.
- Der erzeugte Vorgang zeigt in der Import-Response oder der anschließenden Detailansicht sowohl die verknüpfte Mail als auch die ausgewählten Transaktionen.
- Ein Import ohne transaction_ids bleibt erfolgreich und regressionsfrei.
- Eine ungültige oder nicht vorhandene transaction_id führt zu einem sauberen 4xx-Fehler statt zu still ignorierter oder inkonsistenter Verknüpfung.

## Hinweise für den Umsetzungs-Agenten

- In server.py ist die fachliche Verarbeitung bereits vorhanden: _mail_vorgang_import übergibt transaction_ids aus links.transaction_ids an create_vorgang(...).
- Die Existenzprüfung sollte bewusst über _replace_vorgang_links bzw. _replace_link_rows laufen; dort wird gegen transactions validiert und bei fehlenden IDs LookupError ausgelöst.
- GET /api/vorgaenge/link-candidates liefert den kompletten Katalog. Für dieses Paket im Frontend nur candidates.transactions verwenden, ohne Vermischung mit Mails, To-Dos, Belegen oder Terminen.
- Falls app.js bereits einen Import-State für documents, todos, termine und links hält, transaction_ids dort als weiteres links-Feld analog einhängen statt einen separaten Sonderpfad zu bauen.
- Da _mail_vorgang_import bereits den detaillierten Vorgang zurückgibt, möglichst diese Response weiterverwenden statt zusätzliche Reload-Requests einzubauen.
- Der bestehende Fehlerpfad serialisiert LookupError als 404 mit Fehlertext. Tests sollten diese Semantik absichern, nicht eine neue Fehlerklasse verlangen.

## Manuelle Testhinweise

- Im Dashboard eine Mail öffnen, den Import starten, eine vorhandene Transaktion auswählen und importieren.
- Nach dem Import den erzeugten Vorgang prüfen: Mail und ausgewählte Transaktion müssen gemeinsam sichtbar sein.
- Den Flow mit mehreren ausgewählten Transaktionen testen.
- Den Flow ohne Transaktionsauswahl erneut testen; er muss wie bisher funktionieren.
- Negativtest per API oder UI: nicht existente transaction_id mitsenden und prüfen, dass ein sauberer Fehler angezeigt wird.

## Offene Fragen

- Soll die UI eine einfache Checkbox-Liste oder eine Mehrfachauswahlliste verwenden, abhängig davon, was sich am natürlichsten in den bestehenden Importbereich einfügt?
- Falls bis zu 250 Transaktionskandidaten geladen werden: reicht für dieses kleine Paket zunächst eine ungefilterte Liste, oder ist im vorhandenen UI mit geringem Aufwand eine kleine clientseitige Filterung sinnvoll?
