# Nächstes Arbeitspaket

## Titel

Klassifikationsvorschläge im Split-Editor an bestehende Kategorien koppeln

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.2

## Ziel

Split-Zeilen sollen im vorhandenen Split-Editor dieselben nutzbaren Klassifikationsvorschläge und Kategorieabhängigkeiten wie Transaktionen erhalten, damit Teilbeträge konsistent einzeln klassifiziert werden können.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Split-Editor und seine Zeilen-Renderfunktion in banking_dashboard/static/app.js
- Bestehende Datalist- beziehungsweise Auswahl-Elemente in banking_dashboard/static/index.html
- Nutzung oder bei Bedarf schmale Erweiterung von DashboardDataStore.classification_options in banking_dashboard/server.py
- Dashboard-API- und UI-nahe Tests in tests/test_dashboard.py

## Muss umgesetzt werden

- Die vorhandenen Klassifikationsoptionen aus GET /api/classification-options im Split-Editor verwenden, ohne eine zweite Kategorienquelle einzuführen.
- Für jede Split-Zeile Vorschläge für Transaktionstyp und Oberkategorie bereitstellen.
- Unterkategorie in einer Split-Zeile erst nach einer befüllten Oberkategorie aktivieren und nur die zu dieser Oberkategorie passenden vorhandenen Unterkategorien vorschlagen.
- Beim Wechsel von Oberkategorie oder Unterkategorie die vorhandene Sphären-Vorauswahl aus den bestehenden Optionen für genau diese Kombination anwenden, ohne eine bereits manuell gesetzte Sphäre stillschweigend zu überschreiben.
- Sicherstellen, dass die gewählten Werte weiterhin im bestehenden Split-Payload gespeichert und nach erneutem Laden der Transaktionsdetails angezeigt werden.
- Automatisierte Tests für die bereitgestellten Klassifikationsoptionen und mindestens einen Split-Editor-Flow ergänzen oder anpassen.

## Soll umgesetzt werden

- Leere Optionen und fehlende Kategorie-Kombinationen verständlich behandeln, sodass weiterhin freie Texteingaben möglich bleiben.
- Die Bedienung an die bestehende Transaktionsklassifikation angleichen, damit Feldnamen, Vorschlagsverhalten und Sphärenwerte konsistent sind.
- Bestehende Split-Werte beim erneuten Rendern unverändert übernehmen.

## Nicht Teil dieses Arbeitspakets

- Änderungen am Split-Datenmodell, an Split-Summenvalidierung oder an der bestehenden Split-Speicher-API.
- Ableitung oder Änderung von Vorgangsstatus anhand von Split-Klassifikationen.
- Neue Zuordnungen zwischen Split-Zeilen, Rechnungen, Belegen oder Transaktionen.
- Automatische Klassifikationsregeln auf Split-Zeilen anwenden.
- Grundlegender Umbau der Vorgangs-, Beleg- oder Transaktionsarchitektur.

## Akzeptanzkriterien

- Beim Öffnen einer Transaktion mit Split-Zeilen stehen in jeder Split-Zeile Vorschläge für Transaktionstyp und Oberkategorie aus den bestehenden Klassifikationsoptionen zur Verfügung.
- Eine Unterkategorie kann in einer Split-Zeile erst nach Wahl einer Oberkategorie sinnvoll ausgewählt werden und die Vorschlagsliste enthält nur passende Werte.
- Für bekannte Ober-/Unterkategorie-Kombinationen wird die vorhandene bevorzugte Sphäre nur als Vorauswahl gesetzt, wenn die Split-Zeile noch keine Sphäre enthält.
- Manuell eingegebene oder bereits gespeicherte Klassifikationswerte einer Split-Zeile werden nicht durch das Laden von Vorschlägen überschrieben.
- Nach Speichern und erneutem Abruf über den bestehenden Split-Endpunkt bleiben Klassifikationsfelder und Reihenfolge der Split-Zeilen erhalten.
- Die Testausführung benötigt keinen Browser, keine Bankverbindung und keine externen Dienste.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandene API GET /api/classification-options und ihre Struktur mit transaction_types, top_categories, sub_categories, sphere_defaults und spheres wiederverwenden.
- Die bestehende PUT-Route /api/transactions/<transaktions_id>/splits unverändert als Persistenzweg verwenden.
- Keine neue direkte Beziehung zwischen Split, Beleg oder Rechnung anlegen; spätere Zuordnungsfälle bleiben vorgangsbasiert.
- Die UI darf keine produktiven externen Aktionen auslösen.

## Manuelle Testhinweise

- Eine vorhandene Transaktion mit mindestens zwei Split-Zeilen im Dashboard öffnen.
- In der ersten Zeile Oberkategorie setzen und prüfen, dass nur passende Unterkategorien vorgeschlagen werden.
- Eine bekannte Ober-/Unterkategorie-Kombination wählen und prüfen, dass eine leere Sphäre sinnvoll vorausgefüllt wird.
- In einer zweiten Zeile eine manuelle Sphäre eintragen, Kategorie ändern und prüfen, dass die manuelle Sphäre erhalten bleibt.
- Splits speichern, Detailansicht schließen und erneut öffnen; Klassifikationen müssen unverändert sichtbar sein.

## Offene Fragen

- Keine Angaben
