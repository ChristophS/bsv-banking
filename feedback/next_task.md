# Nächstes Arbeitspaket

## Titel

Kartenklick für nicht zugewiesene anstehende Termine auf expliziten Unzugewiesen-Filter führen

## Ziel

Der Überblickskarten-Klick für „Nicht zugewiesene anstehende Termine“ soll die Terminansicht nicht nur allgemein öffnen, sondern direkt auf eine Liste einschränken, die nur geplante, zukünftige und keinem Vorgang zugeordnete Termine zeigt.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: `list_termine()` und/oder der GET-Endpunkt `/api/termine`, um einen zusätzlichen expliziten Filter für nicht zugewiesene Termine anzunehmen.
- banking_dashboard/static/app.js: Kartenklick-Handling für Overview-Cards sowie Laden/Filtern der Terminliste anpassen, damit beim Klick auf `unassigned_termine` der neue Filter gesetzt und verwendet wird.
- banking_dashboard/static/index.html: nur falls für den Filterzustand ein vorhandenes UI-Element ergänzt oder beschriftet werden muss; möglichst minimal halten.
- tests/test_dashboard.py: API- und ggf. End-to-End-nahe Dashboard-Tests für den neuen Terminfilter und das Kartenverhalten ergänzen oder anpassen.

## Muss umgesetzt werden

- Einen expliziten Terminlistenfilter für „nicht zugewiesen“ repo-konkret unterstützen, der fachlich dieselben Kriterien wie die Overview-Kennzahl `unassigned_termine` verwendet.
- Sicherstellen, dass der Klick auf die Karte `unassigned_termine` in der Oberfläche den Terminreiter öffnet und diesen Filter aktiviert.
- Die Terminliste muss dann nur Termine zeigen, die `status = geplant` haben, ab heute liegen und keinen Eintrag in `vorgang_termine` besitzen.
- Automatisierte Tests für den API-Filter ergänzen; falls bereits UI-nahe Routing-/State-Tests vorhanden sind, auch den Kartenklick absichern.

## Soll umgesetzt werden

- Wenn bereits ein allgemeiner Filterzustand für die Terminliste existiert, den neuen Zustand dort integriert statt als Sonderfall nur im Klickpfad zu verdrahten.
- Den aktiven Filter im Frontend sichtbar oder im Zustand nachvollziehbar halten, damit die Liste nach Reload/Neuladen konsistent bleibt, sofern dies mit wenig Aufwand zur bestehenden Struktur passt.

## Nicht Teil dieses Arbeitspakets

- Überarbeitung der `beginnt_am`-Zeitlogik bei ISO-Zeitpunkten.
- Große Terminfilter- oder Such-UX-Neugestaltung.
- Automatische Vorgangserstellung oder neue Termin-Zuordnungsworkflows.
- Backlog-Themen zu Mail/Belegen/Spendenbescheinigungen.

## Akzeptanzkriterien

- `GET /api/termine` kann so gefiltert werden, dass nur nicht zugewiesene anstehende geplante Termine zurückkommen.
- Ein geplanter zukünftiger Termin ohne `vorgang_termine`-Zuordnung erscheint im gefilterten Ergebnis.
- Ein geplanter zukünftiger Termin mit Vorgangszuordnung erscheint nicht im gefilterten Ergebnis.
- Vergangene, abgeschlossene oder abgesagte Termine erscheinen nicht im gefilterten Ergebnis.
- Beim Klick auf die Overview-Karte „Nicht zugewiesene anstehende Termine“ landet der Nutzer in der Terminansicht mit genau diesem Filter aktiv.
- Bestehende Terminlistenaufrufe ohne den neuen Filter verhalten sich unverändert.

## Hinweise für den Umsetzungs-Agenten

- Die SQL-Bedingung aus `overview_counts()` für `unassigned_termine` ist die fachliche Referenz und sollte nicht leicht abweichend neu interpretiert werden.
- Wahrscheinlich ist ein zusätzlicher Query-Parameter auf `/api/termine` der kleinste passende Schnittpunkt zwischen `server.py` und `app.js`.
- Falls im Frontend Karten über `entity: 'termine'` derzeit nur generisch umschalten, braucht `app.js` vermutlich eine Sonderbehandlung anhand des Card-Keys `unassigned_termine`, nicht nur anhand der Entity.
- Wenn `hide_completed` bereits in der Terminliste existiert, diesen nicht überladen; besser ein separater expliziter Filter für unzugewiesen, damit das Verhalten klar testbar bleibt.

## Manuelle Testhinweise

- Dashboard starten und mindestens drei Termine im Testbestand verwenden: 1) geplant + künftig + ohne Vorgang, 2) geplant + künftig + mit Vorgang, 3) vergangen oder nicht geplant.
- Overview öffnen und prüfen, dass die Kennzahl der Karte zum erwarteten unzugewiesenen Terminbestand passt.
- Auf die Karte „Nicht zugewiesene anstehende Termine“ klicken und prüfen, dass nur Fall 1 in der Terminliste erscheint.
- Danach Terminliste normal ohne den speziellen Kartenpfad öffnen und prüfen, dass das Standardverhalten für allgemeine Terminanzeigen unverändert bleibt.

## Offene Fragen

- Falls die aktuelle Frontend-Logik den Kartenklick-Zustand nicht granular pro Card-Key speichert: minimaler passender Integrationspunkt in `app.js` wählen, ohne Routing neu zu bauen.
