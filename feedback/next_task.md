# Nächstes Arbeitspaket

## Titel

Vorgangs- und Belegzuordnungen im bestehenden Mail-Kontext präzisieren

## Ziel

Die bestehende Vorgang-zentrierte Verknüpfung für Mails, Transaktionen und Belege so konkret beschreiben, dass daraus ein kleines, direkt umsetzbares Folgepaket abgeleitet werden kann. Dabei soll klar werden, wie eine Mail mit mehreren Anhängen in einem gemeinsamen Vorgang bleibt und welche bestehenden Stellen im Repo dafür als Einstieg dienen, ohne neue Architektur einzuführen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- transaction_store/database.py
- tests/test_dashboard.py
- tests/test_transactions.py
- feedback/backlog.md

## Wahrscheinliche Änderungsstellen

- feedback/next_task.md: Präzisierung des Folgebriefings für die spätere Umsetzung.
- feedback/backlog.md: Bestehenden Mehrfachzuordnungs-Punkt in kleinere Folgepakete aufteilen.
- banking_dashboard/server.py: Bestehende API-Endpunkte rund um Vorgänge, Mails und Belege als Referenz für den kleinsten nächsten Schritt.
- banking_dashboard/static/app.js: Vorhandene UI-Flows in Mail- und Vorgangskontext als Referenz für die spätere Umsetzung.
- transaction_store/database.py: Bestehende Tabellen und Zuordnungslogik als fachliche Leitplanke.

## Muss umgesetzt werden

- Den vorhandenen Backlog-Punkt zur Zuordnung mehrerer Dokumente aus einer Mail auf unterschiedliche Transaktionen innerhalb eines Vorgangs repo-konret analysieren.
- Explizit festhalten, dass die bestehende Vorgangszentrierung über `inbox_vorgaenge`, `transaktion_vorgaenge` und `vorgang_belege` beibehalten wird.
- Ein kleines erstes Folgepaket formulieren, das nur die kleinste sinnvolle Verbesserung im Mail-/Vorgangskontext vorbereitet, statt die komplette Mehrfachzuordnungslogik zu verlangen.
- Die betroffenen bestehenden Endpunkte, Tabellen und UI-Bereiche namentlich benennen, ohne neue Datenmodelle zu erfinden.
- Alle größeren Teilaspekte wie automatische Aufteilung, Massenzuordnung oder komplexe UX im Backlog belassen.

## Soll umgesetzt werden

- Kurz dokumentieren, dass der Kernfall eine Mail mit mehreren Anhängen in einem gemeinsamen Vorgang ist.
- Falls aus dem Repo eindeutig ableitbar, die kleinste fehlende API- oder UI-Aktion benennen, die später zuerst ergänzt werden sollte.
- Die Begriffsnutzung Vorgang, Mail, Beleg und Transaktion konsistent an die bestehende Codebasis anlehnen.

## Nicht Teil dieses Arbeitspakets

- Implementierung einer neuen Dokument- oder Mail-Import-Engine
- Automatische Aufteilung von Mailanhängen per KI oder OCR
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Integration
- Neue direkte Verknüpfung zwischen Transaktion und Beleg als Ausgangslösung
- Komplette UX-Lösung für alle Mehrfachzuordnungsfälle

## Akzeptanzkriterien

- Es liegt genau ein kleines, zusammenhängendes Folgepaket vor.
- Das Folgepaket basiert auf den bestehenden Repo-Dateien, Tabellen und UI-Flows.
- Die bestehende Vorgang-zentrierte Verknüpfungslogik bleibt unangetastet.
- Alle nicht behandelten Punkte sind nachvollziehbar im Backlog abgebildet.
- Es wird keine neue Architektur oder Direktverknüpfung zwischen Transaktion und Beleg eingeführt.

## Hinweise für den Umsetzungs-Agenten

- Die fachliche Kette bleibt: Mail zu Vorgang über `inbox_vorgaenge`, Transaktion zu Vorgang über `transaktion_vorgaenge`, Beleg zu Vorgang über `vorgang_belege`.
- Die bereits geladenen Dateien `server.py` und `app.js` sollten als Referenz dienen, um vorhandene Einstiegsstellen konkret zu benennen.
- Da direkte Beleg-Transaktions-Beziehungen laut Dokumentation nicht existieren, sollte das nächste Paket auf Sichtbarkeit und Eingrenzung im gemeinsamen Vorgang zielen.
- Die Ausgabe soll als präzisiertes Folgebriefing lesbar sein, nicht als Umsetzung eines großen Gesamtfeatures.

## Manuelle Testhinweise

- Prüfen, ob das Folgebriefing ohne erneute fachliche Interpretation verständlich ist.
- Kontrollieren, dass keine Forderung nach einer neuen Direktverknüpfung zwischen Beleg und Transaktion enthalten ist.
- Sicherstellen, dass Vorgang, Mail, Beleg und Transaktion entlang der bestehenden Tabellen konsistent verwendet werden.

## Offene Fragen

- Soll der erste echte Umsetzungs-Schritt primär in der Mailansicht oder in den Vorgangsdetails ansetzen?
- Reicht die bestehende Vorgang-zentrierte Belegzuordnung für den Kernfall vollständig aus?
- Wie soll später im UI sichtbar werden, welches Dokument fachlich zu welcher Transaktion gehört, wenn die Datenbank dies nur indirekt über den Vorgang ausdrückt?
