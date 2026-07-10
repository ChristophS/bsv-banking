# Nächstes Arbeitspaket

## Titel

Aktuellste Transaktionen im Mail-Vorgangsanlegen frisch nachladen

## Ziel

Beim Anlegen eines Vorgangs aus einer Mail sollen die auswählbaren Transaktionen immer auf dem aktuellen Serverstand basieren, damit neu importierte Kontobewegungen ohne Dashboard-Neustart sofort verfügbar sind.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_dashboard.py
- tests/test_mail_integration.py
- transaction_store/database.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Stelle finden, an der der Mail-Vorgangsdialog Kandidaten lädt oder cached, und dort vor dem Öffnen bzw. vor dem Absenden gezielt einen frischen Abruf auslösen.
- banking_dashboard/server.py: nur falls für den bestehenden /api/vorgaenge/link-candidates-Endpunkt eine kleine Ergänzung nötig ist; bevorzugt die vorhandene API wiederverwenden.
- tests/test_dashboard.py: Serverseitige Absicherung, dass Kandidatenlisten aus dem aktuellen Datenstand kommen.
- tests/test_mail_integration.py: Flow-Test für den Mail-Vorgang, damit neue Transaktionen nach Import in der Auswahl sichtbar sind.

## Muss umgesetzt werden

- Sicherstellen, dass der Mail-Flow zum Vorgangsanlegen die Transaktionskandidaten frisch vom Server lädt statt einen alten Initialstand im Frontend weiterzuverwenden.
- Prüfen, wo in app.js die Kandidaten für den Mail-Importdialog befüllt werden, und dort einen erneuten Abruf von /api/vorgaenge/link-candidates oder einem bereits vorhandenen äquivalenten Fetch auslösen.
- Die bestehende Verknüpfungslogik über links.transaction_ids und den Import-POST /api/mail/<id>/vorgang-import unverändert lassen.
- Mindestens einen Test ergänzen, der zeigt, dass Kandidatenlisten nach einem neuen Import nicht auf einem alten Snapshot festhängen.

## Soll umgesetzt werden

- Falls im Dialog bereits ein kleines Reload-Muster existiert, dieses konsistent auch für die Transaktionsliste nutzen.
- Einen kleinen Ladezustand oder eine klare Fehlermeldung anzeigen, falls das Nachladen scheitert.

## Nicht Teil dieses Arbeitspakets

- Button-Text oder Position beim Vorgangsanlegen aus Mail verbessern.
- Transaktionen splitten oder Teilbeträge mehreren Kategorien/Rechnungen zuordnen.
- Fehlbuchungs-Flow für Nullung mit Gegenbetrag und direktem Abschluss.
- Dashboard-Startseite mit Widgets und Alles-synchronisieren.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Integration.
- Zusätzlicher HTTP-Test für unbekannte Transaktions-ID.

## Akzeptanzkriterien

- Wenn nach dem Dashboard-Start neue Transaktionen importiert werden, zeigt der Mail-Dialog zum Vorgangsanlegen diese Transaktionen bei der nächsten Öffnung der Auswahl an.
- Die Auswahl aktueller Transaktionen im Mail-Vorgangsanlegen basiert auf einem frischen Serverabruf und nicht nur auf einem alten Initialzustand im Frontend.
- Das bestehende Verknüpfen ausgewählter transaction_ids in _mail_vorgang_import funktioniert weiterhin unverändert.
- Andere Kandidatenlisten oder Vorgangsfunktionen werden durch die Änderung nicht sichtbar verschlechtert.
- Tests decken die Aktualisierung der Kandidatenliste mindestens auf Server- oder Flow-Ebene ab.

## Hinweise für den Umsetzungs-Agenten

- In server.py existiert bereits GET /api/vorgaenge/link-candidates; dieser liefert data_store.link_candidate_catalog() und ist der naheliegende Wiederverwendungspunkt.
- Die Ursache ist sehr wahrscheinlich Frontend-seitig: Kandidaten werden in app.js einmal geladen und für den Mail-Importdialog wiederverwendet. Dort nachschärfen statt Backend duplizieren.
- Falls app.js einen globalen Kandidaten-Cache hält, sollte er vor dem Mail-Vorgangsanlegen invalidiert oder gezielt für transactions neu geladen werden.
- Die Transaktionskandidaten kommen aus _transaction_link_candidates(), das auf normalized_transactions zugreift und bis zu 250 Einträge liefert; diese bestehende Logik nicht parallel nachbauen.
- Falls ein automatischer Refresh beim Öffnen des Dialogs zu aufwendig wäre, ist auch ein kleiner expliziter Reload-Schritt im Dialog akzeptabel, solange das Kernproblem gelöst wird.

## Manuelle Testhinweise

- Dashboard starten und den Mail-Reiter öffnen.
- Eine Mail auswählen, aus der ein Vorgang angelegt werden soll.
- Separat 'Aktuelle Kontobewegungen anfordern' ausführen und neue Transaktionen importieren.
- Danach ohne Dashboard-Neustart erneut den Mail-Vorgangsanlegen-Dialog öffnen.
- Prüfen, dass die frisch importierte Transaktion in der Auswahl erscheint und erfolgreich verknüpft werden kann.

## Offene Fragen

- Soll die Kandidatenliste beim Öffnen des Mail-Dialogs immer automatisch neu geladen werden, oder ist ein expliziter kleiner Aktualisieren-Schritt im Dialog besser anschlussfähig?
