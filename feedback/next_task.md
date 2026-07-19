# Nächstes Arbeitspaket

## Titel

Dashboard als Startseite mit freier Tab-Navigation gestalten

## Epic

**Epic-ID:** epic-dashboard-navigation

**Epic-Titel:** Dashboard-Navigation und fachliche Übersichten entlasten

**Epic-Ziel:** Das Dashboard soll je Fachbereich unmittelbar die relevanten Inhalte zeigen, ohne dauerhaft sichtbare globale Blöcke als Sichtblocker.

**Teilpaket:** Teil 1

## Ziel

Das Dashboard soll als eigene Startseite dienen und die fachlichen Tabs ohne dauerhaft sichtbare globale Blöcke oder Scroll-Zwang nutzbar machen.

## Relevante Dateien

- banking_dashboard/static/index.html
- banking_dashboard/static/app.js
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Dashboard-Routing und Startseitenzustand
- Tab-Navigation und Inhaltsbereiche
- Dashboard-Layout und responsive Darstellung
- Dashboard-Tests

## Muss umgesetzt werden

- Eine eigenständige Dashboard-Startseite als initiale Ansicht bereitstellen.
- Die fachlichen Tabs frei anwählbar machen, ohne dass ein globaler Block dauerhaft oberhalb jedes Tab-Inhalts angezeigt wird.
- Die offene Arbeit aus der dauerhaften globalen Darstellung innerhalb der Tab-Navigation oder der Startseitenstruktur sinnvoll zugänglich machen.
- Beim Wechsel der Tabs den jeweils gewählten Fachbereich unmittelbar sichtbar anzeigen.
- Die bestehende fachliche Struktur und vorhandene Dashboard-Funktionen weiterverwenden.

## Soll umgesetzt werden

- Den aktiven Tab eindeutig kennzeichnen.
- Den zuletzt gewählten Tab innerhalb der bestehenden Sitzung beibehalten, sofern dies ohne zusätzlichen Umbau möglich ist.
- Die Darstellung auch bei kleineren Bildschirmbreiten ohne unnötigen vertikalen Sichtblocker nutzbar halten.

## Nicht Teil dieses Arbeitspakets

- Die inhaltliche Überarbeitung der Transaktionsansicht oder der Saldokorrekturen.
- Die Mail-Synchronisation.
- Das direkte Abschließen von Vorgängen.
- Ein vollständiger Neuaufbau des Dashboard-Backends oder der bestehenden Vorgangsstrukturen.
- Neue externe Dienste oder echte Banking-Aktionen.

## Akzeptanzkriterien

- Beim Öffnen des Dashboards erscheint eine eigene Startansicht und nicht automatisch ein dauerhaft oberhalb aller Tabs sichtbarer globaler Arbeitsblock.
- Jeder vorhandene fachliche Tab kann direkt ausgewählt werden.
- Nach Auswahl eines Tabs ist dessen Inhalt ohne vorheriges Wegscrollen durch einen globalen Block sichtbar.
- Der aktive Tab ist visuell und programmatisch erkennbar.
- Die offene Arbeit bleibt über die Dashboard-Navigation erreichbar.
- Bestehende Dashboard-Tests bleiben erfolgreich oder werden um Tests für Startansicht und Tab-Wechsel ergänzt.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandene Dashboard-Struktur, Services und Verknüpfungen verwenden.
- Die konkrete technische Umsetzung der Navigation kann der Coding-Agent anhand des Repositorys festlegen.
- Keine fachliche Ersatzbeziehung außerhalb der bestehenden vorgangsbasierten Struktur einführen.

## Manuelle Testhinweise

- Dashboard öffnen und prüfen, dass die Startansicht ohne störenden globalen Sichtblock erscheint.
- Jeden vorhandenen Tab auswählen und prüfen, dass der zugehörige Inhalt unmittelbar sichtbar ist.
- Zwischen Tabs wechseln und prüfen, dass der aktive Tab eindeutig erkennbar bleibt.
- Die Ansicht bei einer schmalen Fensterbreite prüfen.

## Offene Fragen

- Keine Angaben
