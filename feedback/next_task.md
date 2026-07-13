# Nächstes Arbeitspaket

## Titel

Kassierer-Workflows und Reibungspunkte im Dashboard strukturiert analysieren

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 1

## Ziel

Die wichtigsten täglichen Arbeitsabläufe von Kassierern beim Sichten, Klassifizieren, Zuordnen und Abschließen von Vorgängen erfassen, konkrete Reibungspunkte priorisieren und daraus umsetzbare Verbesserungsanforderungen für das Dashboard ableiten.

## Relevante Dateien

- banking_dashboard/static/index.html
- banking_dashboard/static/app.js
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Dashboard-Ansichten und bestehende Arbeitsabläufe
- Darstellung von Vorgangs-, Transaktions-, Beleg-, Mail-, To-do- und Termin-Zuständen
- Bestehende Dashboard-Tests oder ein fachliches Analyseartefakt

## Muss umgesetzt werden

- Die wichtigsten Kassierer-Arbeitsabläufe vom Eingang eines offenen Elements bis zum Abschluss beschreiben.
- Reibungspunkte bei Sichtung, Klassifikation, Zuordnung und Abschluss von Vorgängen identifizieren.
- Offene Vorgänge als zentrales fachliches Objekt berücksichtigen und bestehende Verknüpfungen nicht durch direkte Ersatzbeziehungen umgehen.
- Die identifizierten Probleme nach Nutzerwirkung und Umsetzungsdringlichkeit priorisieren.
- Aus der Analyse klar abgegrenzte Anforderungen für nachfolgende Dashboard-Arbeitspakete ableiten.

## Soll umgesetzt werden

- Typische Einstiege und Wechsel zwischen offenen Vorgängen, Transaktionen, Belegen, Mails, To-dos und Terminen vergleichen.
- Unklare Statusanzeigen, fehlende Rückmeldungen und unnötige Bearbeitungsschritte gesondert erfassen.
- Leistungs- und Funktionsrisiken möglicher Verbesserungen dokumentieren.

## Nicht Teil dieses Arbeitspakets

- Keine konkrete Umsetzung einer neuen Übersicht oder Arbeitsliste.
- Keine Vereinheitlichung der Zuordnungsdialoge.
- Keine Änderung von Klassifikations- oder Abschlussvalidierungen.
- Keine umfassende Überarbeitung der datenintensiven Listen.
- Keine Einführung neuer externer Dienste oder produktiver Integrationen.

## Akzeptanzkriterien

- Ein nachvollziehbares Arbeitsablaufmodell für die zentralen Kassierer-Tätigkeiten liegt vor.
- Mindestens die Bereiche Sichten, Klassifizieren, Zuordnen und Abschließen sind abgedeckt.
- Jeder identifizierte Reibungspunkt ist einem konkreten Arbeitsablauf und einer betroffenen fachlichen Entität zugeordnet.
- Die Probleme sind priorisiert und die Priorisierung ist fachlich begründet.
- Aus den Ergebnissen lassen sich eigenständige, kleine Folgepakete für Übersicht, Zuordnungsdialoge und Abschlussblocker ableiten.
- Die Analyse wahrt die Vorgangsarchitektur und fordert keine Änderung an Originaldaten oder produktiven externen Aktionen.

## Hinweise für den Umsetzungs-Agenten

- Zunächst bestehende Dashboard-Flows und Zustandsdarstellungen anhand des Repository-Kontexts nachvollziehen.
- Technische Detailentscheidungen und konkrete Änderungsstellen erst im Folgepaket festlegen.
- Falls die Analyse in Dokumentation erfolgt, keine sensiblen Laufzeitdaten, Secrets oder externen Zugangsdaten aufnehmen.

## Manuelle Testhinweise

- Die bestehenden Dashboard-Einstiege und Bearbeitungsschritte mit repräsentativen lokalen Testdaten nachvollziehen.
- Prüfen, ob die Analyse alle zentralen offenen Bearbeitungsfälle und Blocker abdeckt.

## Offene Fragen

- Welche Kassiererrolle und welches Erfahrungsniveau bilden den primären Nutzungskontext?
- Welche offenen Elemente sollen fachlich zuerst bearbeitet werden, wenn mehrere Kategorien gleichzeitig vorliegen?
- Welche bestehenden Dashboard-Zustände und Filter gelten bereits als verbindlich?
