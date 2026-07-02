# Nächstes Arbeitspaket

## Titel

Vorgangs-Auswahl im Mail-Bereich per Suche und Filter verbessern

## Ziel

Die Auswahl vorhandener Vorgänge bei der Mail-Verknüpfung soll mit Suche und einem Filter für abgeschlossene Vorgänge bedienbar werden, ohne die bestehende Verknüpfungslogik zu ändern.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-UI für die Vorgangszuordnung um Suchfeld und Filter für abgeschlossene Vorgänge erweitern; vorhandene Lade- und Render-Logik anpassen.
- banking_dashboard/static/index.html: kleine UI-Ergänzungen für Such- und Filter-Controls im Mail-Vorgangsbereich.
- banking_dashboard/server.py: nur falls nötig den bestehenden /api/vorgaenge-Endpunkt im Mail-Flow nutzen; keine neue Such-API einführen.
- tests/test_dashboard.py: Tests für /api/vorgaenge mit search und hide_completed sowie für den Mail-Verknüpfungs-Flow ergänzen.

## Muss umgesetzt werden

- Im Mail-Bereich eine echte Suche auf vorhandene Vorgänge anbieten, statt nur eine unfilterte Liste anzuzeigen.
- Einen klaren Schalter oder Filter für abgeschlossene Vorgänge ergänzen.
- Die Suche gegen den bestehenden /api/vorgaenge-Endpunkt mit search und optional hide_completed anbinden.
- Sicherstellen, dass das Verknüpfen einer Mail mit einem gefundenen Vorgang weiterhin über den bestehenden Flow funktioniert.
- Bei keinem Treffer einen verständlichen Leerzustand anzeigen.

## Soll umgesetzt werden

- Falls die UI bisher /api/vorgaenge/link-candidates als Einstieg nutzt, diesen Startpunkt beibehalten, aber die gezielte Suche auf /api/vorgaenge umstellen.
- Suchanfragen im Frontend leicht entprellen oder erst ab kurzer Eingabelänge auslösen.
- In der Trefferliste Status, Typ oder Bezug sichtbar lassen, damit ähnlich benannte Vorgänge unterscheidbar bleiben.

## Nicht Teil dieses Arbeitspakets

- Neue Vorgangserstellung aus Mails
- Änderungen an der Vorgangs- oder Verknüpfungsarchitektur
- Komplexe Ranking- oder Scoring-Logik für Suchtreffer
- Allgemeine Dashboard-Neugestaltung
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen zuordnen

## Akzeptanzkriterien

- Im Mail-Bereich können Vorgänge per Suche gefunden werden, ohne durch die komplette Liste scrollen zu müssen.
- Abgeschlossene Vorgänge lassen sich in der Auswahl ausblenden.
- Die Treffer basieren auf der bestehenden Vorgangslogik von /api/vorgaenge.
- Eine Mail kann weiterhin mit einem gefundenen Vorgang verknüpft werden.
- Bei Suchbegriffen ohne Treffer wird ein klarer Leerzustand angezeigt.
- Bestehende Dashboard-Tests bleiben grün; ergänzte Tests decken Suche und Filter ab.

## Hinweise für den Umsetzungs-Agenten

- /api/vorgaenge unterstützt laut Analyse bereits search und hide_completed über DashboardDataStore.list_vorgaenge().
- Die bestehende inbox_vorgaenge-/Mail-Verknüpfung soll unverändert bleiben; nur die Auswahl der Zielvorgänge wird verbessert.
- Wenn /api/vorgaenge/link-candidates aktuell als Quelle dient, sollte es nicht als neue parallele Suchlogik ausgebaut werden.
- Die bereits vorhandenen Felder bezug, status, vorgangstyp und anzahl_transaktionen sind hilfreich für die Ergebnisanzeige.

## Manuelle Testhinweise

- Dashboard starten, Mail-Reiter öffnen und eine Mail zur Vorgangsverknüpfung auswählen.
- Nach einem Teil eines Titels, einer Beschreibung oder eines Bezugs suchen und passende Vorgänge prüfen.
- Filter für abgeschlossene Vorgänge ein- und ausschalten und die Änderung der Trefferliste beobachten.
- Eine Mail mit einem gefundenen offenen Vorgang verknüpfen und danach prüfen, dass die Verknüpfung sichtbar ist.
- Mit einem Suchbegriff ohne Treffer prüfen, dass ein verständlicher Leerzustand erscheint.

## Offene Fragen

- Soll der Filter für abgeschlossene Vorgänge standardmäßig aktiv sein oder standardmäßig aus?
- Nutzt die aktuelle Mail-UI bereits /api/vorgaenge/link-candidates als alleinige Datenquelle, oder wird schon /api/vorgaenge abgefragt?
