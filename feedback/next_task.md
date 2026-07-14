# Nächstes Arbeitspaket

## Titel

Verhaltensbasierte Tests für die drei Zustände der To-do- und Terminlisten ergänzen

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5.1

## Ziel

Die Zustandslogik der Dashboard-Listen für To-dos und Termine verhaltensbasiert absichern, damit leerer Bestand, erfolglose Suche oder Filterung sowie Ladefehler eindeutig und stabil dargestellt werden.

## Relevante Dateien

- tests/test_dashboard.py
- banking_dashboard/static/app.js

## Wahrscheinliche Änderungsstellen

- Dashboard-Tests für To-do- und Terminlisten
- Bestehende Zustands- und Renderinglogik der Dashboard-Listen

## Muss umgesetzt werden

- Verhaltensbasierte Tests für einen leeren Bestand der To-do-Liste und der Terminliste ergänzen.
- Verhaltensbasierte Tests für eine Suche oder Filterung ohne Treffer ergänzen.
- Verhaltensbasierte Tests für einen Ladefehler ergänzen.
- Prüfen, dass die drei Zustände fachlich unterscheidbar dargestellt oder behandelt werden.
- Bestehende Dashboard-Komponenten und Testmuster verwenden.

## Soll umgesetzt werden

- Gemeinsame Testhilfen für die beiden Listen nutzen, sofern dadurch die Tests verständlich bleiben.
- Externe Dienste ausschließlich durch vorhandene Mocks, Fakes oder Fixtures ersetzen.

## Nicht Teil dieses Arbeitspakets

- Änderungen an Persistenz, Datenbank oder Vorgangsstrukturen.
- Neue Dashboard-Funktionen außerhalb der To-do- und Terminlisten.
- Änderungen an Ergebniszählern oder dem Verhalten alter Filterresultate bei Ladefehlern; dies bleibt ein separates Folgepaket.
- Dokumentation einer vollständigen Zustandsmatrix für weitere Dashboard-Listen.

## Akzeptanzkriterien

- Die Tests decken für die To-do-Liste die Zustände leerer Bestand, keine Treffer und Ladefehler ab.
- Die Tests decken für die Terminliste die Zustände leerer Bestand, keine Treffer und Ladefehler ab.
- Die Tests prüfen beobachtbares Verhalten statt ausschließlich statischer Implementierungsdetails.
- Die Tests laufen reproduzierbar ohne externe Dienste oder produktive Daten.
- Bestehende Dashboard-Tests bleiben erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete Teststrategie und die geeigneten Testwerkzeuge anhand der vorhandenen Dashboard-Teststruktur bestimmen.
- Keine unnötige Umstrukturierung bestehender Komponenten vornehmen.

## Manuelle Testhinweise

- Dashboard mit leerem Datenbestand öffnen und To-do- sowie Terminliste prüfen.
- Suche oder Filter so wählen, dass keine Einträge übrig bleiben, und die Darstellung prüfen.
- Einen simulierten oder lokal reproduzierbaren Ladefehler auslösen und die Fehlerdarstellung prüfen.

## Offene Fragen

- Welche vorhandenen Mocks oder Fixtures bilden die Datenladefehler des Dashboards bereits ab?
