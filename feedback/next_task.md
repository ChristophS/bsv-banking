# Nächstes Arbeitspaket

## Titel

Manuelles To-Do-Anlegen in der mailbasierten Vorgangsanlage auch ohne Vorschlag ermöglichen

## Ziel

Im Flow zum Anlegen eines Vorgangs aus einer Mail soll mindestens ein To-Do immer manuell angelegt und mit dem neuen Vorgang importiert werden können, auch wenn die Analyse keine To-Do-Vorschläge liefert.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: UI-Zustand und Rendering der To-Do-Sektion in der Mail-Vorgangsanlage erweitern, damit auch ohne Analysevorschläge ein manuell erfassbarer To-Do-Eintrag vorhanden ist bzw. hinzugefügt werden kann.
- banking_dashboard/static/index.html: nur falls ein zusätzlicher Container/Button/Leerzustand im bestehenden Mail-Vorgangsanlage-Dialog notwendig ist.
- banking_dashboard/server.py: Import-Flow nur soweit absichern, dass manuell erfasste todos mit enabled/title/description/due_date/priority wie bestehende Vorschläge akzeptiert werden; voraussichtlich keine große Backend-Änderung nötig.
- tests/test_dashboard.py: API-/Import-Tests für den Fall ergänzen, dass analysis keine todos liefert, der Import-Payload aber manuell hinzugefügte todos enthält und diese korrekt angelegt/verknüpft werden.
- tests/test_mail_integration.py: nur prüfen/ergänzen, falls bestehende Tests Annahmen treffen, dass To-Dos ausschließlich aus Vorschlägen stammen.

## Muss umgesetzt werden

- Im Mail-zu-Vorgang-UI sicherstellen, dass der Nutzer auch bei leerer analysis.todos mindestens ein To-Do manuell erfassen kann.
- Die manuell erfassten To-Do-Felder müssen in denselben Import-Payload unter todos einfließen wie vorgeschlagene To-Dos.
- Der Import muss ein manuell angelegtes To-Do mit dem neu erzeugten Vorgang verknüpfen.
- Der Fall 'keine Vorschläge, aber manuelles To-Do' darf nicht durch UI-Logik blockiert werden.
- Leere oder unvollständige manuell hinzugefügte To-Dos sollen wie bisher defensiv behandelt werden, also nur mit Titel importiert werden bzw. leere Einträge ignoriert werden.

## Soll umgesetzt werden

- Im UI einen klaren Leerzustand für die To-Do-Sektion anzeigen, z. B. sinngemäß 'Keine Vorschläge' plus Möglichkeit zum manuellen Hinzufügen.
- Falls bereits mehrere To-Dos unterstützt werden, sollte auch manuell mehr als ein To-Do ergänzt werden können; nur wenn das mit kleiner Änderung in die bestehende Struktur passt.
- Sicherstellen, dass Priorität und Fälligkeit bei manuell angelegten To-Dos dieselben Defaults/Validierungen wie im restlichen UI verwenden.

## Nicht Teil dieses Arbeitspakets

- Automatische To-Do-Erkennung verbessern.
- Manuelles To-Do-Anlegen in anderen Bereichen außerhalb der mailbasierten Vorgangsanlage.
- Neuer allgemeiner To-Do-Editor oder separate Dialoge.
- Vorgangsvorschläge für Transaktionen.
- Mehrere Mail-Anhänge sichtbar machen.
- Aktuellste Transaktionen im Mail-Flow nachladen.

## Akzeptanzkriterien

- Wenn die Mailanalyse keine To-Do-Vorschläge liefert, kann der Nutzer im Vorgangsanlage-Flow trotzdem mindestens ein To-Do mit Titel eingeben.
- Beim Import wird dieses To-Do in der Tabelle todos angelegt und über todo_vorgaenge mit dem neuen Vorgang verknüpft.
- Der Import funktioniert weiterhin unverändert, wenn Analysevorschläge vorhanden sind.
- Leere manuell angelegte To-Do-Zeilen führen nicht zu einem Fehler und werden nicht als defekte Datensätze gespeichert.
- Bestehende Mail-Vorgangsanlage für Dokumente, Termine, Transaktionsverknüpfungen und direkten Abschluss wird durch die Änderung nicht regressiv beeinträchtigt.

## Hinweise für den Umsetzungs-Agenten

- In server.py verarbeitet _mail_vorgang_import bereits payload['todos']; der Engpass ist sehr wahrscheinlich primär die Frontend-Erfassung in app.js.
- Die Backend-Importlogik erwartet pro To-Do u. a. title, description, due_date, priority und optional enabled. Dieses Format sollte das Frontend auch für manuelle Einträge wiederverwenden.
- Wenn im UI bisher nur analysis.todos gerendert wird, sollte die Datenstruktur beim Öffnen des Importdialogs so initialisiert werden, dass sie unabhängig von Vorschlägen bearbeitbar bleibt.
- Beim Import werden To-Dos mit source='automatic' und source_reference=inbox_id erstellt. Diesen bestehenden Pfad beibehalten, statt für manuelle Einträge aus dem Mail-Import eine Sonderbehandlung einzubauen.
- Falls es bereits Helper zum Sammeln/Sanitizen der Importsektionen gibt, diese wiederverwenden statt neue parallele Payload-Logik einzuführen.

## Manuelle Testhinweise

- Mail mit Analyse ohne To-Do-Vorschläge öffnen, Vorgangsanlage starten, manuell ein To-Do eintragen, importieren, dann prüfen, dass es im neuen Vorgang und im To-Do-Reiter sichtbar ist.
- Mail mit vorhandenen To-Do-Vorschlägen öffnen und zusätzlich manuell ergänzen; prüfen, dass beide importiert werden können.
- Leeren manuellen To-Do-Eintrag stehen lassen und importieren; prüfen, dass der Import nicht fehlschlägt und kein leeres To-Do entsteht.
- Optional direkten Vorgangsabschluss im selben Flow testen, um sicherzustellen, dass die neue To-Do-UI den restlichen Importdialog nicht stört.

## Offene Fragen

- Unterstützt die bestehende UI-Struktur bereits mehrere bearbeitbare To-Do-Zeilen, oder sollte dieses Paket aus Stabilitätsgründen nur genau einen zusätzlichen manuellen Eintrag absichern?
- Gibt es in app.js schon wiederverwendbare Renderer/State-Helper für todos aus dem Analyseergebnis, die auch für leere Initialzustände genutzt werden können?
