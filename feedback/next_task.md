# Nächstes Arbeitspaket

## Titel

Overview-Kachelrouting auf zentrale Frontend-Mapping-Tabelle umstellen

## Ziel

Die Navigation beim Klick auf Overview-Kacheln soll im Frontend über eine zentrale Mapping-Tabelle statt über verstreute Kachel-Logik laufen. Das bestehende Dashboard-Verhalten bleibt dabei fachlich unverändert und neue Kacheln lassen sich später leichter ergänzen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: bestehende Klickbehandlung der Overview-Kacheln identifizieren und auf eine zentrale Routing-/Mapping-Struktur umstellen.
- banking_dashboard/static/app.js: falls aktuell mehrere if/switch-Zweige pro Kachel existieren, diese durch ein zentrales Mapping nach card.key oder entity ersetzen.
- banking_dashboard/static/index.html: nur falls die Kachel-Container oder data-Attribute für eine saubere zentrale Zuordnung leicht ergänzt werden müssen.
- tests/test_dashboard.py: Tests für /api/overview und ggf. erwartetes Dashboard-Verhalten minimal prüfen und bei Bedarf ergänzen.

## Muss umgesetzt werden

- Die Klicknavigation für Overview-Kacheln in banking_dashboard/static/app.js in eine zentrale Mapping-Tabelle oder eine äquivalente zentrale Konfiguration überführen.
- Die bestehende Navigation für alle aktuell vorhandenen Karten funktionsgleich beibehalten.
- Die Zuordnung so strukturieren, dass mehrere Karten mit derselben entity oder mit spezifischem key gezielt auf unterschiedliche Zielzustände gelenkt werden können.
- Fallback-Verhalten definieren: Unbekannte Karten dürfen das Dashboard nicht beschädigen und sollen entweder nichts tun oder auf eine sichere Standardansicht wechseln.

## Soll umgesetzt werden

- Falls bereits ein Sonderfall für Termine oder andere Kacheln existiert, diesen im Mapping explizit dokumentieren statt in separater Logik versteckt zu lassen.
- Die Mapping-Struktur im Code kurz sprechend benennen, damit spätere Kacheln ohne erneute Frontend-Suche ergänzt werden können.

## Nicht Teil dieses Arbeitspakets

- Neue Overview-Kacheln hinzufügen.
- Spezifischere Terminfilter für anstehende und nicht zugewiesene Termine umsetzen.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren.
- Größere Umbauten an API, Datenmodell oder serverseitiger Dashboard-Struktur.

## Akzeptanzkriterien

- Ein Klick auf jede bestehende Overview-Kachel führt weiterhin zur passenden Dashboard-Ansicht wie vor der Änderung.
- Die Zuordnungslogik für Kachelklicks ist im Frontend an einer zentralen Stelle lesbar definiert und nicht mehr über mehrere Fallunterscheidungen verstreut.
- Die vorhandenen Overview-Daten aus /api/overview bleiben kompatibel oder werden nur minimal und abwärtskompatibel genutzt.
- Unbekannte oder neu hinzukommende Karten verursachen keinen Frontend-Fehler.

## Hinweise für den Umsetzungs-Agenten

- Bevorzugt card.key als primären Mapping-Schlüssel nutzen, weil damit 'upcoming_termine' und 'unassigned_termine' trotz gleicher entity='termine' unterscheidbar bleiben.
- Falls die aktuelle Navigation nur über entity arbeitet, sollte das Mapping key-spezifische Overrides unterstützen und erst danach auf entity-Fallback zurückfallen.
- Da server.py die card.key-Werte bereits zentral erzeugt, sollte diese vorhandene Struktur genutzt statt dupliziert werden.
- Wenn Tests keine JS-Ausführung abdecken, kann ein kleiner serverseitiger Test auf stabile Overview-card-Schlüssel sinnvoller sein als fragile String-Assertions im kompletten JS-Inhalt.

## Manuelle Testhinweise

- Dashboard starten und auf jede Overview-Kachel klicken: Nicht abgeschlossene Vorgänge, Ungelesene Mails, Nicht zugewiesene Transaktionen, Offene To-Dos, Nicht zugewiesene Dokumente, Anstehende Termine, Nicht zugewiesene Termine.
- Prüfen, dass jeweils die gleiche Zielansicht wie vor der Änderung geöffnet bzw. aktiviert wird.
- Optional einen unbekannten Kartenfall simulieren, falls leicht möglich, und sicherstellen, dass kein JS-Fehler die Oberfläche blockiert.

## Offene Fragen

- Falls 'anstehende Termine' und 'nicht zugewiesene Termine' heute bereits auf exakt dieselbe Terminansicht springen: Soll das im Mapping zunächst bewusst gleich bleiben oder gibt es schon versteckte Filterparameter, die erhalten werden müssen?
