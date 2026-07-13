# Nächstes Arbeitspaket

## Titel

Kassierer-Workflows und Reibungspunkte im Dashboard strukturiert analysieren

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 1

## Ziel

Die täglichen Abläufe beim Sichten, Klassifizieren, Zuordnen und Abschließen von Vorgängen aus Sicht der allgemeinen Vereinsverwaltung erfassen und konkrete, priorisierte Verbesserungsbedarfe für nachfolgende UI-Arbeitspakete ableiten.

## Relevante Dateien

- banking_dashboard/static/index.html
- banking_dashboard/static/app.js
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Die bestehenden Dashboard-Arbeitsabläufe für offene Vorgänge, Transaktionen, Belege, Mails, To-Dos und Termine aus Kassierersicht nachvollziehbar erfassen.
- Reibungspunkte bei Sichtung, Klassifikation, Zuordnung, Validierung und Abschluss fachlich beschreiben.
- Die Ergebnisse nach Auswirkung auf tägliche Vereinsverwaltung und Umsetzungsdringlichkeit priorisieren.
- Für jeden priorisierten Punkt einen klar abgegrenzten Verbesserungsvorschlag formulieren, ohne die Vorgangsarchitektur zu umgehen.

## Soll umgesetzt werden

- Unterscheiden, ob ein Problem durch fehlende Sichtbarkeit, unklare Zustände, unnötige Schritte oder fehlende Rückmeldung entsteht.
- Aus den Ergebnissen eine sinnvolle Reihenfolge für die nachfolgenden Teilpakete des Usability-Epics ableiten.
- Mögliche Auswirkungen auf bestehende Funktionen und Leistungsanforderungen ausdrücklich festhalten.

## Nicht Teil dieses Arbeitspakets

- Keine konkrete UI-Implementierung.
- Keine Änderung an Datenmodell, API oder bestehenden Verknüpfungstabellen.
- Keine neuen externen Integrationen.
- Keine umfassende Performance-Optimierung oder technische Neustrukturierung.

## Akzeptanzkriterien

- Ein nachvollziehbares Ergebnisdokument oder eine gleichwertige dokumentierte Analyse der relevanten Kassierer-Workflows liegt vor.
- Die wichtigsten Reibungspunkte sind fachlich beschrieben und priorisiert.
- Die Analyse deckt Sichten, Klassifikation, Zuordnung und Abschluss von Vorgängen sowie die relevanten angrenzenden Entitätstypen ab.
- Mindestens die nächsten eigenständigen Verbesserungsbereiche sind so abgegrenzt, dass daraus kleine Folgearbeitspakete erstellt werden können.
- Die Analyse enthält keine Empfehlung, bestehende vorgangsbasierte Beziehungen durch direkte Ersatzbeziehungen zu umgehen.
- Bestehender Funktionsumfang und erwartete Leistung werden als Randbedingungen berücksichtigt.

## Hinweise für den Umsetzungs-Agenten

- Die Analyse kann anhand des vorhandenen Dashboard-Codes, der bestehenden Tests und des README-Kontexts durchgeführt werden.
- Technische Änderungsstellen für spätere Teilpakete müssen noch nicht festgelegt werden.

## Manuelle Testhinweise

- Die vorhandenen Dashboard-Ansichten und Bearbeitungsschritte mit typischen offenen und teilweise klassifizierten Daten gedanklich oder lokal nachvollziehen.
- Prüfen, ob aus jeder identifizierten Blockade eine verständliche nächste Handlung für Kassierer ableitbar ist.

## Offene Fragen

- Welche Aufgabenarten im realen Vereinsbetrieb werden am häufigsten gemeinsam bearbeitet?
- Welche bestehenden Status- und Abschlussregeln sind für Kassierer aktuell am wenigsten verständlich?
- Welche priorisierten Verbesserungen sollen anschließend zuerst als eigenständige UI-Arbeitspakete umgesetzt werden?
