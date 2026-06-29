# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Umsetzung erfüllt das Arbeitspaket: Der neue optionale Filter für /api/transactions wurde serverseitig, im Frontend und mit Tests ergänzt. Die JSON-Antwort enthält den aktiven Filterzustand, und der Filterzustand wird beim Umschalten beibehalten sowie die Liste neu geladen. Der Compare-Zustand ist sauber (ahead_by=1, behind_by=0), und es gibt keine offensichtlichen Blocker im Diff.

### Review-Ergebnis

Die Implementierung ist akzeptierbar.

### Abgleich mit dem Arbeitspaket

- `/api/transactions` unterstützt nun den optionalen Query-Parameter `hide_completed_vorgaenge`.
- Die Filterlogik blendet nur Transaktionen aus, die ausschließlich mit abgeschlossenen Vorgängen verknüpft sind.
- Transaktionen ohne Vorgangszuordnung bleiben sichtbar.
- Transaktionen mit mindestens einem offenen Vorgang bleiben sichtbar.
- Die Antwort enthält den aktiven Filterzustand.
- Die UI wurde um eine klar beschriftete Checkbox ergänzt.
- Beim Umschalten wird die Transaktionsliste neu geladen, ohne Suche, Zeitraum oder Sortierung zu verlieren.
- Tests für Store und API wurden ergänzt.

### Bewertung

Keine blockierenden Probleme erkennbar.
