# Nächstes Arbeitspaket

## Titel

Transaktion einem bestehenden Vorgang zuordnen

## Ziel

Im Dashboard soll eine vorhandene Transaktion einem bereits existierenden Vorgang zugeordnet werden können. Dabei sollen bestehende Vorschlags- und Kandidatenmechanismen genutzt werden, ohne einen neuen Vorgang anlegen zu müssen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: dedizierten Link-Flow bzw. eine DataStore-Methode für Transaktion -> bestehender Vorgang ergänzen; außerdem Vorgangsvorschläge für source_type 'transaction' bereitstellen.
- banking_dashboard/static/app.js: Transaktionsdetailansicht um Anzeige passender bestehender Vorgänge, Auswahl und Link-Aktion erweitern.
- banking_dashboard/static/index.html: falls nötig Container/Platzhalter für den Zuordnungsbereich in der Transaktionsdetailansicht ergänzen.
- tests/test_dashboard.py: API- und UI-nahe Tests für Zuordnung, Vorschläge, Idempotenz und Fehlerfälle ergänzen.

## Muss umgesetzt werden

- Eine Transaktion muss über die Backend-Schicht einem bestehenden Vorgang zugeordnet werden können, ohne bestehende Links unbeabsichtigt zu löschen.
- Für eine geöffnete Transaktion müssen passende bestehende Vorgänge vorgeschlagen werden.
- Die Transaktionsdetailansicht muss die neue Vorgangsverknüpfung nach erfolgreicher Zuordnung sofort anzeigen.
- Unbekannte oder ungültige Vorgangs-IDs müssen einen sauberen Fehler liefern.
- Automatisierte Tests für Erfolgsfall, wiederholte Zuordnung und Fehlerfall ergänzen.

## Soll umgesetzt werden

- Wenn im bestehenden UI einfach möglich, Vorschläge vor allgemeinen Kandidaten anzeigen.
- Doppelte Zuordnungen im UI abfangen oder idempotent behandeln.
- Bei bereits bestehender Verknüpfung eine stille Erfolgsreaktion oder klare idempotente Meldung statt Fehler verwenden.

## Nicht Teil dieses Arbeitspakets

- Transaktionensplitting oder Teilbeträge
- Automatische finale Auswahl des richtigen Vorgangs
- Neue Zuordnungstabelle oder neues Datenmodell
- Komplexe Matching- oder ML-Logik
- Mehrere Dokumente aus einer Mail unterschiedlichen Transaktionen zuordnen

## Akzeptanzkriterien

- In der Transaktionsansicht kann eine vorhandene Transaktion einem bereits existierenden Vorgang zugeordnet werden, ohne einen neuen Vorgang anzulegen.
- Die Zuordnung verwendet die bestehende relationale Struktur und erzeugt keine redundante Parallelstruktur.
- Bestehende Verknüpfungen der Transaktion bleiben erhalten; die Transaktion kann danach mehreren Vorgängen zugeordnet sein.
- Für eine geöffnete Transaktion werden passende bestehende Vorgänge vorgeschlagen.
- Ungültige Vorgangs-IDs führen zu einem sauberen Fehler.
- Tests decken Erfolgsfall, idempotenten Wiederholungsfall und Fehlerfall ab.

## Hinweise für den Umsetzungs-Agenten

- Wichtig: update_vorgang ersetzt in _replace_vorgang_links alle Link-Listen. Für einen Link aus der Transaktionsansicht daher nicht blind ein partielles Update auf einen Vorgang verwenden, ohne bestehende transaction_ids mitzulesen.
- Ein kleiner dedizierter API-Endpunkt oder eine DataStore-Methode für 'link transaction to vorgang' ist naheliegender als ein Sonderfall im bestehenden Vorgang-Update.
- Die vorhandene suggest_related_entities-Methode kennt source_type 'transaction', liefert aber derzeit keine Zielgruppe 'vorgaenge'; diese Methode gezielt erweitern statt einen parallelen Vorschlagsmechanismus einzubauen.
- Für Vorgangsvorschläge vorhandene Vorgangsfelder wie Titel, Beschreibung, Vorgangstyp und verknüpfte Transaktionsbegriffe nutzen.

## Manuelle Testhinweise

- Im Dashboard eine Transaktion öffnen, die bisher nur ihren auto-erzeugten Vorgang hat.
- Einen bestehenden Vorgang auswählen und die Transaktion zuordnen.
- Prüfen, dass danach beide Vorgänge in der Transaktionsansicht sichtbar sind.
- Prüfen, dass der bestehende Vorgang in seiner Detailansicht die zusätzliche Transaktion zeigt.
- Dieselbe Zuordnung erneut ausführen und verifizieren, dass kein Duplikat entsteht.
- Vorschläge bei einer Transaktion mit aussagekräftigem Verwendungszweck prüfen.

## Offene Fragen

- Soll der auto-erzeugte Standardvorgang einer Transaktion später manuell entfernt oder zusammengeführt werden können?
