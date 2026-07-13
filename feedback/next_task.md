# Nächstes Arbeitspaket

## Titel

Übersicht als priorisierte Arbeitsliste für offene Kassierer-Aufgaben verbessern

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 2

## Ziel

Die Dashboard-Übersicht so überarbeiten, dass offene Vorgänge, unklassifizierte Transaktionen, Mails, To-Dos, Dokumente und Termine als klar priorisierte, direkt bearbeitbare Einstiegspunkte erscheinen.

## Relevante Dateien

- banking_dashboard/static/index.html
- banking_dashboard/static/app.js
- banking_dashboard/static/styles.css

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/index.html
- banking_dashboard/static/app.js
- banking_dashboard/static/styles.css

## Muss umgesetzt werden

- Die bestehenden Dashboard-Einstiege für offene Arbeitspunkte identifizieren.
- Eine priorisierte Arbeitslisten-Ansicht für die relevanten offenen Aufgaben konzipieren und umsetzen.
- Kennzahlen und Zustände so darstellen, dass sie direkt in konkrete Bearbeitungsschritte führen.
- Die Darstellung für offene Vorgänge, unklassifizierte Transaktionen, Mails, To-Dos, Dokumente und Termine konsistent halten.

## Soll umgesetzt werden

- Kurze, handlungsorientierte Labels verwenden.
- Visuelle Priorisierung nach fachlicher Dringlichkeit unterstützen.
- Bestehende Interaktionen nicht unnötig verändern.

## Nicht Teil dieses Arbeitspakets

- Keine vollständige Neuentwicklung des Dashboards.
- Keine Änderung der fachlichen Vorgangs-, Transaktions- oder Belegarchitektur.
- Keine externen Integrationen oder produktiven Banking-Aktionen.
- Keine Umsetzung der Zuordnungsdialoge, Abschlussblocker oder Listenoptimierungen aus späteren Teilpaketen.

## Akzeptanzkriterien

- Die Übersicht zeigt offene Kassierer-Aufgaben als priorisierte Arbeitsliste.
- Mindestens die wichtigsten offenen Arbeitskategorien sind direkt erkennbar und bearbeitbar.
- Die Darstellung führt nachvollziehbar zu den passenden Folgeaktionen.
- Die Lösung bleibt innerhalb der bestehenden Dashboard-Architektur.
- Es werden keine späteren Epic-Teilpakete vorweggenommen.

## Hinweise für den Umsetzungs-Agenten

- Zuerst die bestehenden Kacheln, Kennzahlen und Einstiegspunkte im Dashboard identifizieren.
- Die Arbeitsliste nur innerhalb der vorhandenen UI-Struktur erweitern.
- Die Priorisierung auf fachliche Relevanz und Bearbeitungsdruck ausrichten.

## Manuelle Testhinweise

- Dashboard mit typischen offenen Fällen laden und prüfen, ob die priorisierten Arbeitskategorien sichtbar sind.
- Prüfen, ob ein Klick aus der Übersicht in die passende Bearbeitung führt.
- Prüfen, ob offene Vorgänge, unklassifizierte Transaktionen und weitere Kategorien klar unterscheidbar sind.

## Offene Fragen

- Welche Kennzahlen sollen in der Arbeitsliste im Vordergrund stehen?
- Welche Kategorien müssen zwingend auf der ersten Ebene erscheinen?
- Soll die Priorisierung rein fachlich oder auch nach Fälligkeit erfolgen?
