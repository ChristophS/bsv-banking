# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der Diff ist für die fachliche Prüfung ausreichend: Die Statuspriorisierung wurde direkt in der bestehenden SQL-ORDER-BY-Klausel von list_vorgaenge() ergänzt und passende API-/Datastore-Tests wurden erweitert.

## Zusammenfassung

Die Vorgangsliste priorisiert nun serverseitig offene Vorgänge vor abgeschlossenen Vorgängen, während die bestehende Datumssortierung innerhalb der Statusgruppen erhalten bleibt. Die Umsetzung erfüllt die Akzeptanzkriterien inklusive Suche und hide_completed-Verhalten.

## Review-Ergebnis

**Accepted:** ja

## Geprüfte Anforderungen

- Offene Vorgänge sollen vor abgeschlossenen Vorgängen erscheinen.
- Innerhalb der Statusgruppen soll die bisherige Sortierung nach letztem Transaktionsdatum, `aktualisiert_am` und `vorgangs_id` erhalten bleiben.
- Die Änderung soll sowohl für die normale Liste als auch für Suchtreffer gelten.
- `hide_completed=true` soll abgeschlossene Vorgänge weiterhin vollständig ausblenden.
- Automatisierte Tests sollen die neue Priorisierung abdecken.

## Bewertung der Umsetzung

In `banking_dashboard/server.py` wurde die bestehende `ORDER BY`-Klausel in `DashboardDataStore.list_vorgaenge()` um folgende Statuspriorisierung erweitert:

```sql
CASE
    WHEN v.status = 'abgeschlossen' THEN 1
    ELSE 0
END,
```

Diese Sortierung steht vor der bisherigen Sortierung nach `COALESCE(MAX(n.datum), '') DESC`, `v.aktualisiert_am DESC` und `v.vorgangs_id`. Damit werden offene bzw. nicht abgeschlossene Vorgänge vor abgeschlossenen Vorgängen angezeigt, ohne die bestehende fachliche Reihenfolge innerhalb der jeweiligen Statusgruppe zu ersetzen.

Da die Priorisierung direkt in der gemeinsamen SQL-Abfrage von `list_vorgaenge()` liegt, gilt sie plausibel sowohl für die normale Vorgangsliste als auch für Suchtreffer. Der bestehende `hide_completed`-Filter wird durch die Änderung nicht erkennbar beeinflusst.

## Tests

In `tests/test_dashboard.py` wurden Tests ergänzt für:

- Priorisierung offener Vorgänge vor abgeschlossenen Vorgängen in der Datastore-Liste.
- Priorisierung bei Suchtreffern.
- Fortbestehendes Ausblenden abgeschlossener Vorgänge mit `hide_completed=True`.
- API-Verhalten von `/api/vorgaenge` und `/api/vorgaenge?search=...`.

Der Implementation Report nennt einen erfolgreichen Lauf von `tests/test_dashboard.py` mit `87 passed, 4 skipped`.

## Blockierende Probleme

Keine.

## Nicht-blockierende Hinweise

Optional könnten weitere Tests mit mehreren offenen und mehreren abgeschlossenen Vorgängen ergänzt werden, um die Beibehaltung der bisherigen Sortierung innerhalb jeder Statusgruppe noch stärker abzusichern.
