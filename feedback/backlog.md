# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Kritische Dashboard-API-Flows auf konsistente Eingabevalidierung und Fehlerantworten prüfen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2

**Priorität:** hoch

**Grund:** Nach der Testbaseline sollen die lokalen API-Endpunkte für Transaktionen, Vorgänge, Belege, To-Dos und Termine gezielt auf konsistente Validierung, korrekte Statuscodes und nachvollziehbare Fehlerantworten geprüft werden.

**Feedback:**

- Inbox: gesamten Code auf Konsistenz und Funktion prüfen
- Folgepaket der automatisierten Konsistenz-Baseline

## 2. Persistenz- und Vorgangsverknüpfungen auf Integrität und konsistente Folgeeffekte prüfen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 3

**Priorität:** hoch

**Grund:** Die zentrale Vorgangsarchitektur verknüpft Transaktionen, Belege, Mails, To-Dos und Termine. Änderungen, Löschungen, Abschlussprüfungen und Split-Speicherung müssen Datenintegrität und zulässige N:M-Verknüpfungen zuverlässig erhalten.

**Feedback:**

- Inbox: gesamten Code auf Konsistenz und Funktion prüfen
- Architekturregel: Vorgänge und bestehende Verknüpfungsstrukturen verwenden

## 3. Externe Adapter auf sichere lokale Fehlermodi und Mock-Abdeckung prüfen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 4

**Priorität:** mittel

**Grund:** Banking, Microsoft Graph und DFBnet dürfen keine unkontrollierten produktiven Aktionen ausführen. Ihre Fehler-, Abbruch- und Testpfade müssen daher getrennt mit Mocks, Fakes oder Fixtures geprüft werden.

**Feedback:**

- Inbox: gesamten Code auf Konsistenz und Funktion prüfen
- Projektregel: externe Dienste nur mit Mocks, Fakes oder Fixtures testen

## 4. Kassierer-Workflows und Reibungspunkte im Dashboard strukturiert analysieren

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 1

**Priorität:** hoch

**Grund:** Für maximalen Benutzerkomfort muss zuerst nachvollziehbar beschrieben werden, wie ein Kassierer tägliche Vorgänge bearbeitet: Kontobewegungen sichten, klassifizieren, Belege und Mails zuordnen, offene Arbeit erkennen und Vorgänge abschließen.

**Feedback:**

- Inbox: Nutzerfreundlichkeit aus Sicht der allgemeinen Vereinsverwaltung und Zuordnung prüfen

## 5. Übersicht als priorisierte Arbeitsliste für offene Kassierer-Aufgaben verbessern

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Die vorhandenen Kennzahlen für offene Vorgänge, unklassifizierte Transaktionen, Mails, To-Dos, Dokumente und Termine sollen nach der Workflow-Analyse zu klaren, direkt bearbeitbaren Einstiegspunkten führen.

**Feedback:**

- Inbox: maximalen Benutzerkomfort ohne Leistungs- und Featureeinbußen erreichen
- Vorhaben: Kassiererfreundliche Arbeitsabläufe

## 6. Zuordnungsdialoge für Vorgänge, Transaktionen, Belege, Mails, To-Dos und Termine vereinheitlichen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 3

**Priorität:** mittel

**Grund:** Die zentrale Vorgangsarbeit umfasst mehrere Entitätstypen. Einheitliche Such-, Auswahl-, Bestätigungs- und Fehlerrückmeldungen reduzieren Fehlzuordnungen und verkürzen wiederkehrende Bearbeitungsschritte.

**Feedback:**

- Inbox: Nutzerfreundlichkeit aus Sicht der allgemeinen Vereinsverwaltung und Zuordnung prüfen
- Architekturregel: Vorgänge sind das zentrale fachliche Objekt

## 7. Klassifikations- und Abschlussblocker verständlich und handlungsorientiert darstellen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 4

**Priorität:** mittel

**Grund:** Ein Kassierer muss erkennen können, warum ein Vorgang nicht abgeschlossen werden kann und welche Klassifikationsfelder oder Belege fehlen, ohne Details und vorhandene Validierung zu umgehen.

**Feedback:**

- Inbox: maximalen Benutzerkomfort ohne Leistungs- und Featureeinbußen erreichen
- Bestehender Dashboard-Kontext: Abschlussprüfungen und Klassifikationsstatus

## 8. Bedienbarkeit und Rückmeldungen in datenintensiven Dashboard-Listen prüfen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5

**Priorität:** niedrig

**Grund:** Transaktions-, Vorgangs-, Mail-, Beleg-, To-Do- und Terminlisten müssen bei typischen Vereinsdaten verständlich filterbar, suchbar und performant bleiben; Verbesserungen sollen keine Feature- oder Leistungseinbußen verursachen.

**Feedback:**

- Inbox: Nutzerkomfort ohne Feature- und Leistungseinbußen
