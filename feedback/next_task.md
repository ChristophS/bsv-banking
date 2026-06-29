# Nächstes Arbeitspaket

## Titel

Transaktionen: Filter für abgeschlossene Vorgänge

## Ziel

Im Reiter „Transaktionen“ soll eine Option verfügbar sein, mit der Transaktionen ausgeblendet werden können, die ausschließlich zu bereits abgeschlossenen Vorgängen gehören. Das bisherige Verhalten bleibt ohne aktivierten Filter unverändert.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: DashboardDataStore.list_transactions() um einen optionalen Filterparameter erweitern und die bestehende Zuordnung über transaktion_vorgaenge/vorgaenge auswerten.
- banking_dashboard/server.py: DashboardRequestHandler._transactions_response() um Query-Parsing und Rückgabe des aktiven Filterzustands erweitern.
- banking_dashboard/static/index.html: In der Transaktions-Toolbar eine Checkbox oder Umschaltoption für den neuen Filter ergänzen.
- banking_dashboard/static/app.js: Den Filterzustand in den API-Request für /api/transactions aufnehmen und beim Umschalten die Liste neu laden.
- banking_dashboard/static/styles.css: Nur falls nötig die neue Filter-Option an das bestehende Toolbar-Layout anpassen.
- tests/test_dashboard.py: API-Test für /api/transactions mit und ohne aktivem Filter ergänzen.

## Muss umgesetzt werden

- Neuen optionalen Filter für /api/transactions implementieren, z. B. hide_completed_vorgaenge.
- Beim aktiven Filter Transaktionen ausblenden, deren zugeordnete Vorgänge vollständig abgeschlossen sind und für die kein offener zugeordneter Vorgang mehr existiert.
- Ohne aktivierten Filter muss /api/transactions exakt das bisherige Verhalten behalten.
- Die UI im Transaktionsbereich um eine klar beschriftete Filter-Option ergänzen.
- Beim Umschalten des Filters die Transaktionsliste neu laden, ohne Suche, Zeitraum oder Sortierung zu verlieren.
- Die JSON-Antwort von /api/transactions soll den aktiven Filterzustand enthalten.

## Soll umgesetzt werden

- Die Beschriftung so wählen, dass klar ist, dass abgeschlossene Vorgänge gemeint sind.
- Falls im Frontend bereits zentraler Filter-State existiert, den neuen Wert dort integrieren statt einen Sonderfall zu bauen.

## Nicht Teil dieses Arbeitspakets

- Keine Änderung der Abschlusslogik für Vorgänge.
- Keine Änderung der automatischen Vorgangserzeugung.
- Keine Persistenz oder globale Benutzereinstellung für den Filter.
- Keine Änderungen an Spielerprämien, DFBnet, Zahlungsdatenabruf, Spam-Erkennung oder Mail-Verlauf.
- Keine Umsetzung des Themas Umbuchung mit Position und Gegenposition.
- Keine Änderungen an anderen Listen außerhalb der Transaktionen.

## Akzeptanzkriterien

- Ohne neuen Query-Parameter liefert /api/transactions dieselben Ergebnisse wie bisher.
- Mit aktivem Filter werden Transaktionen, die nur abgeschlossenen Vorgängen zugeordnet sind, nicht angezeigt.
- Transaktionen ohne Vorgangszuordnung bleiben bei aktivem Filter sichtbar.
- Transaktionen mit mindestens einem offenen zugeordneten Vorgang bleiben bei aktivem Filter sichtbar.
- Der Filter ist im Reiter „Transaktionen“ sichtbar und umschaltbar.
- Suche, Zeitraumfilter und Sortierung funktionieren weiterhin zusammen mit dem neuen Filter.
- Die bestehenden Tests laufen weiterhin erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Für die SQL-Logik bietet sich eine EXISTS/NOT EXISTS-Prüfung über transaktion_vorgaenge und vorgaenge an.
- Wichtig ist die Mehrfachzuordnung: eine Transaktion darf nur dann verschwinden, wenn kein offener Vorgang mehr verknüpft ist.
- Die bereits vorhandene Query-Parsing-Hilfe in server.py kann wiederverwendet werden.
- Für den UI-Filter kann das Muster aus der Vorgangsliste als Orientierung dienen.

## Manuelle Testhinweise

- Dashboard öffnen und den Reiter „Transaktionen“ aufrufen.
- Mit deaktiviertem Filter prüfen, dass die Liste unverändert bleibt.
- Einen bereits abgeschlossenen Vorgang mit zugeordneter Transaktion verwenden oder erzeugen.
- Filter aktivieren und prüfen, dass die Transaktion verschwindet, sofern sie keinem offenen Vorgang mehr zugeordnet ist.
- Filter wieder deaktivieren und prüfen, dass die Transaktion wieder erscheint.
- Zusätzlich Suche und Datumsfilter setzen und prüfen, dass der neue Filter weiterhin korrekt wirkt.

## Offene Fragen

- Soll die UI nur als Checkbox oder als allgemeiner Umschalter umgesetzt werden? Für das Paket reicht eine einfache Checkbox.
