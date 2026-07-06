# Nächstes Arbeitspaket

## Titel

Dashboard-Kennzahlen für Termine präziser zählen

## Ziel

Die Dashboard-Karten für „Anstehende Termine“ und „Nicht zugewiesene Termine“ sollen nur fachlich passende Termine zählen, damit abgeschlossene oder abgesagte Termine nicht irreführend in den Kennzahlen erscheinen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: Berechnung in DashboardDataStore.overview_counts() für upcoming_termine und unassigned_termine anpassen.
- tests/test_dashboard.py: Dashboard-/API-Tests für die präzisierte Termin-Zähllogik ergänzen.
- banking_dashboard/static/app.js: Falls die Kartenbeschriftung oder erklärende Texte aus API-Werten gerendert werden, diese konsistent halten.
- banking_dashboard/static/index.html: Nur falls statische Labels oder Hilfetexte für die Kennzahlen angepasst werden müssen.

## Muss umgesetzt werden

- Für „Anstehende Termine“ nur tatsächlich anstehende Termine zählen; abgeschlossene und abgesagte Termine dürfen nicht mitgezählt werden.
- Für „Nicht zugewiesene Termine“ die Zähllogik so präzisieren, dass nur fachlich relevante offene/geplante unzugeordnete Termine gezählt werden, falls das mit der bestehenden Logik vereinbar ist.
- Automatisierte Tests für die neue Zähldefinition hinzufügen oder anpassen.
- Bestehende Statuskonstanten und die vorhandene Terminzuordnung über vorgang_termine weiterverwenden.

## Soll umgesetzt werden

- Grenzfälle mit Datum und Uhrzeit robust behandeln, wenn beginnt_am ISO-Datum oder ISO-Zeitpunkt enthalten kann.
- Falls die neue Logik enger ist als die bisherige Bezeichnung, die Kartenbezeichnung oder Begleittexte entsprechend klarziehen.
- Darauf achten, dass die Kartenlogik nicht fachlich von der bestehenden Terminlisten-Logik abweicht.

## Nicht Teil dieses Arbeitspakets

- Neue Terminfilter-UI oder eine neue Such-/Filter-Engine.
- Automatische Terminzuordnung zu Vorgängen.
- Änderungen an Mail-Import, Dokumenthandling oder Vorgangslogik.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Integration.

## Akzeptanzkriterien

- GET /api/overview zählt unter upcoming_termine keine abgeschlossenen oder abgesagten Termine mit.
- Ein geplanter zukünftiger Termin wird in upcoming_termine gezählt; ein geplanter Termin in der Vergangenheit nicht.
- unassigned_termine folgt einer klar präzisierten Regel und die Tests decken geplante versus abgeschlossene/abgesagte unzugeordnete Termine ab.
- Die Dashboard-Beschriftung ist nicht irreführend zur tatsächlichen Zähllogik.
- Die bestehenden Dashboard-Tests bleiben grün und sind um die neue Terminlogik ergänzt.

## Hinweise für den Umsetzungs-Agenten

- Die Änderung sollte lokal in overview_counts() konzentriert bleiben; dort liegen die relevanten SQL-Abfragen.
- TERMIN_STATUS_PLANNED, TERMIN_STATUS_COMPLETED und TERMIN_STATUS_CANCELLED sind bereits vorhanden und sollen ohne Magic Strings genutzt werden.
- Wenn unassigned_termine enger gefasst wird, die Anzeigeformulierung in der UI auf Verständlichkeit prüfen.
- transaction_store/database.py ist vor allem für Statuskonstanten und Termin-Schema-Details relevant; die eigentliche Umsetzung liegt voraussichtlich in server.py und den Tests.

## Manuelle Testhinweise

- Dashboard mit Testdaten starten, die mindestens je einen geplanten zukünftigen, geplanten vergangenen, abgeschlossenen und abgesagten Termin enthalten.
- Prüfen, dass die Karte „Anstehende Termine“ nur die fachlich erwarteten Termine zählt.
- Prüfen, dass unzugeordnete abgeschlossene oder abgesagte Termine die entsprechende Karte nicht mehr künstlich erhöhen, falls diese Regel umgesetzt wurde.
- Optional die Terminübersicht gegenprüfen, damit die gezählten offenen Termine für Nutzer nachvollziehbar sind.

## Offene Fragen

- Soll „Nicht zugewiesene Termine“ nur geplante Termine zählen oder weiterhin alle unzugeordneten Termine außer abgeschlossenen und abgesagten?
- Soll für „anstehend“ nur das Datum oder bei vorhandener Uhrzeit auch die genaue Startzeit maßgeblich sein?
