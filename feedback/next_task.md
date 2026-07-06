# Nächstes Arbeitspaket

## Titel

Browser-Test für die Overview-Kachel „Nicht zugewiesene Dokumente“ ergänzen

## Ziel

Die bestehende Overview-Navigation soll durch einen expliziten Test abgesichert werden, der den realen Klickpfad auf die Kachel `unassigned_documents` prüft und sicherstellt, dass die Oberfläche in den Dokumente-Bereich mit dem erwarteten Zustand wechselt.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- tests/test_dashboard.py: Hauptort für den neuen Regressionstest auf den Klick der echten Overview-Kachel.
- banking_dashboard/static/app.js: nur falls der Test eine bestehende Routing-Lücke oder ein nicht testbares Verhalten aufdeckt; hier liegt sehr wahrscheinlich die Kachel-Klicklogik.
- banking_dashboard/static/index.html: nur falls stabile Selektoren oder semantische Markierungen für die Kachel fehlen und minimal ergänzt werden müssen.

## Muss umgesetzt werden

- Einen Test ergänzen, der explizit die echte Overview-Kachel für `unassigned_documents` verwendet statt nur indirekte Routing-Helfer oder generische Mapping-Annahmen zu prüfen.
- Im Test sicherstellen, dass der Klick auf die Kachel zur Dokumentansicht führt und nicht versehentlich in einem anderen Bereich landet.
- Falls die Dokumentansicht beim Klick einen bestimmten Such-/Filterzustand für nicht zugewiesene Dokumente setzen soll, diesen Zustand im Test konkret prüfen.
- Falls der Test einen echten Bug im Frontend-Routing aufdeckt, diesen minimal im bestehenden Code beheben und den Test grün machen.

## Soll umgesetzt werden

- Falls vorhanden, für die Kachel einen stabilen DOM-Selektor oder ein eindeutiges `data-*`-Attribut nutzen, damit der Test robust bleibt.
- Benennung des Tests so wählen, dass klar erkennbar ist, dass hier der konkrete Klickpfad auf die Overview-Kachel regressionsgesichert wird.

## Nicht Teil dieses Arbeitspakets

- Zentrale Vereinfachung des gesamten Overview-Routings über eine neue Mapping-Tabelle.
- Neue Terminfilter für anstehende oder nicht zugewiesene Termine.
- Erweiterungen für mehrere Dokumente pro Mail auf unterschiedliche Transaktionen innerhalb eines Vorgangs.
- Konzeption oder Umsetzung von Spendenbescheinigungen mit DFBnet-/Adressdatenbank-Integration.

## Akzeptanzkriterien

- `tests/test_dashboard.py` enthält einen automatisierten Test, der den Klick auf die Overview-Kachel `unassigned_documents` abdeckt.
- Der Test schlägt fehl, wenn die Kachel nicht in den Dokumente-Bereich navigiert oder den erwarteten Zustand nicht aktiviert.
- Die bestehende Testsuite läuft weiterhin erfolgreich.
- Es werden keine fachlichen Änderungen an Beleg-, Vorgangs- oder Mail-Datenmodellen eingeführt.

## Hinweise für den Umsetzungs-Agenten

- Aus dem bereits geladenen Server-Code ist ersichtlich, dass `overview_counts()` die Karte mit `key = "unassigned_documents"` und `entity = "documents"` liefert; der Test sollte genau diese produktive Schlüsselverwendung absichern.
- Da der Fokus auf der 'echten Kachel' liegt, sollte kein rein unitartiger Test eines Hilfs-Mappings genügen, wenn bereits ein DOM-/App-Fluss testbar ist.
- Falls in `app.js` die Kachel-Klicklogik derzeit über `entity` statt `key` unterscheidet, im Test trotzdem `unassigned_documents` als konkreten Einstieg verwenden, damit spätere Routing-Regressionen erkannt werden.
- Wenn Selektoren instabil sind, bevorzugt minimale Ergänzungen in `index.html` oder erzeugtem Markup gegenüber breitflächigem Refactoring.

## Manuelle Testhinweise

- Dashboard starten und die Overview laden.
- Auf die Kachel `Nicht zugewiesene Dokumente` klicken.
- Prüfen, dass der Dokumente-Bereich geöffnet wird und nur bzw. gezielt nicht zugewiesene Dokumente sichtbar sind, sofern dieser Zustand im UI vorgesehen ist.
- Zusätzlich prüfen, dass andere Overview-Kacheln durch die Änderung nicht beeinträchtigt wurden.

## Offene Fragen

- Soll der Klick auf `unassigned_documents` lediglich den Dokumente-Tab öffnen oder zusätzlich automatisch auf 'nicht zugewiesen' vorfiltern? Falls beides im aktuellen UI nicht eindeutig ist, soll der Test das tatsächlich bestehende Soll-Verhalten aus dem Code absichern.
- Gibt es in `tests/test_dashboard.py` bereits eine Hilfsinfrastruktur für Frontend-/DOM-nahe Tests, die wiederverwendet werden sollte, statt einen neuen Teststil einzuführen?
