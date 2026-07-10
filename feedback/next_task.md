# Nächstes Arbeitspaket

## Titel

Vorgangsübersicht nach Status priorisieren

## Ziel

Die Vorgangsliste soll offene Vorgänge vor abgeschlossenen Vorgängen anzeigen, ohne die bestehende Such-, Detail- und Zuordnungslogik zu verändern.

## Relevante Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: Sortierung in DashboardDataStore.list_vorgaenge() so anpassen, dass offene Vorgänge vor abgeschlossenen erscheinen.
- tests/test_dashboard.py: Bestehende Tests für die Vorgangsliste um die erwartete Status-Priorisierung ergänzen.

## Muss umgesetzt werden

- Die Standardreihenfolge der Vorgangsliste so ändern, dass Vorgänge mit status != abgeschlossen vor Vorgängen mit status = abgeschlossen erscheinen.
- Innerhalb der Statusgruppen die bestehende fachlich sinnvolle Reihenfolge möglichst beibehalten, also weiterhin nach letztem Transaktionsdatum bzw. aktualisiert_am sortieren statt eine komplett neue Sortierlogik einzuführen.
- Sicherstellen, dass die Änderung sowohl für die normale Vorgangsliste als auch für Suchtreffer gilt.
- Automatisierte Tests für die neue Priorisierung ergänzen.

## Soll umgesetzt werden

- Bei Gleichstand innerhalb einer Statusgruppe die bestehende deterministische Sortierung beibehalten.
- Bestehende Tests zur Suche und hide_completed-Filterung kurz mit prüfen, damit die neue Sortierung diese nicht bricht.

## Nicht Teil dieses Arbeitspakets

- Transaktionen bestehenden Vorgängen zuordnen und Vorgangsvorschläge für Transaktionen.
- Splitten von Transaktionen oder Rechnungen.
- Mail-Anhänge, To-Do-Erzeugung, Termin- oder Dokument-Flow-Anpassungen.
- Änderungen an Vorgangsstatus-Regeln oder automatische Abschlusslogik.
- Dashboard-Startseite oder weitere Komfortsortierungen in anderen Listen.
- Änderungen an der UI-Sortierung im DOM, falls die Reihenfolge sauber serverseitig geliefert werden kann.

## Akzeptanzkriterien

- GET /api/vorgaenge liefert offene Vorgänge vor abgeschlossenen Vorgängen zurück.
- Bei gemischter Datenlage erscheint ein abgeschlossener Vorgang nicht mehr vor einem offenen Vorgang nur wegen neuerem Datum.
- Die Suche über /api/vorgaenge?search=... respektiert weiterhin die Suchlogik und priorisiert innerhalb der Treffer offene Vorgänge vor abgeschlossenen.
- Der Filter hide_completed=true blendet abgeschlossene Vorgänge weiterhin vollständig aus.
- Bestehende Vorgangsdetails, Statusänderungen und Verknüpfungen funktionieren unverändert weiter.

## Hinweise für den Umsetzungs-Agenten

- In list_vorgaenge() wird aktuell primär nach COALESCE(MAX(n.datum), '') DESC, v.aktualisiert_am DESC, v.vorgangs_id sortiert. Die Statuspriorisierung sollte in diese ORDER-Bedingung integriert werden, statt nachträglich separat in der UI zu sortieren.
- Da status in der Tabelle bereits als String vorliegt und fachlich nur in_bearbeitung / abgeschlossen verwendet wird, reicht eine CASE-Sortierung im SQL nahe der bestehenden ORDER BY-Logik.
- Wenn app.js die Reihenfolge der API-Daten unverändert rendert, sollte dort kein Eingriff nötig sein; nur prüfen, ob irgendwo clientseitig re-sorted wird.
- Tests möglichst auf API-Ebene formulieren, damit das Verhalten unabhängig vom Rendering abgesichert ist.

## Manuelle Testhinweise

- Im Dashboard mehrere Vorgänge mit gemischtem Status anlegen oder Testdaten verwenden: mindestens zwei offene und zwei abgeschlossene.
- Vorgangsreiter öffnen und prüfen, dass alle offenen Vorgänge vor allen abgeschlossenen erscheinen.
- Danach Suche verwenden und prüfen, dass in den Suchergebnissen ebenfalls offene vor abgeschlossenen stehen.
- hide_completed aktivieren und prüfen, dass nur offene Vorgänge verbleiben.
- Optional einen offenen Vorgang abschließen und Liste neu laden; der Vorgang soll danach in den abgeschlossenen Block rutschen.

## Offene Fragen

- Falls mehrere offene Vorgänge existieren: Soll innerhalb der offenen Gruppe exakt die bisherige Reihenfolge beibehalten werden? Das ist fachlich wahrscheinlich sinnvoll und sollte so umgesetzt werden, sofern kein gegenteiliger Testbestand existiert.
