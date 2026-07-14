# Nächstes Arbeitspaket

## Titel

Übersicht als priorisierte Arbeitsliste für offene Kassierer-Aufgaben verbessern

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 2

## Ziel

Das Dashboard soll offene Kassierer-Aufgaben anhand klarer Kennzahlen und verständlicher Prioritäten als direkt bearbeitbare Arbeitsliste darstellen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css

## Wahrscheinliche Änderungsstellen

- Dashboard-Kennzahlen und Datenaufbereitung
- Darstellung der priorisierten offenen Aufgaben
- Verlinkung oder Navigation zu den jeweiligen Bearbeitungsbereichen

## Muss umgesetzt werden

- Offene Vorgänge, unklassifizierte Transaktionen, Mails, To-Dos, Dokumente und Termine als verständliche Arbeitsbereiche berücksichtigen.
- Für jeden Arbeitsbereich eine nachvollziehbare Kennzahl oder einen klaren offenen Zustand anzeigen.
- Die Arbeitsbereiche nach fachlicher Dringlichkeit beziehungsweise Bearbeitungsrelevanz priorisiert darstellen.
- Jeder relevante Einstieg muss direkt in den bestehenden Bearbeitungs- oder Zuordnungsfluss führen.
- Bestehende Vorgangsstrukturen und vorhandene Services beziehungsweise Verknüpfungen weiterverwenden.

## Soll umgesetzt werden

- Leere Zustände verständlich und ohne irreführende Warnungen darstellen.
- Die Darstellung so umsetzen, dass typische Kassierer-Aufgaben ohne zusätzliche Recherche erkennbar sind.
- Bestehende Dashboard-Funktionen und deren Performance unverändert erhalten.

## Nicht Teil dieses Arbeitspakets

- Vereinheitlichung der Zuordnungsdialoge für mehrere Entitätstypen
- Änderung von Klassifikations- oder Abschlussregeln
- Grundlegender Neuaufbau der Vorgangsarchitektur
- Umsetzung externer Banking-, Mail-, Microsoft-Graph- oder DFBnet-Aktionen
- Umfassende Optimierung aller datenintensiven Listen

## Akzeptanzkriterien

- Das Dashboard zeigt offene Vorgänge, unklassifizierte Transaktionen, Mails, To-Dos, Dokumente und Termine in einer priorisierten Übersicht oder weist einen nachvollziehbaren leeren Zustand aus.
- Die angezeigten Zahlen und Zustände entsprechen den vorhandenen Daten und werden nicht durch reine UI-Schätzungen erzeugt.
- Ein Nutzer kann von jedem vorhandenen offenen Arbeitsbereich aus den zugehörigen Bearbeitungsfluss erreichen.
- Die Anzeige unterscheidet verständlich zwischen offenen, erledigten beziehungsweise nicht vorhandenen Aufgaben.
- Bestehende Dashboard-Funktionen bleiben nutzbar und vorhandene Tests werden nicht unbeabsichtigt beeinträchtigt.
- Die Priorisierung ist im UI erkennbar und enthält keine fachlich nicht begründeten oder widersprüchlichen Zustände.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete technische Umsetzung und Datenabfrage soll anhand des vorhandenen Dashboard-Codes geprüft werden.
- Keine parallele Ersatzlogik für Vorgänge einführen; bestehende fachliche Zählungen und Verknüpfungen nutzen.
- Bei fehlenden Datenquellen eine sichere, klar gekennzeichnete Darstellung vorsehen statt Daten zu erfinden.

## Manuelle Testhinweise

- Dashboard mit mehreren offenen Aufgabentypen laden und prüfen, ob Reihenfolge, Kennzahlen und Einstiege verständlich sind.
- Dashboard mit vollständig erledigten beziehungsweise leeren Bereichen laden und die leeren Zustände prüfen.
- Von jedem angezeigten Arbeitsbereich in den bestehenden Bearbeitungsfluss navigieren.
- Prüfen, dass vorhandene Dashboard-Funktionen weiterhin funktionieren.

## Offene Fragen

- Welche der genannten Bereiche sind im aktuellen Dashboard bereits als Datenquelle verfügbar?
- Welche fachliche Reihenfolge gilt für die Priorisierung, falls mehrere Bereiche gleichzeitig offen sind?
