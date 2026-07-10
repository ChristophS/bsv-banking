# Nächstes Arbeitspaket

## Titel

Dashboard-Startseite mit offenen Vorgängen, To-Dos, Terminen und Synchronisieren-Aktion ausbauen

## Ziel

Die bestehende Dashboard-Übersicht so erweitern, dass sie als klare Startseite die wichtigsten offenen Arbeitsobjekte sichtbar macht und die vorhandene Aktualisierungsfunktion als deutlich benannte 'Alles synchronisieren'-Aktion anbietet, ohne neue Architektur einzuführen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: vorhandene Overview-Daten um kleine Vorschauen oder einen kompakten Dashboard-Payload aus bestehenden DataStore-Methoden ergänzen; Refresh-Statuslogik weiterverwenden.
- banking_dashboard/static/index.html: Start-/Übersichtsbereich so anpassen, dass KPI-Karten, Vorschau-Listen und ein klarer Synchronisieren-Button sichtbar sind.
- banking_dashboard/static/app.js: Laden, Rendern und Aktualisieren der Dashboard-Startansicht; bestehende /api/overview- und /api/refresh-Flows an die UI anbinden.
- tests/test_dashboard.py: Tests für Overview/Refresh sowie für neue oder erweiterte Dashboard-Daten und sichtbare Startseiten-Inhalte ergänzen.

## Muss umgesetzt werden

- Einen klaren Dashboard-Startbereich bereitstellen, der mindestens offene Vorgänge, offene To-Dos und anstehende Termine sichtbar macht.
- Die vorhandene Aktualisierungsfunktion im UI als prominenten Button mit verständlicher Bezeichnung wie 'Alles synchronisieren' sichtbar machen.
- Den Status der Synchronisierung auf der Startseite anzeigen und parallele Starts weiterhin verhindern.
- Die Startansicht auf vorhandene API-Daten stützen und keine separaten Schattenmodelle im Frontend einführen.

## Soll umgesetzt werden

- Direkte Navigation aus den Dashboard-Karten oder Vorschauen in die bestehenden Bereiche Vorgänge, To-Dos und Termine ermöglichen.
- Vorschau-Listen sinnvoll begrenzen, etwa auf die nächsten Termine oder wenige offene Objekte.
- Die Benennung der Synchronisierungsaktion im UI verständlich an das Nutzerfeedback angleichen.

## Nicht Teil dieses Arbeitspakets

- Neues umfassendes Portal mit frei konfigurierbaren Widgets.
- Neue Sync-Logik für Mails jenseits der bereits vorhandenen Mechaniken.
- Transaktions-Splitting.
- Zuordnung mehrerer Mail-Dokumente zu verschiedenen Transaktionen innerhalb eines Vorgangs.
- Konzeption oder Umsetzung von Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Integration.

## Akzeptanzkriterien

- Beim Öffnen des Dashboards ist ein klar erkennbarer Start- bzw. Übersichtsbereich vorhanden.
- Die Startansicht zeigt offene Vorgänge, offene To-Dos und anstehende Termine auf Basis echter Repos-Daten an.
- Eine sichtbare Synchronisieren-Aktion stößt den bestehenden /api/refresh-Flow an und zeigt den laufenden bzw. abgeschlossenen Status an.
- Ein zweiter Start der Synchronisierung während eines laufenden Refreshs wird weiterhin abgefangen und führt nicht zu parallelen Läufen.
- Vorhandene Dashboard-Tests bleiben grün; neue Tests decken die Startseiten-Daten bzw. den Refresh-Einstieg ab.

## Hinweise für den Umsetzungs-Agenten

- Falls overview_counts() aktuell nur Kennzahlen liefert, ist eine kleine Erweiterung im selben DataStore naheliegend, etwa zusätzliche Vorschau-Arrays für Vorgänge, To-Dos und Termine.
- Die Auswahl 'anstehende Termine' sollte an die vorhandene Terminlogik anknüpfen, nicht an neue Regeln.
- Für offene To-Dos und offene Vorgänge sollten bestehende Sortierungen möglichst wiederverwendet oder konsistent gespiegelt werden.
- Wenn die UI bereits Tabs nutzt, soll die Dashboard-Startseite diese ergänzen oder als erste Ansicht verwenden, statt die Navigationsstruktur neu zu bauen.

## Manuelle Testhinweise

- Dashboard starten und prüfen, dass beim ersten Laden die Startübersicht sichtbar ist.
- Mit Testdaten offene To-Dos, offene Vorgänge und künftige Termine anlegen und prüfen, dass sie in der Übersicht erscheinen.
- Synchronisieren-Button anklicken und prüfen, dass der Status von idle auf running und anschließend auf completed oder failed wechselt.
- Während laufender Synchronisierung erneut klicken und prüfen, dass kein zweiter Lauf startet und eine verständliche Rückmeldung erscheint.
- Von den Dashboard-Karten oder Vorschauen in die jeweiligen Bereiche navigieren und prüfen, dass die bestehenden Listen weiter funktionieren.

## Offene Fragen

- Soll die Startseite zusätzlich ungelesene Mails als eigener Vorschau-Block zeigen, oder reichen dafür zunächst Kennzahl/Karte und Navigation?
- Soll 'Alles synchronisieren' nur den bestehenden Bank-Refresh triggern, oder im UI-Text ausdrücklich klarstellen, dass damit aktuell vor allem Kontobewegungen aktualisiert werden?
