# Nächstes Arbeitspaket

## Titel

Split-Editor im Transaktionsdetail um Vorgangszuordnung und Beleghinweise erweitern

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 5

## Ziel

Im bestehenden Transaktionsdetail sollen Split-Zeilen einem bereits mit der Transaktion verknüpften Vorgang zugeordnet werden können. Dabei sollen die zugehörigen Rechnungsbelege als Hinweis zum ausgewählten Vorgang sichtbar sein, ohne neue direkte Beziehungen zwischen Transaktionen und Belegen einzuführen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Transaktionsdetail und bestehender Split-Editor in banking_dashboard/static/app.js
- HTML-Struktur oder Vorlagenbereiche für das Transaktionsdetail in banking_dashboard/static/index.html
- Darstellung von Split-Zeilen, Vorgangsauswahl und Beleghinweisen in banking_dashboard/static/styles.css
- Bestehende GET-/PUT-Endpunkte /api/transactions/<id>/splits in banking_dashboard/server.py
- Dashboard-HTTP- und UI-nahe Regressionstests in tests/test_dashboard.py

## Muss umgesetzt werden

- Im bestehenden Split-Editor je Split-Zeile eine Auswahl der von der Split-API gelieferten zulässigen Vorgänge anbieten.
- Die Auswahl ausschließlich über das vorhandene Feld vorgangs_id in der bestehenden Split-Payload speichern; keine neue direkte Transaktion-Beleg-Verknüpfung und keine neue fachliche Entität einführen.
- Zu jedem auswählbaren Vorgang dessen Titel, Status und vorhandene Belege aus zulaessige_vorgaenge verständlich anzeigen; Rechnungsbelege müssen als Information zum gewählten Vorgang erkennbar sein.
- Beim erneuten Laden des Transaktionsdetails die gespeicherte Vorgangszuordnung jeder Split-Zeile korrekt vorauswählen und die sichtbaren Beleginformationen aktualisieren.
- Die bestehende Betrags-, Summen- und Klassifikationsbearbeitung des Split-Editors unverändert funktionsfähig halten.
- Automatisierte Tests für die Serialisierung beziehungsweise Speicherung einer Split-Vorgangszuordnung und für die Anzeige der zulässigen Vorgangs- und Belegdaten ergänzen.

## Soll umgesetzt werden

- Eine leere Auswahl als explizit nicht zugeordnet kennzeichnen.
- Vorgänge ohne Belege und Vorgänge mit mehreren Belegen eindeutig unterscheiden.
- Eine kurze Hilfebeschreibung ergänzen, dass Belege dem Vorgang und nicht unmittelbar dem Split oder der Transaktion zugeordnet werden.

## Nicht Teil dieses Arbeitspakets

- Neue Datenbanktabellen oder Änderungen an transaction_splits, vorgaenge, transaktion_vorgaenge oder vorgang_belege.
- Automatisches Erzeugen zusätzlicher Vorgänge, Rechnungen oder Belege aus Split-Zeilen.
- Eine generische Zuordnung einer Rechnung zu beliebigen Transaktionen außerhalb der bereits zur Transaktion verknüpften Vorgänge.
- Änderungen an Split-Klassifikations- oder Statusableitungslogik.
- Der separate Mail-Dokumentzuordnungs-Workflow.
- Externe Banking-, Mail-, DFBnet- oder Microsoft-Graph-Aktionen.

## Akzeptanzkriterien

- Eine Split-Zeile kann im Transaktionsdetail einem vorhandenen, mit derselben Transaktion verknüpften Vorgang zugeordnet oder wieder auf keine Zuordnung gesetzt werden.
- Nach dem Speichern und erneuten Abrufen über GET /api/transactions/<id>/splits enthält die betreffende Split-Zeile die gewählte vorgangs_id.
- Die Oberfläche zeigt für zulässige Vorgänge mindestens Vorgangstitel oder ID, Status sowie die zugehörigen Belegnamen an; bei Rechnungsbelegen ist der Bezug nachvollziehbar sichtbar.
- Die Oberfläche bietet keine Vorgänge an, die nicht in zulaessige_vorgaenge der betroffenen Transaktion enthalten sind.
- Die Split-Summe muss weiterhin exakt dem Transaktionsbetrag entsprechen; eine reine Vorgangszuordnung verändert keine Split-Beträge.
- Bestehende Dashboard-Tests und neue Tests laufen ohne Zugriff auf produktive Datenbanken, Dateien, Mails oder externe Dienste.

## Hinweise für den Umsetzungs-Agenten

- Die serverseitig vorhandene Methode transaction_splits liefert bereits splits und zulaessige_vorgaenge; diese Datenquelle im UI wiederverwenden statt eine parallele Auswahl-API zu schaffen.
- Das Speichern weiterhin gesammelt über PUT /api/transactions/<id>/splits mit dem bestehenden Feld splits ausführen.
- Beleginformationen nur aus den über den Vorgang gelieferten belege-Daten ableiten. Die Architektur bleibt somit Transaktion → Vorgang ← Beleg.
- Bei Bedarf serverseitige Validierung nur gezielt ergänzen, damit eine vorgangs_id einer Split-Zeile ausschließlich einen in transaktion_vorgaenge verknüpften Vorgang referenzieren kann; keine Strukturmigration vornehmen.
- Tests mit temporären SQLite-Testdaten und vorhandenen lokalen Dashboard-Helfern beziehungsweise Fakes ausführen.

## Manuelle Testhinweise

- Eine Transaktion mit mindestens zwei Split-Zeilen und mindestens zwei verknüpften Vorgängen öffnen, von denen einer einen Rechnungsbeleg besitzt.
- Für eine Split-Zeile den Rechnungs-Vorgang wählen, speichern und die Transaktion neu öffnen; Auswahl und Beleghinweis prüfen.
- Die Zuordnung entfernen, speichern und nach erneutem Öffnen prüfen, dass kein Vorgang ausgewählt ist.
- Eine Betragsänderung ohne Zuordnungsänderung sowie eine Zuordnungsänderung ohne Betragsänderung testen und jeweils die korrekte Split-Summe kontrollieren.

## Offene Fragen

- Keine Angaben
