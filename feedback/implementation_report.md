# Implementation Report

## Nachbesserung nach Review

- Der Einstieg `unclassified_transactions` setzt jetzt den serverseitigen Filter `unclassified_only=true`. Store und API verwenden exakt dieselbe Regel wie die Dashboard-Kennzahl: Ohne Splits werden die vier Pflichtfelder der Transaktion geprüft, mit Splits die Pflichtfelder jedes Splits. Beim regulären Einstieg in den Transaktions-Tab wird der Arbeitsfilter wieder aufgehoben.
- Der Einstieg `unassigned_documents` fragt Dokumente mit dem serverseitigen Filter `unassigned_only=true` ab und öffnet das erste offene Dokument direkt im vorhandenen Vorgang-Erstell- und Zuordnungsdialog. Das Dokument ist dort bereits ausgewählt und muss nicht mehr über die allgemeine Vorgangsliste gesucht werden.
- Store-, HTTP- und Browser-Tests prüfen den exakten Transaktionsfilter und beim Dokumenteinstieg den geöffneten Zuordnungsdialog samt vorausgewähltem Dokument.
- Nach der Nachbesserung ausgeführt: `& "C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_dashboard.py -q` mit **131 bestanden, 6 übersprungen und 50 bestandenen Subtests**; außerdem `node --check banking_dashboard/static/app.js` und `git diff --check`, beide erfolgreich.
- Die übersprungenen Tests benötigen Playwright beziehungsweise Chromium. Es wurden keine externen Dienste und keine echten Zugangsdaten verwendet.

## Branchname

`agent2/rework-20260714-102409`

## Geänderte Dateien

- `banking_dashboard/server.py`
- `banking_dashboard/static/app.js`
- `banking_dashboard/static/index.html`
- `banking_dashboard/static/styles.css`
- `tests/test_dashboard.py`
- `feedback/implementation_report.md`

## Umgesetzte Punkte

- Die vorhandene Dashboard-Übersicht wurde zu einer sichtbar nummerierten Arbeitsliste mit einer festen fachlichen Reihenfolge erweitert.
- Offene Vorgänge, unklassifizierte Transaktionen, ungelesene Mails, offene To-Dos, nicht zugewiesene Dokumente und anstehende Termine werden mit serverseitig ermittelten Kennzahlen berücksichtigt.
- Die vorhandene Zusatzaufgabe für nicht zugewiesene anstehende Termine bleibt als nachrangiger siebter Einstieg erhalten.
- Jede Karte enthält eine kurze Begründung der Bearbeitungsrelevanz sowie den eindeutigen Zustand `n offen` oder `Nichts offen`.
- Die Zählung unklassifizierter Transaktionen verwendet dieselben Pflichtfelder wie die bestehende Abschlussvalidierung. Bei Transaktionssplits werden die Split-Klassifikationen berücksichtigt.
- Alle Karten führen über die vorhandene Navigation in den jeweiligen Bearbeitungs- oder Zuordnungsbereich. Die bestehenden Vorschauen für Vorgänge, To-Dos und Termine bleiben erhalten.
- Leere Bereiche werden zurückhaltend und ohne Warnfarbe dargestellt.
- Der bestehende API-Wert `unassigned_transactions` bleibt aus Kompatibilitätsgründen erhalten, wird aber nicht mehr fälschlich als Klassifikationsaufgabe angezeigt.

## Nicht umgesetzte Punkte

- Keine neuen Zuordnungsdialoge oder Entitätstabellen.
- Keine Änderungen an Klassifikations- oder Abschlussregeln.
- Keine externen Banking-, Mail-, Microsoft-Graph- oder DFBnet-Aktionen.
- Keine dynamische Neupriorisierung nach Anzahl; die Reihenfolge ist bewusst fachlich stabil, damit hohe Mengen in einem nachrangigen Bereich die Bedeutung der Aufgaben nicht verfälschen.

## Ausgeführte Tests

- `& "C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_dashboard.py`
- `& "C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_dashboard.py -k "overview"`
- `node --check banking_dashboard/static/app.js`
- `git diff --check -- banking_dashboard/server.py banking_dashboard/static/app.js banking_dashboard/static/index.html banking_dashboard/static/styles.css tests/test_dashboard.py feedback/implementation_report.md`

## Testergebnis

- Vollständige Dashboard-Suite: 130 bestanden, 6 übersprungen, 0 fehlgeschlagen.
- Gezielte Übersichtstests nach der abschließenden Split-Korrektur: 4 bestanden, 2 optionale Browsertests übersprungen, 0 fehlgeschlagen.
- JavaScript-Syntaxprüfung: bestanden.
- Diff-Prüfung: bestanden; nur vorhandene Hinweise zur künftigen LF/CRLF-Konvertierung.

## Bekannte Einschränkungen

- Die sechs übersprungenen Tests benötigen Playwright beziehungsweise einen lokal installierten Chromium-Browser. Es wurden keine Browser-Automationen gegen externe Dienste gestartet.
- Dokumente besitzen keinen eigenen Haupt-Tab. Der Einstieg verwendet daher repo-konform den bestehenden dokumentbezogenen Vorgangsfluss.
- Die feste Prioritätsreihenfolge ist die kleinste sichere Annahme mangels einer im Repository hinterlegten abweichenden Fachentscheidung: zuerst Buchungsklassifikation, dann zentrale Vorgänge, anschließend To-Dos, Mails, Dokumente und Termine.

## Hinweise für den Review-Agenten

- Besonders zu prüfen sind die Prioritätsmetadaten und Zustände in `overview_counts()` sowie deren Darstellung in `renderOverview()`.
- Die neue Transaktionskennzahl unterscheidet bewusst zwischen unklassifiziert und lediglich noch keinem Vorgang zugewiesen.
- Bei gesplitteten Transaktionen zählt eine Buchung als offen, sobald mindestens ein Split unvollständig klassifiziert ist; die Felder der Ursprungstransaktion werden dann nicht zusätzlich bewertet.
- Vorhandene, nicht zu diesem Paket gehörende Änderungen an `feedback/Review-report.md` sowie die unversionierte Prompt-Datei wurden nicht verändert.
