# Nächstes Arbeitspaket

## Titel

Transaktionsdetail- und Vorgangsverknüpfungs-API auf konsistente Validierung und Fehlerantworten prüfen

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.3.2

## Ziel

Die lokalen API-Flows zum Lesen einer Transaktion und zum Verknüpfen einer Transaktion mit einem bestehenden Vorgang sollen ungültige Eingaben, fehlende Entitäten und zulässige Wiederholungen nachvollziehbar und ohne unerwünschte Persistenzänderungen behandeln.

## Relevante Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py
- tests/test_transactions.py
- transaction_store/database.py

## Wahrscheinliche Änderungsstellen

- DashboardDataStore.transaction_detail
- DashboardDataStore.link_transaction_vorgang
- DashboardRequestHandler._transaction_detail_response
- DashboardRequestHandler.do_POST für /api/transactions/<id>/vorgaenge
- bestehende Dashboard-API-Regressionstests

## Muss umgesetzt werden

- Die Fehlerpfade von GET /api/transactions/<transaktions_id> und POST /api/transactions/<transaktions_id>/vorgaenge gegen die bestehende API-Konvention prüfen.
- Für fehlende oder ungültige Transaktions- und Vorgangs-IDs, unbekannte Transaktionen, unbekannte Vorgänge und ungültige JSON-Payloads eindeutige 400- oder 404-Antworten sicherstellen.
- Sicherstellen, dass abgelehnte Verknüpfungsanfragen keine neue N:M-Zuordnung oder sonstige Persistenzänderung erzeugen.
- Das bestehende idempotente Verhalten einer bereits vorhandenen Transaktion-Vorgang-Verknüpfung erhalten und mit einem Regressionstest absichern.
- Regressionstests mit einer lokalen temporären SQLite-Testdatenbank ergänzen oder präzisieren; keine produktiven Daten, Browser oder externen Dienste verwenden.

## Soll umgesetzt werden

- Fehlermeldungen auf die bereits verwendete deutsche, fachlich verständliche Terminologie abstimmen.
- Bestehende Tests für HTTP-Statuscodes und JSON-Fehlerobjekte wiederverwenden, statt eine parallele Testinfrastruktur einzuführen.

## Nicht Teil dieses Arbeitspakets

- Änderungen am Datenmodell oder an den bestehenden Tabellen transaktion_vorgaenge und vorgaenge.
- Split-Persistenz, Split-Editor oder Split-Klassifikation.
- Überarbeitung anderer Vorgangs-, Beleg-, To-Do- oder Terminendpunkte.
- Neue direkte Beziehungen zwischen Transaktionen und Belegen.
- Externe Banking-, Mail-, Microsoft-Graph- oder DFBnet-Aktionen.

## Akzeptanzkriterien

- Eine nicht vorhandene Transaktion liefert beim Detailabruf eine JSON-Fehlerantwort mit HTTP 404.
- Ein leerer oder nicht sinnvoll auflösbarer Transaktionspfad wird nicht als erfolgreiche Detailantwort behandelt und folgt der bestehenden 400/404-Konvention.
- Eine Verknüpfungsanfrage akzeptiert ausschließlich das erwartete Feld vorgangs_id mit einem nichtleeren Wert.
- Unbekannte Transaktions- oder Vorgangs-IDs beim Verknüpfen liefern HTTP 404; ungültige Payloads liefern HTTP 400.
- Nach jeder abgelehnten Verknüpfungsanfrage enthält transaktion_vorgaenge unverändert keine neue Zuordnung.
- Das wiederholte Verknüpfen derselben gültigen Transaktion mit demselben Vorgang erzeugt weiterhin höchstens einen Zuordnungseintrag und liefert eine erfolgreiche, nachvollziehbare Antwort.
- Die ergänzten Regressionstests laufen zusammen mit den bestehenden Tests ohne Netzwerk-, Browser- oder Secret-Zugriff.

## Hinweise für den Umsetzungs-Agenten

- Die bestehende Vorgangsarchitektur beibehalten: Verknüpfungen ausschließlich über transaktion_vorgaenge erzeugen oder prüfen.
- Vorhandene ValueError- und LookupError-Behandlung des Request-Handlers nutzen und nur dort präzisieren, wo Statuscode oder Fehlertext inkonsistent sind.
- Keine generische Umgestaltung der API-Fehlerbehandlung vornehmen; auf die beiden genannten Endpunkt-Flows begrenzen.
- Die Datenintegrität über die vorhandenen Fremdschlüssel und INSERT OR IGNORE-Semantik erhalten.

## Manuelle Testhinweise

- Mit einer temporären lokalen Testdatenbank einen gültigen Transaktionsdetailabruf, einen 404-Abruf und einen gültigen Verknüpfungsabruf prüfen.
- POST-Anfragen mit leerem Objekt, zusätzlichem Feld, leerer vorgangs_id sowie unbekannter Vorgangs-ID lokal ausführen und Statuscode sowie JSON-Fehler kontrollieren.
- Eine gültige Verknüpfung zweimal absenden und anschließend prüfen, dass sie nur einmal in der Vorgangsdetailansicht beziehungsweise der Zuordnungstabelle erscheint.

## Offene Fragen

- Keine Angaben
