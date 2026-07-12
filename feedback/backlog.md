# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Widerruf oder bewussten Ersatz bestehender manueller Saldo-Korrekturen ergänzen

**Epic-ID:** epic-balance-correction

**Epic-Titel:** Manuelle Behandlung abweichender Kontostandsanker

**Epic-Ziel:** Abweichungen zwischen exportierten Bank-Salden und importierten Umsatz-Saldoketten kontrolliert, nachvollziehbar und ohne Veränderung von Originaldaten behandeln.

**Teilpaket:** Teil 3

**Priorität:** mittel

**Grund:** Neben dem Anlegen einer manuellen Korrektur wird ein klar geregelter Weg benötigt, bestehende Korrekturen bewusst zu widerrufen oder zu ersetzen.

**Feedback:**

- Widerruf oder bewussten Ersatz bestehender Korrekturen in einem separaten Arbeitspaket ergänzen.

## 2. API um eine formale Bestätigungsaktion für manuelle Saldo-Korrekturen erweitern

**Epic-ID:** epic-balance-correction

**Epic-Titel:** Manuelle Behandlung abweichender Kontostandsanker

**Epic-Ziel:** Abweichungen zwischen exportierten Bank-Salden und importierten Umsatz-Saldoketten kontrolliert, nachvollziehbar und ohne Veränderung von Originaldaten behandeln.

**Teilpaket:** Teil 4

**Priorität:** mittel

**Grund:** Falls fachliche Prüfung und Anlegen des lokalen Ankers künftig getrennte Schritte werden sollen, braucht die API eine explizite Bestätigungsaktion.

**Feedback:**

- Die API um eine formale Bestätigungsaktion erweitern, falls die fachliche Prüfung und das Anlegen des Ankers künftig getrennte Schritte werden sollen.

## 3. Kritische Dashboard-API-Flows auf konsistente Eingabevalidierung und Fehlerantworten prüfen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2

**Priorität:** hoch

**Grund:** Lokale API-Endpunkte für Transaktionen, Vorgänge, Belege, To-Dos und Termine sollen auf einheitliche Validierung, korrekte Statuscodes und nachvollziehbare Fehlerantworten geprüft werden.

**Feedback:**

- gesamten Code auf Konsistenz und Funktion prüfen
- Folgepaket der automatisierten Konsistenz-Baseline

## 4. Persistenz- und Vorgangsverknüpfungen auf Integrität und konsistente Folgeeffekte prüfen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 3

**Priorität:** hoch

**Grund:** Änderungen, Löschungen, Abschlussprüfungen und Split-Speicherung müssen die Datenintegrität sowie die zulässigen N:M-Verknüpfungen zwischen Transaktionen, Vorgängen, Belegen, Mails, To-Dos und Terminen erhalten.

**Feedback:**

- gesamten Code auf Konsistenz und Funktion prüfen
- Architekturregel: Vorgänge und bestehende Verknüpfungsstrukturen verwenden

## 5. Externe Adapter auf sichere lokale Fehlermodi und Mock-Abdeckung prüfen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 4

**Priorität:** mittel

**Grund:** Banking, Microsoft Graph und DFBnet dürfen keine unkontrollierten produktiven Aktionen ausführen; Fehler-, Abbruch- und Testpfade müssen deshalb getrennt mit Mocks, Fakes oder Fixtures geprüft werden.

**Feedback:**

- gesamten Code auf Konsistenz und Funktion prüfen
- Projektregel: externe Dienste nur mit Mocks, Fakes oder Fixtures testen

## 6. Kassierer-Workflows und Reibungspunkte im Dashboard strukturiert analysieren

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 1

**Priorität:** hoch

**Grund:** Vor UI-Änderungen sollen die täglichen Abläufe beim Sichten, Klassifizieren, Zuordnen und Abschließen von Vorgängen aus Kassierersicht nachvollziehbar erfasst und priorisiert werden.

**Feedback:**

- Nutzerfreundlichkeit aus Sicht der allgemeinen Vereinsverwaltung und Zuordnung prüfen

## 7. Übersicht als priorisierte Arbeitsliste für offene Kassierer-Aufgaben verbessern

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 2

**Priorität:** mittel

**Grund:** Kennzahlen für offene Vorgänge, unklassifizierte Transaktionen, Mails, To-Dos, Dokumente und Termine sollen zu klaren, direkt bearbeitbaren Einstiegspunkten führen.

**Feedback:**

- maximalen Benutzerkomfort ohne Leistungs- und Featureeinbußen erreichen
- Vorhaben: Kassiererfreundliche Arbeitsabläufe

## 8. Zuordnungsdialoge für Vorgänge, Transaktionen, Belege, Mails, To-Dos und Termine vereinheitlichen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 3

**Priorität:** mittel

**Grund:** Einheitliche Suche, Auswahl, Bestätigung und Fehlerrückmeldungen sollen Fehlzuordnungen reduzieren und wiederkehrende Bearbeitungsschritte beschleunigen, ohne die Vorgangsarchitektur zu umgehen.

**Feedback:**

- Nutzerfreundlichkeit aus Sicht der allgemeinen Vereinsverwaltung und Zuordnung prüfen
- Architekturregel: Vorgänge sind das zentrale fachliche Objekt

## 9. Klassifikations- und Abschlussblocker verständlich und handlungsorientiert darstellen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 4

**Priorität:** mittel

**Grund:** Kassierer sollen erkennen können, warum ein Vorgang nicht abgeschlossen werden kann und welche Klassifikationsfelder oder Belege fehlen, ohne bestehende Validierung zu umgehen.

**Feedback:**

- maximalen Benutzerkomfort ohne Feature- und Leistungseinbußen
- Bestehender Dashboard-Kontext: Abschlussprüfungen und Klassifikationsstatus

## 10. Bedienbarkeit und Rückmeldungen in datenintensiven Dashboard-Listen prüfen

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 5

**Priorität:** niedrig

**Grund:** Transaktions-, Vorgangs-, Mail-, Beleg-, To-Do- und Terminlisten sollen bei typischen Vereinsdaten verständlich filterbar, suchbar und performant bleiben.

**Feedback:**

- Nutzerkomfort ohne Feature- und Leistungseinbußen
