# Nächstes Arbeitspaket

## Titel

Mail-Vorgang-Import: primäre Aktion verständlich benennen und besser erreichbar platzieren

## Ziel

Im bestehenden Mail-Import-Dialog soll die primäre Aktion zum Anlegen oder Abschließen eines Vorgangs verständlicher beschriftet und ohne unnötiges Scrollen erreichbar sein, ohne den bestehenden Import-Flow fachlich zu ändern.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Rendering des Mail-Vorgang-Import-Dialogs, dynamische Button-Beschriftung und ggf. zweite/obere Aktionsleiste mit derselben Submit-Logik.
- banking_dashboard/static/index.html: Falls der Importdialog feste Template-Strukturen oder Container für eine zusätzliche Aktionsleiste benötigt.
- banking_dashboard/static/styles.css: Positionierung der primären Aktion (z. B. sticky oder oben im Formular) und visuelle Trennung von sekundären Aktionen.
- tests/test_dashboard.py: Bestehende Tests auf UI-/HTML-Regressionen und ausgelieferte Assets prüfen, falls dort Frontend-Ausgabe abgesichert wird.

## Muss umgesetzt werden

- Die bisher missverständliche Beschriftung 'Bestätigt importieren' ersetzen.
- Die primäre Aktion abhängig vom Abschlusszustand klar als 'Vorgang anlegen' oder 'Vorgang abschließen' beschriften.
- Sicherstellen, dass der bestehende Import weiterhin denselben Request sendet und das Feld completed unverändert aus dem Formular übernimmt.
- Die primäre Aktion im Dialog so platzieren, dass sie ohne langes Scrollen erreichbar ist.

## Soll umgesetzt werden

- Wenn es mit geringem Aufwand möglich ist, eine zusätzliche identische Aktionsleiste oben im Formular oder eine sticky Aktionsleiste ergänzen.
- Die Button-Beschriftung bei Änderung des Abschluss-Schalters sofort live aktualisieren.
- Sekundäre Aktionen optisch klar von der primären Importaktion trennen.

## Nicht Teil dieses Arbeitspakets

- Änderungen an der fachlichen Abschlussvalidierung von Vorgängen.
- Backend-Refactoring des Mail-Import-Flows.
- Fehlbuchungs-Sonderlogik für automatische Nullung.
- Splitten von Transaktionen oder neue Zuordnungsmodelle.
- Mehrere Dokumente auf verschiedene Transaktionen innerhalb eines Vorgangs.
- Dashboard-Startseite mit Widgets.
- Änderungen an anderen Mail-Aktionen wie Zusammenfassung, Lesen, Taggen oder Antworten.

## Akzeptanzkriterien

- Im Mail-Vorgang-Import ist die primäre Aktion ohne Scrollen bis ganz nach unten praktikabel erreichbar.
- Die UI zeigt nicht mehr den Text 'Bestätigt importieren'.
- Bei offenem Abschluss-Häkchen lautet die primäre Aktion sinngemäß 'Vorgang anlegen'.
- Bei gesetztem Abschluss-Häkchen lautet die primäre Aktion sinngemäß 'Vorgang abschließen'.
- Ein Import ohne gesetzten Abschluss erzeugt weiterhin einen offenen Vorgang über den bestehenden Flow.
- Ein Import mit gesetztem Abschluss nutzt weiterhin den bestehenden completed-Flow; Erfolg oder Ablehnung erfolgt wie bisher über die bestehende Backend-Logik.
- Vorhandene Dashboard-Funktionalität außerhalb dieses Dialogs bleibt unverändert.

## Hinweise für den Umsetzungs-Agenten

- Im Backend ist der bestehende Mail-Vorgang-Import bereits auf completed ausgelegt; das Paket sollte deshalb voraussichtlich frontendseitig gelöst werden.
- Die Button-Beschriftung sollte an den aktuellen Formularzustand gekoppelt werden, nicht an spätere Response-Felder wie direct_completion.
- Falls das Importformular in app.js dynamisch zusammengesetzt wird, gezielt die Aktionssektion anpassen statt ein neues Template-System einzuführen.
- Wenn sowohl eine obere als auch eine untere Aktion angeboten wird, müssen beide dieselbe Submit-Logik verwenden.

## Manuelle Testhinweise

- Mail-Reiter öffnen, eine Mail analysieren und den Vorgang-Import-Dialog öffnen.
- Prüfen, dass die primäre Aktion sichtbar oder schnell erreichbar ist, ohne bis zum Formularende zu scrollen.
- Abschluss-Checkbox aus- und einschalten und beobachten, ob sich die Button-Beschriftung passend zwischen offenem Anlegen und Abschließen ändert.
- Import einmal ohne Abschluss und einmal mit Abschluss auslösen; prüfen, dass die bestehende Erfolgs- oder Fehlermeldung weiter funktioniert.
- Kurz gegenprüfen, dass andere Mail-Aktionen unverändert bleiben.

## Offene Fragen

- Soll die bessere Erreichbarkeit eher über eine sticky Toolbar oder über eine zusätzliche obere Aktionsleiste umgesetzt werden?
- Falls im UI mehrere Submit-Kontexte existieren, soll die Beschriftung an allen Stellen vereinheitlicht werden oder nur im Mail-Vorgang-Import?
