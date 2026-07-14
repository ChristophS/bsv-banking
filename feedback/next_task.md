# Nächstes Arbeitspaket

## Titel

Zuordnungsdialoge für Vorgänge, Transaktionen, Belege, Mails, To-Dos und Termine vereinheitlichen

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 3

## Ziel

Einheitliche, vorgangsbasierte Zuordnungsabläufe mit verständlicher Suche, Auswahl, Bestätigung und Fehlerrückmeldung für die bestehenden Dashboard-Entitäten schaffen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Dashboard-UI für Zuordnungsdialoge
- Bestehende Zuordnungs- und Vorgangsservices
- Dashboard-Tests

## Muss umgesetzt werden

- Die bestehenden Zuordnungsdialoge für Vorgänge, Transaktionen, Belege, Mails, To-Dos und Termine auf ein einheitliches Bedienmuster ausrichten.
- Suche und Auswahl verfügbarer Vorgänge verständlich und konsistent darstellen.
- Eine explizite Bestätigung vor dem Speichern einer Zuordnung vorsehen.
- Erfolgreiche Zuordnungen und fachliche oder technische Fehler mit verständlichen Rückmeldungen anzeigen.
- Bestehende Vorgangs-, Verknüpfungs- und Service-Strukturen weiterverwenden.
- Keine direkte Ersatzbeziehung anstelle einer bestehenden vorgangsbasierten Verknüpfung einführen.

## Soll umgesetzt werden

- Gemeinsame UI-Texte und Zustände für Laden, keine Treffer, Auswahl, Speichern und Fehler verwenden.
- Mehrfachklicks oder wiederholte Speichervorgänge während laufender Aktionen verhindern.
- Bestehende Filter-, Such- und Listenfunktionen ohne unnötige zusätzliche Datenabfragen integrieren.

## Nicht Teil dieses Arbeitspakets

- Neue fachliche Entitäten oder ein neues Zuordnungsmodell einführen.
- Klassifikations- oder Abschlussblocker überarbeiten.
- Die allgemeine Performance- und Bedienbarkeitsprüfung aller datenintensiven Listen durchführen.
- Neue Mail-, Banking-, DFBnet- oder externe Integrationen entwickeln.
- Unabhängige Funktionen außerhalb der Zuordnungsdialoge umbauen.

## Akzeptanzkriterien

- Alle sechs genannten Entitätstypen verwenden für die Zuordnung ein konsistentes Bedien- und Rückmeldemuster.
- Eine Zuordnung kann nur nach Auswahl eines Vorgangs und expliziter Bestätigung gespeichert werden.
- Nach erfolgreicher Speicherung ist die neue Zuordnung im Dialog oder in der zugehörigen Ansicht erkennbar.
- Bei fehlender Auswahl, keinen Suchtreffern oder einem Speichervalidierungsfehler erhält der Nutzer eine verständliche und handlungsorientierte Rückmeldung.
- Ein laufender Speichervorgang kann nicht versehentlich mehrfach ausgelöst werden.
- Bestehende vorgangsbasierte Verknüpfungen bleiben kompatibel und werden nicht durch direkte Ersatzbeziehungen ersetzt.
- Automatisierte Tests decken mindestens den erfolgreichen Zuordnungsfall, fehlende Auswahl und einen Fehlerfall ab.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete technische Umsetzung und die Wiederverwendung vorhandener Komponenten soll anhand des bestehenden Codes ermittelt werden.
- Fachliche Validierung und bestehende Berechtigungs- oder Fehlerlogik dürfen nicht umgangen werden.
- Externe Dienste sind für Tests ausschließlich mit Mocks, Fakes oder Fixtures zu behandeln.

## Manuelle Testhinweise

- Je einen Zuordnungsdialog für eine Transaktion und einen weiteren Entitätstyp öffnen.
- Nach einem Vorgang suchen, ihn auswählen und die Zuordnung bestätigen.
- Den Dialog ohne Auswahl bestätigen und die Rückmeldung prüfen.
- Einen Suchbegriff ohne Treffer verwenden und die Darstellung prüfen.
- Während des Speicherns mehrfach auf die Bestätigung klicken und sicherstellen, dass keine Doppelzuordnung entsteht.

## Offene Fragen

- Welche bestehenden Dialogkomponenten oder Endpunkte werden bereits von mehreren Entitätstypen gemeinsam genutzt?
- Welche Unterschiede zwischen den sechs Zuordnungsfällen sind fachlich zwingend und dürfen nicht vereinheitlicht werden?
