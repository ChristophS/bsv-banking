# Nächstes Arbeitspaket

## Titel

Split-Editor in der Transaktionsdetailansicht des Dashboards umsetzen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 2

## Ziel

Eine bestehende Transaktion im Dashboard interaktiv in mehrere Split-Zeilen aufteilen können, sodass Teilbeträge angelegt, bearbeitet und gelöscht werden können und die Summe der Splits nachvollziehbar zur Originaltransaktion passt.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- transaction_store/database.py
- transaction_store/models.py
- tests/test_dashboard.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: bestehende Transaktions-Detail-API und mögliche Split-Endpunkte für Dashboard-Nutzung
- banking_dashboard/static/app.js: Detailansicht, Split-Editor-Interaktionen, Laden/Speichern/Löschen von Split-Zeilen
- banking_dashboard/static/index.html: Markup für Split-Bereich in der Transaktionsdetailansicht
- banking_dashboard/static/styles.css: einfache Darstellung des Split-Editors
- transaction_store/database.py: Nutzung der vorhandenen Split-Persistenz aus der UI-Schicht
- transaction_store/models.py: Serialisierung vorhandener Split-Daten für API-Antworten
- tests/test_dashboard.py: API- und UI-nahe Server-Tests für Split-Editor-Flow
- tests/test_transactions.py: Absicherung der erwarteten Split-Datenform für Dashboard-Antworten

## Muss umgesetzt werden

- Prüfen und nutzen, wie die vorhandene Split-Persistenz und Split-API aus Teil 1 bereits modelliert sind, statt neue Parallelstrukturen einzuführen.
- In der Transaktionsdetailansicht einen klar abgegrenzten Split-Bereich ergänzen, der vorhandene Split-Zeilen anzeigt.
- Anlegen neuer Split-Zeilen über die bestehende Architektur ermöglichen.
- Bearbeiten und Löschen einzelner Split-Zeilen im Dashboard ermöglichen.
- Die Summenlogik in der UI sichtbar machen, insbesondere Originalbetrag, Summe der Split-Zeilen und eine eventuelle Differenz.
- Fehlerfälle vom Backend verständlich anzeigen, z. B. wenn ungültige Beträge oder inkonsistente Summen gespeichert werden sollen.
- Tests für die Dashboard-API bzw. den Server ergänzen, ohne echte externe Dienste zu verwenden.

## Soll umgesetzt werden

- Eine kleine Guardrail in der UI ergänzen, damit unvollständige neue Split-Zeilen nicht versehentlich gespeichert werden.
- Die Split-Bedienung so gestalten, dass spätere Klassifikationsfelder pro Split ergänzt werden können, ohne das UI neu zu strukturieren.
- Bestehende Transaktionsdetails nach dem Speichern von Splits direkt aktualisieren.

## Nicht Teil dieses Arbeitspakets

- Fachliche Klassifikation einzelner Split-Zeilen
- Vorschlagslisten oder Datalists für Split-Klassifikationsfelder
- Statusableitung aus Split-Klassifikationen
- Zuordnung zu mehreren Rechnungen oder Teilrechnungen
- Neue fachliche Grundarchitektur außerhalb der vorhandenen Vorgangs-, Beleg-, Transaktions- und Verknüpfungsstrukturen
- Breiter Umbau der bestehenden Transaktionsdetailansicht jenseits des Split-Bereichs

## Akzeptanzkriterien

- In der Transaktionsdetailansicht werden vorhandene Split-Zeilen einer Transaktion geladen und sichtbar dargestellt.
- Benutzer können im Dashboard mindestens eine neue Split-Zeile anlegen, eine bestehende ändern und eine bestehende löschen.
- Die UI zeigt den Originalbetrag der Transaktion sowie die aktuelle Summe der Split-Zeilen und eine Differenz nachvollziehbar an.
- Speicheraktionen verwenden die bestehende Split-Backend-Struktur statt neuer paralleler Speicherung.
- Bei ungültigen Eingaben oder Backend-Validierungsfehlern bleibt die Anwendung bedienbar und zeigt eine verständliche Fehlermeldung an.
- Automatisierte Tests decken den Server-Flow für Laden und Ändern von Split-Daten ab.

## Hinweise für den Umsetzungs-Agenten

- Vorgänge bleiben zentrales fachliches Objekt; keine direkte neue Beleg-zu-Transaktion-Architektur einführen.
- Falls Teil 1 bereits Endpunkte oder Datenbanktabellen für Splits bereitstellt, diese nur für das Dashboard anschließen.
- Falls die bestehende Detail-API bereits Transaktionsdaten serialisiert, Split-Daten dort mit ausgeben statt einen unnötig separaten Ladepfad zu erfinden.
- UI bewusst klein halten: tabellarische Split-Zeilen mit Betrag und minimalen Feldern reichen für diesen Schritt.
- Keine spätere Split-Klassifikationslogik vorwegnehmen; dafür nur anschlussfähige Struktur lassen.

## Manuelle Testhinweise

- Dashboard lokal öffnen und eine Transaktion mit bekannter Split-Unterstützung in der Detailansicht öffnen.
- Eine neue Split-Zeile anlegen und prüfen, dass sie nach dem Speichern erneut geladen wird.
- Eine vorhandene Split-Zeile bearbeiten und prüfen, dass Summenanzeige und Persistenz aktualisiert werden.
- Eine Split-Zeile löschen und prüfen, dass die Rest-Summe korrekt dargestellt wird.
- Einen ungültigen Zustand provozieren, z. B. fehlerhafte Betragseingabe oder Summendifferenz, und prüfen, dass eine verständliche Fehlermeldung erscheint.

## Offene Fragen

- Welche konkreten Felder wurden in Teil 1 pro Split-Zeile bereits festgelegt und müssen im UI jetzt sichtbar sein?
- Soll das Speichern pro Zeile sofort erfolgen oder gesammelt für alle Split-Zeilen einer Transaktion?
- Welche Validierung übernimmt bereits das Backend und welche minimale Vorvalidierung soll zusätzlich im Frontend erfolgen?
