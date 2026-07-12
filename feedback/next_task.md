# Nächstes Arbeitspaket

## Titel

Klassifikations-API für einzelne Transaktionen auf konsistente Fehlerantworten absichern

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.2

## Ziel

Der PATCH-Flow zur manuellen Klassifikation einer einzelnen Transaktion soll ungültige Eingaben, unbekannte Transaktionen und erfolgreiche Aktualisierungen mit konsistenten HTTP-Statuscodes und nachvollziehbaren JSON-Fehlern behandeln.

## Relevante Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- DashboardDataStore.update_transaction_classification in banking_dashboard/server.py
- DashboardRequestHandler._classification_update_response und do_PATCH in banking_dashboard/server.py
- bestehende Dashboard-API-Tests in tests/test_dashboard.py

## Muss umgesetzt werden

- Den bestehenden PATCH-Endpunkt /api/transactions/<transaktions_id>/classification für den isolierten Klassifikationsflow prüfen und nur konkret belegte Inkonsistenzen beheben.
- Sicherstellen, dass ein leerer Request, unbekannte Klassifikationsfelder, nicht-textuelle Werte, zu lange Werte und eine unbekannte Transaktions-ID kontrolliert behandelt werden.
- Für Validierungsfehler HTTP 400, für nicht gefundene Transaktionen HTTP 404 und für erfolgreiche Aktualisierungen HTTP 200 mit dem aktualisierten Transaktionsdatensatz beibehalten beziehungsweise eindeutig absichern.
- Automatisierte Tests für mindestens einen Erfolgsfall sowie die genannten Fehlerklassen ergänzen oder präzisieren.
- Keine echten externen Dienste, Datenbanken aus produktiven Laufzeitdaten oder Zugangsdaten verwenden; Tests müssen mit temporären Testdaten und lokalen Fixtures arbeiten.

## Soll umgesetzt werden

- Fehlermeldungen auf verständliche, feldbezogene und keine internen Implementierungsdetails preisgebende Texte prüfen.
- Sicherstellen, dass ein abgewiesener Request keine Teiländerung an Klassifikationsfeldern oder Vorgangsstatus hinterlässt.

## Nicht Teil dieses Arbeitspakets

- Änderungen am Split-Editor, an Split-Persistenz oder an der Split-API.
- Validierungsarbeiten für Vorgänge, Belege, To-Dos oder Termine.
- Umbau des Datenbankschemas, der Vorgangsarchitektur oder bestehender N:M-Verknüpfungen.
- UI-Änderungen in app.js, index.html oder styles.css.
- Banking-, Microsoft-Graph- oder DFBnet-Aufrufe.

## Akzeptanzkriterien

- PATCH /api/transactions/<id>/classification aktualisiert zulässige Klassifikationsfelder und antwortet mit HTTP 200 sowie der aktualisierten Transaktion.
- Ein leerer oder fachlich ungültiger Klassifikationspayload antwortet mit HTTP 400 und einem JSON-Objekt mit error.
- Unbekannte oder nicht erlaubte Klassifikationsfelder werden nicht stillschweigend ignoriert und führen zu HTTP 400.
- Eine nicht existierende Transaktions-ID führt zu HTTP 404 und einem JSON-Objekt mit error.
- Bei abgewiesenen Requests bleiben die zuvor gespeicherten Klassifikationswerte unverändert.
- Die neuen oder angepassten Tests laufen ohne Browserstart, Netzwerkzugriff, Secrets oder produktive Daten.

## Hinweise für den Umsetzungs-Agenten

- Die bestehende Zuordnung von API-Feldnamen über CLASSIFICATION_FIELDS und die vorhandene DashboardDataStore-Methode weiterverwenden.
- Die vorhandene Fehlerübersetzung im Request-Handler nutzen; keine parallele Fehlerarchitektur einführen.
- Klassifikationsänderungen müssen weiterhin die bestehende Abschlussregelverarbeitung für verknüpfte Vorgänge auslösen.

## Manuelle Testhinweise

- Mit einer temporären Testdatenbank einen gültigen PATCH-Request für eine vorhandene Transaktion ausführen und Antwort sowie gespeicherte Werte prüfen.
- Je einen PATCH mit leerem Objekt, unbekanntem Feld, nicht-textuellem Wert und unbekannter Transaktions-ID ausführen.
- Nach jedem abgewiesenen Request den Transaktionsdetail-Endpunkt abfragen und unveränderte Klassifikationswerte kontrollieren.

## Offene Fragen

- Keine Angaben
