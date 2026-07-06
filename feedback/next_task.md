# Nächstes Arbeitspaket

## Titel

Dashboard-Übersichtskarten klickbar machen und in passende Reiter navigieren

## Ziel

Die bestehenden Dashboard-Karten sollen als interaktive Einstiegspunkte dienen und beim Anklicken in den fachlich passenden Reiter wechseln. Dabei sollen vorhandene Filter- und Ladeflüsse wiederverwendet werden, ohne neue Architektur oder neue Datenmodelle einzuführen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Klick-Handling für Overview-Karten, Reiterwechsel und Wiederverwendung vorhandener Reload-/Filterlogik.
- banking_dashboard/static/index.html: Nur falls nötig, semantische Anpassungen an den Karten für Interaktion und Tastaturbedienung.
- banking_dashboard/static/styles.css: Hover-, Fokus- und aktive Zustände für klickbare Karten.
- tests/test_dashboard.py: Regressionstests für Dashboard-Overview und Karten-/Entity-Ausgabe.

## Muss umgesetzt werden

- Overview-Karten in der Oberfläche klickbar machen.
- Jede Karte auf einen bestehenden Reiter mappen: offene Vorgänge -> Vorgänge, ungelesene Mails -> Mails, nicht zugewiesene Transaktionen -> Transaktionen, offene To-Dos -> To-Dos, nicht zugewiesene Dokumente -> Belege/Dokumente, anstehende Termine und nicht zugewiesene Termine -> Termine.
- Beim Navigieren vorhandene Filtermechanismen nutzen, soweit sie bereits existieren, zum Beispiel `hide_completed` für Vorgänge und To-Dos sowie vorhandene Lade-/Suchflüsse für andere Reiter.
- Interaktive Karten per Tastatur erreichbar machen und mit sichtbarem Fokuszustand versehen.
- Keine neue Backend-Logik erfinden, wenn der Zielreiter mit vorhandenen Standardlisten bereits sinnvoll geladen werden kann.

## Soll umgesetzt werden

- Falls einfach möglich, den aktiven Filterzustand im UI sichtbar setzen, damit der Nutzer erkennt, warum die Zielansicht eingeschränkt ist.
- Für Karten ohne passenden Serverfilter die Navigation zum richtigen Reiter bevorzugen statt eine größere neue Filterlogik einzubauen.

## Nicht Teil dieses Arbeitspakets

- Größere Dashboard-Neustrukturierung oder neue Navigationsarchitektur.
- Neue globale Such- oder Filterkonzepte über mehrere Reiter hinweg.
- Neue automatische Vorgangserstellung oder neue Verknüpfungsheuristiken.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spendenbescheinigungsmodul mit Adressdatenbank und DFBnet-Integration.

## Akzeptanzkriterien

- Ein Klick auf eine Overview-Karte öffnet den fachlich passenden Reiter.
- Die Karten für offene Vorgänge, offene To-Dos und ungelesene Mails führen direkt in eine nutzbare Arbeitsansicht ohne manuelle Zwischenschritte.
- Für Vorgänge, To-Dos und Transaktionen werden vorhandene Filtermechanismen genutzt, sodass die Zielansicht erkennbar auf den Kartenkontext zugeschnitten ist.
- Die Karten sind per Tastatur fokussierbar und auslösbar.
- Bestehende Dashboard-Funktionen in den Zielreitern bleiben unverändert nutzbar.
- Bestehende Tests laufen weiter und decken die Karten-/Overview-Integration regressionssicher ab.

## Hinweise für den Umsetzungs-Agenten

- Die API liefert bei `/api/overview` bereits `cards` mit `entity`; diese Information sollte im Frontend als primärer Routing-Anker dienen.
- Vor einer Backend-Änderung in `app.js` prüfen, wie Reiterwechsel und jeweilige Reload-Funktionen heute ausgelöst werden, und diese direkt wiederverwenden.
- Falls mehrere Karten auf dieselbe Entity `termine` zeigen, im Frontend pro `key` unterschiedlich reagieren, nicht nur pro `entity`.
- Für `unassigned_documents` und `unassigned_transactions` lieber zunächst sauber zum passenden Reiter navigieren, statt neue Serverfilter zu erfinden, wenn das Paket klein bleiben soll.

## Manuelle Testhinweise

- Dashboard öffnen und jede Overview-Karte einzeln anklicken.
- Prüfen, dass der erwartete Reiter aktiv wird und die Liste lädt.
- Mit Tastatur per Tab auf die Karten navigieren und per Enter oder Space auslösen.
- Für offene Vorgänge und To-Dos prüfen, dass abgeschlossene Einträge nicht unnötig im Fokus stehen, falls vorhandene Hide-Filter aktiviert werden.
- Regressionstest: normale Nutzung der Reiter ohne Klick über die Karten bleibt möglich.

## Offene Fragen

- Wie setzt `app.js` aktuell den aktiven Reiter und den Filterzustand intern genau um; falls dies verstreut ist, sollte die Umsetzung dort konsolidiert werden, ohne die Architektur umzubauen.
