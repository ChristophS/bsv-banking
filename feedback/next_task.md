# Nächstes Arbeitspaket

## Titel

Kassierer-Workflows und Reibungspunkte im Dashboard strukturiert analysieren

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 1

## Ziel

Die täglichen Abläufe beim Sichten, Klassifizieren, Zuordnen und Abschließen von Vorgängen aus Sicht der allgemeinen Vereinsverwaltung erfassen, konkrete Reibungspunkte priorisieren und umsetzbare Verbesserungsbereiche für nachfolgende UI-Arbeitspakete ableiten.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Muss umgesetzt werden

- Die bestehenden Dashboard-Arbeitsabläufe für Vorgänge, Transaktionen, Belege, Mails, To-Dos und Termine aus Kassierersicht systematisch erfassen.
- Reibungspunkte bei Sichten, Klassifikation, Zuordnung, Abschluss und Fehlerbehandlung dokumentieren.
- Verbesserungsvorschläge nach fachlichem Nutzen und Dringlichkeit priorisieren.
- Die zentrale Rolle von Vorgängen und bestehenden Verknüpfungsstrukturen bei der Analyse berücksichtigen.
- Aus der Analyse klar abgegrenzte nachfolgende UI-Arbeitspakete ableiten.

## Soll umgesetzt werden

- Bestehende Status-, Abschluss- und Klassifikationszustände auf Verständlichkeit und Handlungsorientierung prüfen.
- Wiederkehrende Bearbeitungsschritte und unnötige Navigation identifizieren.
- Auswirkungen auf Datenmenge, Antwortzeit und bestehende Funktionen berücksichtigen.

## Nicht Teil dieses Arbeitspakets

- Keine Umsetzung umfassender UI-Änderungen in diesem Arbeitspaket.
- Keine Einführung neuer fachlicher Entitäten anstelle bestehender Vorgänge.
- Keine Änderung der Persistenz- oder Verknüpfungsarchitektur.
- Keine externen Dienste oder produktiven Banking-Aktionen.

## Akzeptanzkriterien

- Die relevanten Kassierer-Workflows sind vollständig und nachvollziehbar beschrieben.
- Für jeden untersuchten Workflow sind konkrete Reibungspunkte oder die Feststellung keiner relevanten Probleme dokumentiert.
- Die Verbesserungen sind priorisiert und jeweils einem klaren fachlichen Problem zugeordnet.
- Die Analyse unterscheidet zwischen kurzfristig umsetzbaren UI-Verbesserungen und späteren, eigenständigen Arbeitspaketen.
- Mindestens ein anschließendes kleines UI-Arbeitspaket ist so beschrieben, dass es unabhängig umgesetzt und geprüft werden kann.
- Bestehende Vorgangs- und Verknüpfungsstrukturen werden ausdrücklich als zu erhaltende Grundlage berücksichtigt.

## Hinweise für den Umsetzungs-Agenten

- Die Analyse kann anhand des vorhandenen Dashboards, der bestehenden Tests und des Repository-Kontexts erfolgen.
- Technische Detailentscheidungen und konkrete Änderungsstellen sollen erst im jeweiligen Folgepaket festgelegt werden.

## Manuelle Testhinweise

- Die vorhandenen Dashboard-Sichten und Bearbeitungswege mit typischen lokalen Testdaten nachvollziehen.
- Prüfen, ob offene, unklassifizierte und nicht abschließbare Elemente aus Sicht eines Kassierers verständlich auffindbar sind.

## Offene Fragen

- Welche Nutzerrollen und typischen Tagesabläufe sollen für die Priorisierung maßgeblich sein?
- Welche bestehenden Dashboard-Zustände gelten fachlich als verbindlich und dürfen nur verständlicher dargestellt werden?
