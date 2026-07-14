# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Verhaltensbasierte Tests für die drei Zustände der To-do- und Terminlisten ergänzen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5.1

**Priorität:** mittel

**Grund:** Der Review weist darauf hin, dass die bestehenden neuen Tests statisch sind und die Zustandslogik für To-dos und Termine robuster verhaltensbasiert abgesichert werden kann.

**Feedback:**

- Verhaltensbasierte Absicherung der drei Zustände: leerer Bestand, keine Übereinstimmung durch Suche oder Filterung, Ladefehler.
- Möglichst ohne externe Dienste und mit den bestehenden Dashboard-Komponenten.

## 2. Eine kompakte Zustandsmatrix für alle datenintensiven Dashboard-Listen dokumentieren

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5.2

**Priorität:** niedrig

**Grund:** Für die Bedienbarkeit der datenintensiven Listen ist eine kompakte Übersicht der Zustände hilfreich und wurde als sinnvolle Folgeverbesserung genannt.

**Feedback:**

- Zustände der relevanten Dashboard-Listen übersichtlich gegenüberstellen.
- Leerer Bestand, Such-/Filtertreffer und Ladefehler klar voneinander abgrenzen.

## 3. Bei Ladefehlern Ergebniszähler und gegebenenfalls alte Filterresultate konsistent als nicht verfügbar oder fehlgeschlagen kennzeichnen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5.3

**Priorität:** mittel

**Grund:** Der Review nennt als Nacharbeit, dass Ergebniszähler bei Ladefehlern noch alte Werte zeigen können und damit inkonsistent zum Fehlzustand wirken.

**Feedback:**

- Bei Fehlerzuständen die Anzeige der Ergebniszähler fachlich konsistent machen.
- Vorherige Filterresultate bei Ladefehlern nicht irreführend fortführen.
