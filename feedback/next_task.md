# Nächstes Arbeitspaket

## Titel

Dashboard-Startseite mit Übersichtskarten und zentralem Sync-Button an bestehende Refresh-API anbinden

## Ziel

Eine kleine, nutzbare Dashboard-Startansicht bereitstellen, die die vorhandenen Kennzahlen sichtbar macht und den bestehenden Hintergrund-Refresh zentral startet, ohne neue Backend-Architektur einzuführen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/index.html: Start-/Übersichtsbereich mit Karten und einem zentralen Button 'Alles synchronisieren' ergänzen.
- banking_dashboard/static/app.js: Übersichtsdaten über GET /api/overview laden, Refresh über GET/POST /api/refresh anstoßen und Statusanzeige aktualisieren.
- banking_dashboard/server.py: nur falls kleine Response-Anpassungen oder Statusdaten nötig sind; vorhandene Endpunkte bevorzugt unverändert nutzen.
- tests/test_dashboard.py: Tests für Übersicht und Refresh-Status bzw. deren Darstellung ergänzen.

## Muss umgesetzt werden

- Eine sichtbare Start-/Übersichtsansicht im Frontend ergänzen, die die von /api/overview gelieferten Kennzahlen als Übersichtskarten anzeigt.
- Einen zentralen Button 'Alles synchronisieren' bereitstellen, der POST /api/refresh verwendet.
- Den aktuellen Refresh-Status aus GET /api/refresh anzeigen, inklusive idle/running/completed/failed und der vorhandenen Statusnachricht.
- Während eines laufenden Refreshs parallele Starts in der UI verhindern oder klar blockieren, passend zur serverseitigen Conflict-Logik.
- Nach erfolgreichem oder fehlgeschlagenem Refresh die Übersichtsdaten erneut laden, damit die Karten aktualisierte Werte zeigen.
- Die Startseite so einbauen, dass bestehende Bereiche weiterhin erreichbar bleiben und das Dashboard nicht auf eine Einzelseite reduziert wird.

## Soll umgesetzt werden

- Karten klickbar machen oder mit vorhandenen Bereichen verknüpfen, wenn dies in der bestehenden Frontend-Struktur ohne größeren Umbau möglich ist.
- Die bereits von /api/overview gelieferten entity-/key-Informationen verwenden, statt Labels im Frontend doppelt zu pflegen.
- Eine klare Benutzer-Rückmeldung beim Start des Refreshs anzeigen, z. B. laufender Status oder Hinweis auf Browser/MFA.

## Nicht Teil dieses Arbeitspakets

- Neue Sync-Arten außerhalb des bestehenden Refresh-Laufs
- Umbau der kompletten Navigation oder aller Dashboard-Reiter
- Automatische Aggregation zusätzlicher Kennzahlen, die nicht aus overview_counts() kommen
- Transaktions-Splitting
- Zuordnung mehrerer Mail-Dokumente zu unterschiedlichen Transaktionen innerhalb eines Vorgangs
- Spendenbescheinigungen/Adressdatenbank/DFBnet-Verein-Integration

## Akzeptanzkriterien

- Beim Öffnen des Dashboards ist eine echte Start-/Übersichtsansicht sichtbar und zeigt die Kennzahlen aus GET /api/overview an.
- Der Button 'Alles synchronisieren' startet über POST /api/refresh den bestehenden Hintergrundlauf.
- Wenn bereits ein Lauf aktiv ist, zeigt die UI den laufenden Zustand an und startet keinen zweiten parallelen Lauf.
- Nach Abschluss oder Fehler des Refreshs wird der Status für den Nutzer sichtbar aktualisiert.
- Die bestehenden Dashboard-Bereiche bleiben weiterhin nutzbar.
- Vorhandene oder ergänzte Tests decken mindestens die relevanten Overview-/Refresh-API-Erwartungen ab.

## Hinweise für den Umsetzungs-Agenten

- overview_counts() liefert bereits cards und counts; diese Struktur möglichst direkt im Frontend rendern statt eine zweite Mapping-Logik einzuführen.
- Für den Sync-Button keine neue Route erfinden; der vorhandene POST /api/refresh ist der richtige Einstiegspunkt.
- Die Statusmeldung des RefreshManagers ist bereits fachlich passend ('Bankbrowser wird geöffnet ...'); diese Nachricht in der UI anzeigen statt neu zu formulieren.
- Falls die Startseite noch keinen eigenen View-State hat, klein anfangen: zusätzlicher Dashboard-Abschnitt oder erster Tab statt größerem Frontend-Refactor.
- Serverseitige Änderungen nur dann, wenn Tests oder Frontend-Anbindung zeigen, dass kleine Ergänzungen an den Response-Daten fehlen.

## Manuelle Testhinweise

- Dashboard starten und prüfen, dass die neue Startseite direkt sichtbar ist.
- Kontrollieren, dass die Kennzahlen für offene Vorgänge, ungelesene Mails, offene To-Dos, nicht zugewiesene Dokumente und anstehende Termine angezeigt werden.
- Auf 'Alles synchronisieren' klicken und prüfen, dass der laufende Status sichtbar wird.
- Während des Laufs erneut klicken und prüfen, dass kein zweiter Start erfolgt bzw. ein sauberer Hinweis erscheint.
- Nach Abschluss prüfen, dass Status und Übersicht neu geladen wurden.
- Bestehende Reiter einmal durchklicken, um sicherzustellen, dass keine Navigation kaputt gegangen ist.

## Offene Fragen

- Soll die neue Startseite der initial sichtbare Standard-Tab sein oder als eigener oberster Abschnitt vor den bestehenden Reitern erscheinen? Der Umsetzungs-Agent sollte dies anhand der vorhandenen Frontend-Struktur minimalinvasiv entscheiden.
