# Nächstes Arbeitspaket

## Titel

Overview-Routing für bestehende Kacheln zentralisieren

## Ziel

Die Navigation von der Overview auf die bestehenden Zielbereiche soll in der Frontend-Logik über eine zentrale Mapping-Stelle vereinheitlicht werden, ohne das Verhalten der vorhandenen Kacheln zu ändern.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: bestehende Klickbehandlung oder Tab-Navigation der Overview-Kacheln auf eine zentrale Zuordnungstabelle umstellen
- banking_dashboard/static/index.html: nur falls für die vorhandenen Kacheln stabile data-Attribute oder kleine Marker zur Zuordnung fehlen
- tests/test_dashboard.py: vorhandene Absicherung des Klickpfads um den refaktorierten Routing-Weg herum beibehalten oder gezielt präzisieren

## Muss umgesetzt werden

- Die Zuordnung von Overview-Kachel zu Zielbereich in banking_dashboard/static/app.js an einer zentralen Stelle bündeln.
- Vorhandene Kacheln weiterhin auf dieselben Zielbereiche führen wie bisher.
- Doppelte oder verstreute if/switch-Logik für die bereits unterstützten Kacheln reduzieren, soweit dies ohne Verhaltensänderung möglich ist.
- Bestehende Tests so absichern, dass die Kachel-Navigation auch nach dem Refactoring nachweislich funktioniert.

## Soll umgesetzt werden

- Falls passend, stabile data-Attribute oder klar benannte Konstanten für die Kachel-Zuordnung verwenden statt textbasierter Fallunterscheidung.
- Das Mapping so formulieren, dass spätere zusätzliche Kacheln leichter ergänzt werden können, ohne dieses Paket auf weitere Fachlogik auszudehnen.

## Nicht Teil dieses Arbeitspakets

- Neue Overview-Kacheln oder neue Zielbereiche hinzufügen
- Fachliche Änderungen an Transaktionen, Vorgängen, Mails, To-Dos oder Budget
- Größere UI-Überarbeitung der Overview
- Backend- oder API-Erweiterungen ohne direkten Bedarf für das Frontend-Refactoring

## Akzeptanzkriterien

- Alle bereits unterstützten Overview-Kacheln navigieren nach dem Refactoring weiterhin in den jeweils korrekten Bereich.
- Die Zuordnungslogik liegt in app.js nicht mehr verstreut, sondern erkennbar zentralisiert vor.
- Es gibt keine Verhaltensänderung bei bestehenden Tabs oder Filtern außerhalb des Kachel-Routings.
- Die relevanten Dashboard-Tests laufen weiterhin erfolgreich und decken den Klickpfad der Overview-Kacheln ab.

## Hinweise für den Umsetzungs-Agenten

- Dieses Paket ist ausdrücklich ein kleines Wartbarkeits-Refactoring auf dem bereits funktionierenden Klickpfad aus dem letzten Review-Kontext.
- Da app.js, index.html und die Dashboard-Tests bereits geladen sind, sollten die vorhandenen IDs, Tab-Namen oder Frontend-Aktionen exakt weiterverwendet werden statt neue Benennungen einzuführen.
- Falls die aktuelle Logik bereits teilweise zentral ist, reicht auch eine kleine Präzisierung oder Vereinheitlichung; kein künstlich großes Refactoring daraus machen.
- Bei Testanpassungen Fokus auf beobachtbares Verhalten legen: Klick auf Kachel -> erwarteter Bereich aktiv bzw. erwartete Navigationsfunktion ausgelöst.

## Manuelle Testhinweise

- Dashboard lokal öffnen und nacheinander die vorhandenen Overview-Kacheln anklicken.
- Prüfen, dass jeweils derselbe Bereich geöffnet wird wie vor dem Refactoring.
- Zusätzlich kurz testen, dass direkte Tab-Wechsel außerhalb der Overview unverändert funktionieren.

## Offene Fragen

- Keine blockierende offene Frage; falls einzelne Kacheln aktuell absichtlich Sonderlogik verwenden, sollte diese nur dann im Mapping bleiben, wenn Tests oder bestehende UI-Struktur sie tatsächlich benötigen.
