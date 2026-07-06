# Nächstes Arbeitspaket

## Titel

Vorgangsübersicht nach Status priorisieren

## Ziel

Die Vorgangsliste im Dashboard soll standardmäßig zuerst nicht abgeschlossene Vorgänge und danach abgeschlossene Vorgänge anzeigen. Innerhalb der Statusgruppen soll die bestehende fachliche Sortierung möglichst erhalten bleiben.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: Sortierung in DashboardDataStore.list_vorgaenge anpassen, damit abgeschlossene Vorgänge nach den offenen/ in_bearbeitung Vorgängen einsortiert werden.
- banking_dashboard/static/app.js: nur prüfen, ob die UI die Server-Reihenfolge direkt rendert; nur ändern, falls dort clientseitig nachsortiert wird.
- tests/test_dashboard.py: Reihenfolge- und Filtertests für /api/vorgaenge ergänzen oder anpassen.

## Muss umgesetzt werden

- Die Standardreihenfolge der Vorgangsübersicht so ändern, dass Vorgänge mit Status ungleich abgeschlossen vor abgeschlossenen Vorgängen erscheinen.
- Innerhalb der Gruppe nicht abgeschlossener Vorgänge die bestehende Sortierlogik nach letztem Transaktionsdatum bzw. aktualisiert_am beibehalten.
- Sicherstellen, dass hide_completed weiterhin funktioniert und abgeschlossene Vorgänge bei aktivem Filter nicht mehr geliefert werden.
- Einen Test ergänzen, der bei gemischten Status explizit prüft, dass offene bzw. in_bearbeitung Vorgänge vor abgeschlossenen geliefert werden.

## Soll umgesetzt werden

- Falls die UI clientseitig sortiert, die Backend-Reihenfolge dort unverändert übernehmen.
- Einen Testfall ohne Transaktionen oder ohne letztes Datum mitprüfen, damit die Status-Priorisierung stabil bleibt.

## Nicht Teil dieses Arbeitspakets

- Eigene Sortieroptionen in der UI für Vorgänge
- Änderungen an der Transaktionsliste
- Änderungen an Abschlussregeln oder Statussemantik
- Dashboard-Startseite oder andere Backlog-Themen

## Akzeptanzkriterien

- GET /api/vorgaenge liefert bei gemischten Status zuerst alle Vorgänge mit Status ungleich abgeschlossen und danach die abgeschlossenen.
- Bei zwei offenen Vorgängen bleibt die bisherige Reihenfolge nach letztem Transaktionsdatum bzw. aktualisiert_am erhalten.
- Bei gesetztem hide_completed=true erscheinen keine abgeschlossenen Vorgänge mehr.
- Bestehende Vorgangsdetails, Statuswechsel und andere API-Endpunkte verhalten sich unverändert.

## Hinweise für den Umsetzungs-Agenten

- Die fachliche Anforderung spricht von offenen bzw. in Bearbeitung; im aktuellen Modell existieren praktisch status in_bearbeitung und abgeschlossen. Die Sortierung sollte daher über eine Status-Priorisierung wie CASE WHEN v.status = 'abgeschlossen' THEN 1 ELSE 0 END erfolgen.
- Da list_vorgaenge die zentrale Quelle für die Übersicht ist, sollte die Änderung dort erfolgen und nicht nur im Frontend.
- Wenn app.js die API-Reihenfolge direkt rendert, ist vermutlich keine Frontend-Änderung nötig; trotzdem prüfen.

## Manuelle Testhinweise

- Im Dashboard mehrere Vorgänge mit gemischtem Status erzeugen oder vorhandene Daten nutzen.
- Reiter Vorgänge öffnen und prüfen, dass nicht abgeschlossene Vorgänge oberhalb der abgeschlossenen erscheinen.
- Einen abgeschlossenen Vorgang wieder öffnen bzw. einen offenen abschließen und prüfen, dass sich die Position nach Neuladen entsprechend ändert.
- Den Filter für abgeschlossene Vorgänge testen, falls in der UI vorhanden.

## Offene Fragen

- Keine fachlich blockierende Frage. Falls die UI bereits lokal nachsortiert, muss entschieden werden, ob die Backend-Reihenfolge dort strikt übernommen wird.
