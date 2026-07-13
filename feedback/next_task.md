# Nächstes Arbeitspaket

## Titel

Kassierer-Workflows und Reibungspunkte im Dashboard strukturiert analysieren

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 1

## Ziel

Die wichtigsten täglichen Arbeitsabläufe beim Sichten, Klassifizieren, Zuordnen und Abschließen von Vorgängen aus Kassierersicht erfassen, konkrete Reibungspunkte priorisieren und daraus umsetzbare Folgearbeiten ableiten.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Die zentralen Kassierer-Workflows für Vorgänge, Transaktionen, Belege, Mails, To-Dos und Termine strukturiert beschreiben.
- Je Workflow Einstieg, erforderliche Bearbeitungsschritte, Zustände, Abschlussbedingungen und mögliche Abbrüche erfassen.
- Reibungspunkte und Verständlichkeitsprobleme aus Sicht der allgemeinen Vereinsverwaltung identifizieren.
- Die Erkenntnisse nach fachlicher Wirkung und Dringlichkeit priorisieren.
- Aus der Analyse klar abgegrenzte Folgepakete für die Dashboard-Übersicht, Zuordnungsdialoge, Abschlussblocker und Listenbedienung ableiten.

## Soll umgesetzt werden

- Bestehende Vorgänge als zentrales fachliches Objekt und vorhandene Verknüpfungen bei der Analyse berücksichtigen.
- Doppelte oder widersprüchliche Bearbeitungsschritte zwischen den Entitätstypen kenntlich machen.
- Prüfen, ob ein Problem durch bessere Orientierung oder Rückmeldung lösbar ist, ohne bestehende Validierung zu umgehen.
- Auswirkungen auf Leistung und bestehenden Funktionsumfang ausdrücklich festhalten.

## Nicht Teil dieses Arbeitspakets

- Keine Implementierung von UI-, API- oder Datenmodelländerungen.
- Keine Neugestaltung oder Ablösung der bestehenden Vorgangs-, Beleg-, Transaktions- oder Verknüpfungsarchitektur.
- Keine Aufteilung oder technische Umsetzung der daraus abgeleiteten Folgepakete.
- Keine externen Dienste, Banking-Aktionen oder produktiven Daten.

## Akzeptanzkriterien

- Eine nachvollziehbare Übersicht der relevanten Kassierer-Workflows liegt vor.
- Für jeden betrachteten Workflow sind Einstieg, Kernschritte, Zustände, Abschlussbedingungen und erkennbare Reibungspunkte dokumentiert.
- Die wichtigsten Probleme sind anhand eines einheitlichen Priorisierungsschemas geordnet.
- Mindestens ein klar abgegrenztes Folgepaket für jedes der fachlichen Themen Übersicht, Zuordnung, Abschlussblocker und Listenbedienung ist beschrieben, sofern dafür ein Befund vorliegt.
- Die Analyse enthält keine Empfehlung, bestehende Vorgangsbeziehungen durch direkte Ersatzbeziehungen zu umgehen.
- Die Ergebnisse sind so konkret, dass die Folgepakete unabhängig geplant und in kleinen Branches umgesetzt werden können.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete technische Analyse des Repositorys und die Identifikation der betroffenen Stellen übernimmt der Coding-Agent.
- Die Analyse sollte beobachtbares Nutzerverhalten und fachliche Zustände von späteren technischen Lösungsentscheidungen trennen.
- Ergebnisse und Prioritäten sollen als Grundlage für die nächsten Teilpakete des Epics dienen.

## Manuelle Testhinweise

- Die beschriebenen Workflows anhand typischer lokaler Vereinsverwaltungsfälle gedanklich oder mit vorhandenen lokalen Testdaten nachvollziehen.
- Prüfen, ob jeder identifizierte Reibungspunkt einer konkreten Folgearbeit oder einer begründeten Verwerfung zugeordnet ist.

## Offene Fragen

- Welche konkreten Dashboard-Ansichten und Bearbeitungsabläufe sind aktuell bereits vorhanden?
- Welche Nutzerrollen und typischen Mengen an Vorgängen sollen bei der Priorisierung zugrunde gelegt werden?
