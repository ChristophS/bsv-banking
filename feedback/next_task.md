# Nächstes Arbeitspaket

## Titel

Aktiven Spezialfilter für nicht zugewiesene anstehende Termine in der Terminansicht sichtbar machen

## Ziel

In der Terminansicht soll klar erkennbar sein, wenn statt der normalen Terminliste der Spezialfilter für nicht zugewiesene anstehende Termine aktiv ist, inklusive einer einfachen Möglichkeit zum Zurücksetzen dieses Filters.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Zustand der Terminansicht um einen sichtbaren Hinweis für den aktiven Spezialfilter ergänzen; Rendering der Terminliste bzw. des Header-Bereichs anpassen; Reset-Aktion verdrahten.
- banking_dashboard/static/index.html: Falls für die Terminansicht ein dedizierter Platzhalter für Filterhinweise fehlt, minimal ergänzen.
- banking_dashboard/static/styles.css: Kleines Styling für Badge/Hinweis und Zurücksetzen-Aktion ergänzen.
- tests/test_dashboard.py: Frontend-nahe HTTP-/HTML-/JS-bezogene Tests bzw. Server-Integration prüfen und um passende Assertions ergänzen.

## Muss umgesetzt werden

- In der Terminansicht sichtbar anzeigen, wenn der Spezialfilter Nicht zugewiesene anstehende Termine aktiv ist.
- Der Hinweis soll für Nutzende verständlich benannt sein, z. B. mit genau diesem Filternamen oder einer sehr nahen Formulierung.
- Eine Zurücksetzen- oder Schließen-Aktion bereitstellen, die wieder zur normalen Terminliste ohne unassigned_upcoming-Filter führt.
- Sicherstellen, dass der sichtbare Hinweis genau an den aktiven Filterzustand gekoppelt ist und nicht dauerhaft eingeblendet bleibt.
- Mindestens einen Test ergänzen oder anpassen, der den sichtbaren Spezialfilterzustand absichert.

## Soll umgesetzt werden

- Den Hinweis als Badge/Infozeile im Kopf der Terminansicht platzieren, damit er sofort auffällt, aber die Liste nicht blockiert.

## Nicht Teil dieses Arbeitspakets

- Testen oder Überarbeiten der Rücksetzlogik bei normaler Termin-Navigation als eigener Backlog-Punkt.
- Änderungen an der Fachlogik, welche Termine als nicht zugewiesen oder anstehend gelten.
- Neue Spezialfilter oder generische Filter-Frameworks für alle Tabs.
- Überarbeitung der Zeitlogik von beginnt_am bei ISO-Zeitpunkten.

## Akzeptanzkriterien

- Wenn die Terminansicht mit aktivem unassigned_upcoming-Spezialfilter geöffnet wird, ist dies in der UI sichtbar gekennzeichnet.
- Die Kennzeichnung benennt den aktiven Spezialfilter verständlich und ist nicht mit dem normalen hide_completed-Filter verwechselt.
- Über die angebotene Zurücksetzen-/Schließen-Aktion kann zur normalen Terminliste zurückgekehrt werden.
- Nach dem Zurücksetzen verschwindet die Kennzeichnung wieder und die Terminliste wird ohne unassigned_upcoming geladen.
- Bestehende Terminlisten-Funktionalität bleibt erhalten; der Serverfilter unassigned_upcoming wird weiterhin wie bisher verwendet.
- Ein automatisierter Test deckt den sichtbaren Spezialfilterhinweis oder dessen Reset-Verhalten mindestens grundlegend ab.

## Hinweise für den Umsetzungs-Agenten

- Da server.py den Filter bereits versteht, sollte die Hauptarbeit im Frontend-State und Rendering liegen.
- Achte darauf, wie app.js zwischen Overview-Karten, Route/Tab-State und dem Laden von /api/termine vermittelt; der Hinweis sollte aus genau diesem bestehenden Zustand abgeleitet werden.
- Wenn index.html keinen festen Container braucht, kann das UI-Element auch komplett aus app.js erzeugt werden; nur minimal invasiv ändern.
- Falls die Terminansicht bereits eigene Filtertexte oder Section-Header rendert, den Spezialfilter dort integrieren statt einen zweiten konkurrierenden Hinweisbereich aufzubauen.

## Manuelle Testhinweise

- Dashboard öffnen und über die Overview-Karte Nicht zugewiesene anstehende Termine in die Terminansicht wechseln.
- Prüfen, dass ein sichtbarer Hinweis auf den aktiven Spezialfilter erscheint.
- Zurücksetzen-Aktion anklicken und prüfen, dass wieder die normale Terminliste erscheint und der Hinweis verschwindet.
- Anschließend normale Terminansicht ohne Spezialfilter direkt öffnen und prüfen, dass kein Hinweis fälschlich angezeigt wird.

## Offene Fragen

- Ob in app.js bereits ein zentrales Route-/View-State-Objekt für die Terminfilter existiert oder der Spezialfilter heute implizit nur beim Laden gesetzt wird; die Umsetzung sollte sich an der vorhandenen Struktur orientieren.
- Ob der Reset nur den Spezialfilter entfernen oder zusätzlich andere Terminfilter auf Standard setzen soll; bevorzugt nur den Spezialfilter zurücksetzen, sofern die bestehende Struktur das sauber erlaubt.
