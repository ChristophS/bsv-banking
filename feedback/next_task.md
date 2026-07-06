# Nächstes Arbeitspaket

## Titel

Regressionstest für Rücksetzen des Spezialfilters bei normaler Termin-Navigation ergänzen

## Ziel

Absichern, dass der Spezialfilter für nicht zugewiesene anstehende Termine nur im vorgesehenen Spezialkontext aktiv ist und beim Wechsel in die normale Terminansicht wieder zurückgesetzt wird.

## Relevante Dateien

- tests/test_dashboard.py
- banking_dashboard/static/app.js
- banking_dashboard/server.py

## Wahrscheinliche Änderungsstellen

- tests/test_dashboard.py: einen gezielten Regressionsfall ergänzen, der zuerst den Spezialfilter unassigned_upcoming nutzt und danach die normale Terminansicht aufruft.
- banking_dashboard/static/app.js: nur falls der Test eine echte Lücke offenlegt; dort liegt voraussichtlich der State für Terminfilter und Navigation.
- banking_dashboard/server.py: nur als Referenz für die erwartete API-Semantik von unassigned_upcoming und hide_completed.

## Muss umgesetzt werden

- Einen automatisierten Test ergänzen, der den Spezialfilter unassigned_upcoming aktiv verwendet und anschließend eine normale Termin-Navigation bzw. Standardansicht auslöst.
- Im Test verifizieren, dass die nachfolgende normale Terminladung nicht mehr mit unassigned_upcoming=true erfolgt.
- Sicherstellen, dass der Test klar zwischen Spezialansicht und regulärer Terminansicht unterscheidet.

## Soll umgesetzt werden

- Falls bereits ähnliche Tests für Query-Parameter oder Tab-Wechsel existieren, denselben Teststil und vorhandene Hilfsfunktionen wiederverwenden.
- Den Test auf beobachtbares Verhalten statt auf interne Implementierungsdetails ausrichten.

## Nicht Teil dieses Arbeitspakets

- Prüfung oder Anpassung der beginnt_am-Zeitlogik bei ISO-Zeitpunkten.
- Neue Terminfilter oder Persistenz des Filterzustands.
- Größere Überarbeitung der Termin-Navigation.
- Mail-/Dokumenten-Zuordnung oder Spendenbescheinigungsfunktionen.

## Akzeptanzkriterien

- Es existiert ein automatisierter Test, der den Spezialfilter-Rücksetzfall explizit abdeckt.
- Der Test zeigt, dass nach Rückkehr zur normalen Terminansicht keine Anfrage mehr mit unassigned_upcoming=true für den regulären Flow verwendet wird.
- Vorhandene Terminfunktionen und andere Dashboard-Tests bleiben grün.

## Hinweise für den Umsetzungs-Agenten

- Das Paket bewusst testzentriert halten; Produktivcode nur anfassen, wenn der neue Test eine reale Regression offenlegt.
- server.py trennt die Semantik von unassigned_upcoming bereits klar, daher liegt die wahrscheinlichste Ursache in app.js bei der Zustandsverwaltung beim Wechsel zwischen Spezialansicht und normaler Terminroute/-tab.
- Falls der Test API-Aufrufe beobachtet, auf die Kombinationen hide_completed/unassigned_upcoming achten und den Standardfall sauber von der Spezialansicht abgrenzen.

## Manuelle Testhinweise

- Im Dashboard zur Spezialansicht für nicht zugewiesene anstehende Termine wechseln.
- Danach über die normale Termin-Navigation bzw. den allgemeinen Termin-Reiter zurückgehen.
- Prüfen, dass wieder die normale Terminliste erscheint und nicht weiterhin nur nicht zugewiesene anstehende Termine gefiltert werden.

## Offene Fragen

- Welche konkrete UI-Aktion in app.js bildet die normale Termin-Navigation ab: Tab-Klick, Unteransicht oder erneutes Laden derselben Liste?
- Ob bereits ein ähnlicher Regressionstest existiert, der nur erweitert statt neu aufgebaut werden sollte.
