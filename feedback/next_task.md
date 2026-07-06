# Nächstes Arbeitspaket

## Titel

UI-Test für Overview-Kachel „Nicht zugewiesene Dokumente“ ergänzen

## Ziel

Den bestehenden Klickpfad über die Overview-Kachel `unassigned_documents` absichern, damit ein Klick auf die echte Kachel zuverlässig in den Dokumente-/Belege-Bereich führt.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- tests/test_dashboard.py: neuer gezielter Test für die Kachel `unassigned_documents` und das erwartete Routing-Ziel `documents`.
- banking_dashboard/static/app.js: nur minimale Anpassung, falls der Test eine kleine Unschärfe im Klick-Handling oder im Bereichswechsel offenlegt.
- banking_dashboard/static/index.html: nur falls ein stabiler Selektor/Hook für den Test fehlt; keine funktionale UI-Änderung.

## Muss umgesetzt werden

- Einen expliziten Test ergänzen, der die echte Overview-Kachel `unassigned_documents` abdeckt und bestätigt, dass der Klick in den Dokumente-/Belege-Bereich führt.
- Dabei nicht nur die API-Daten prüfen, sondern den tatsächlichen Frontend-Klickpfad absichern.
- Falls dabei ein bestehender Fehler sichtbar wird, nur den minimal nötigen Fix im vorhandenen Routing-/Klick-Flow umsetzen.

## Soll umgesetzt werden

- Im Test die fachlich sichtbaren Kennzeichen mitprüfen, insbesondere Kachel-Key/Label und Zielbereich `documents` bzw. Belege.
- Wenn es bereits ähnliche Tests für andere Kacheln gibt, das neue Szenario im gleichen Stil ergänzen.

## Nicht Teil dieses Arbeitspakets

- Zentrale Mapping-Tabelle für weitere Overview-Kacheln.
- Spezifischere Terminfilter für anstehende und nicht zugewiesene Termine.
- Mehrfachzuordnung mehrerer Mail-Dokumente zu unterschiedlichen Transaktionen innerhalb eines Vorgangs.
- Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration.

## Akzeptanzkriterien

- Es gibt in `tests/test_dashboard.py` einen expliziten Test für den Klickpfad der Overview-Kachel `unassigned_documents`.
- Der Test schlägt fehl, wenn die Kachel nicht mehr auf den Dokumente-/Belege-Bereich routet.
- Bestehende Dashboard-Tests bleiben grün.
- Falls Code angepasst wurde, bleibt das sichtbare Verhalten aller anderen Overview-Kacheln unverändert.

## Hinweise für den Umsetzungs-Agenten

- In `server.py` ist die relevante Karte bereits definiert: `key: 'unassigned_documents'`, `label: 'Nicht zugewiesene Dokumente'`, `entity: 'documents'`. Diese Semantik sollte im Test direkt referenziert werden.
- Der Test soll nicht nur eine isolierte Hilfsfunktion prüfen, sondern den tatsächlich genutzten UI-Pfad aus `app.js` abdecken.
- Wenn das Frontend schwer testbar ist, ist ein kleiner testfreundlicher Hook akzeptabel, solange keine neue Architektur entsteht und das Produktionsverhalten unverändert bleibt.

## Manuelle Testhinweise

- Dashboard starten und die Übersicht öffnen.
- Auf die Kachel `Nicht zugewiesene Dokumente` klicken.
- Prüfen, dass der Dokumente-/Belege-Bereich sichtbar wird und nicht ein anderer Bereich aktiv ist.
- Optional gegenprüfen, dass andere Kacheln weiterhin wie bisher funktionieren.

## Offene Fragen

- Ob `tests/test_dashboard.py` bereits ein Muster für JS-/HTML-Interaktionstests enthält oder ob der neue Test eher als ausgeliefertes Asset-/Selektor-/Routing-Test konstruiert werden muss.
- Welcher konkrete UI-Zustand im Test am stabilsten als Zielsignal dient: aktiver Tab, geladene Dokumentliste oder intern gesetzter Bereichsstatus.
