# Nächstes Arbeitspaket

## Titel

Kompakte Zustandsmatrix für datenintensive Dashboard-Listen dokumentieren

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5.2

## Ziel

Die relevanten Zustände datenintensiver Dashboard-Listen übersichtlich dokumentieren und leeren Bestand, erfolglose Suche oder Filterung sowie Ladefehler klar voneinander abgrenzen.

## Relevante Dateien

- feedback/cashier_workflow_analysis.md

## Wahrscheinliche Änderungsstellen

- feedback/cashier_workflow_analysis.md

## Muss umgesetzt werden

- Eine kompakte Matrix für die relevanten datenintensiven Dashboard-Listen erstellen oder ergänzen.
- Mindestens die Zustände geladener Bestand, leerer Bestand, keine Such- oder Filtertreffer und Ladefehler unterscheiden.
- Für jeden Zustand eine verständliche Bedeutung und eine geeignete Nutzerorientierung oder Handlungsempfehlung dokumentieren.
- Die Zustandsbegriffe konsistent und ohne neue fachliche Datenstrukturen festlegen.

## Soll umgesetzt werden

- Gemeinsame Zustandsmerkmale listenübergreifend wiederverwenden.
- Besondere Hinweise für initiales Laden und aktive Suche oder Filterung kenntlich machen.

## Nicht Teil dieses Arbeitspakets

- Änderungen an Dashboard-Code, API, Persistenz oder Datenmodellen.
- Implementierung neuer Listen, Filter oder Ladezustände.
- Überarbeitung unabhängiger Mail-, Spenden-, Adress- oder DFBnet-Funktionen.

## Akzeptanzkriterien

- Die Dokumentation enthält eine kompakte, leicht auffindbare Zustandsmatrix.
- Leerer Bestand ist eindeutig von erfolglosen Such- oder Filtertreffern abgegrenzt.
- Ladefehler sind eindeutig von beiden leeren Ergebniszuständen abgegrenzt.
- Für jeden dokumentierten Zustand ist die fachliche Bedeutung nachvollziehbar.
- Das Arbeitspaket enthält ausschließlich die Zustandsdokumentation und verändert keine Laufzeitfunktion.

## Hinweise für den Umsetzungs-Agenten

- Die bestehende Analyse unter feedback/cashier_workflow_analysis.md als fachlichen Bezug verwenden.
- Keine konkreten UI- oder Implementierungsdetails festschreiben, die aus dem vorhandenen Kontext nicht abgesichert sind.

## Manuelle Testhinweise

- Dokumentation auf Vollständigkeit und eindeutige Abgrenzung der Zustände prüfen.
- Prüfen, dass die Matrix auch ohne Kenntnis interner Implementierungsdetails verständlich ist.

## Offene Fragen

- Keine Angaben
