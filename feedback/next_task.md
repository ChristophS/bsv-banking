# Nächstes Arbeitspaket

## Titel

Ladefehler in Dashboard-Listen konsistent als nicht verfügbar kennzeichnen

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5.3

## Ziel

Bei Ladefehlern sollen Ergebniszähler und zuvor angezeigte Filterresultate keinen veralteten oder scheinbar gültigen Zustand vermitteln.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Dashboard-Zustands- und Fehlerbehandlung für datenintensive Listen
- Darstellung von Ergebniszählern und bisherigen Filterresultaten
- Tests für Ladefehler und den daraus resultierenden Anzeigezustand

## Muss umgesetzt werden

- Bei einem Ladefehler den betroffenen Listenbereich eindeutig als fehlgeschlagen oder nicht verfügbar kennzeichnen.
- Ergebniszähler bei einem Ladefehler nicht als gültige aktuelle Ergebnisse anzeigen.
- Vorherige Filterresultate bei einem Ladefehler nicht als aktuelle oder erfolgreich geladene Daten fortführen.
- Den Fehlerzustand klar vom Zustand eines leeren Bestands oder einer erfolglosen Suche beziehungsweise Filterung abgrenzen.
- Das Verhalten durch automatisierte Tests absichern.

## Soll umgesetzt werden

- Eine konsistente, für Kassierer verständliche Fehlerbezeichnung und Darstellung über die betroffenen Listen hinweg verwenden.
- Bereits vorhandene Datenstrukturen und Zustandsmodelle weiterverwenden, statt neue fachliche Ersatzstrukturen einzuführen.

## Nicht Teil dieses Arbeitspakets

- Die Zustandsmatrix für alle datenintensiven Dashboard-Listen als eigenes Dokument erstellen.
- Neue Such-, Filter- oder Dashboard-Funktionen entwickeln.
- Backend- oder Datenbankstrukturen grundlegend umbauen.
- Ladezeiten oder externe Datenquellen optimieren.
- Mail-, Spenden-, Adress- oder DFBnet-Funktionen ändern.

## Akzeptanzkriterien

- Wenn das Laden einer Dashboard-Liste fehlschlägt, ist der Fehlerzustand sichtbar und eindeutig von einem leeren Ergebnis unterschieden.
- Während des Fehlerzustands wird kein Ergebniszähler als verlässlicher aktueller Wert angezeigt.
- Vor einem Ladefehler sichtbare Filterresultate werden nicht ohne klare Fehlerkennzeichnung als weiterhin gültige Ergebnisse präsentiert.
- Nach einem erfolgreichen erneuten Laden werden Ergebniszähler und Resultate wieder konsistent angezeigt.
- Bestehende Erfolgs-, Leerbestands- sowie Such- und Filterzustände bleiben unverändert funktionsfähig.
- Automatisierte Tests decken mindestens den Ladefehler mit Ergebniszähler sowie den Ladefehler nach zuvor vorhandenen Filterresultaten ab.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete technische Umsetzung und die benötigten Zustandsübergänge soll der Coding-Agent anhand des vorhandenen Dashboard-Codes prüfen.
- Keine produktiven externen Dienste oder echten Bankdaten für Tests verwenden; Fehlerantworten und Listendaten mocken oder als Fixtures bereitstellen.

## Manuelle Testhinweise

- Eine Dashboard-Liste erfolgreich laden und prüfen, dass Resultate und Zähler normal erscheinen.
- Einen Ladefehler simulieren und prüfen, dass Fehlerstatus, Zähler und alte Resultate nicht irreführend dargestellt werden.
- Nach dem Fehler einen erfolgreichen Reload ausführen und die Wiederherstellung der normalen Anzeige prüfen.
- Leere Resultate sowie erfolglose Suche oder Filterung separat prüfen.

## Offene Fragen

- Welche gemeinsame Fehler- und Ladezustandslogik wird aktuell von den Dashboard-Listen verwendet?
- Soll der Ergebniszähler im Fehlerzustand ausgeblendet oder explizit als nicht verfügbar markiert werden?
