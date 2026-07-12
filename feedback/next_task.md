# Nächstes Arbeitspaket

## Titel

Split-API für Transaktionen auf konsistente Validierung und Fehlerantworten absichern

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 1

## Ziel

Der lokale GET-/PUT-Flow für Transaktions-Splits soll ungültige oder widersprüchliche Eingaben nachvollziehbar ablehnen, gültige Splits atomar speichern und konsistente HTTP-Fehlerantworten liefern.

## Relevante Dateien

- banking_dashboard/server.py
- transaction_store/database.py
- tests/test_dashboard.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- DashboardDataStore.transaction_splits
- DashboardDataStore.replace_transaction_splits
- DashboardRequestHandler.do_GET für /api/transactions/<id>/splits
- DashboardRequestHandler.do_PUT für /api/transactions/<id>/splits
- _transaction_splits_from_payload
- transaction_store.database.replace_transaction_splits
- Tests für Split-API und Split-Persistenz

## Muss umgesetzt werden

- Den GET- und PUT-Flow für /api/transactions/<transaktions_id>/splits gegen die vorhandene Split-Persistenz prüfen.
- Validierung für fehlende Transaktions-IDs, unbekannte Transaktionen, ungültige JSON-Payloads, unbekannte Split-Felder, widersprüchliche Transaktions-IDs und nicht ganzzahlige Cent-Beträge nachvollziehbar absichern oder korrigieren.
- Sicherstellen, dass fachlich ungültige Split-Summen oder ungültige Vorgangsreferenzen über die bestehende Persistenzlogik abgelehnt werden und dabei keine Teiländerung gespeichert bleibt.
- Für erwartete Fehlerfälle konsistente 400- beziehungsweise 404-Antworten mit verständlicher Fehlernachricht sicherstellen.
- Automatisierte Tests für mindestens einen erfolgreichen Speichervorgang sowie die relevanten Validierungs- und Atomizitätsfehler ergänzen oder präzisieren.

## Soll umgesetzt werden

- Prüfen, ob GET- und PUT-Antworten für Split-Beträge, Reihenfolge, Klassifikationsstatus und zulässige Vorgänge dieselben etablierten Feldnamen verwenden.
- Vorhandene Tests und Hilfsfunktionen wiederverwenden; keine produktiven Datenbankdateien oder externe Dienste verwenden.

## Nicht Teil dieses Arbeitspakets

- Split-Editor oder sonstige Dashboard-UI ändern.
- Klassifikations- oder Abschlusslogik für Splits fachlich erweitern.
- Neue Zuordnungsmodelle zwischen Transaktionen, Belegen und Vorgängen einführen.
- Transaktionsdetail- oder Vorgangsverknüpfungsendpunkte außerhalb des Split-Flows prüfen.
- Banking-, Mail-, Microsoft-Graph- oder DFBnet-Zugriffe ausführen oder verändern.

## Akzeptanzkriterien

- GET /api/transactions/<id>/splits liefert für eine vorhandene Transaktion den bestehenden Split-Zustand; eine unbekannte oder leere ID führt zu einer nachvollziehbaren Fehlerantwort.
- PUT /api/transactions/<id>/splits akzeptiert ausschließlich das etablierte splits-Payload-Format und weist ungültige Feldnamen, Typen und widersprüchliche IDs mit HTTP 400 zurück.
- Eine unbekannte Transaktion führt beim Split-Lesen oder -Speichern zu HTTP 404.
- Bei abgelehnter Split-Summe, ungültiger Vorgangsreferenz oder anderem Persistenzfehler bleiben zuvor gespeicherte Splits unverändert.
- Die Testausführung erfolgt ausschließlich mit temporären SQLite-Testdaten und ohne Browser, Netzwerkanfrage oder externe Credentials.
- Die bestehenden Vorgangs- und N:M-Verknüpfungsstrukturen bleiben unverändert.

## Hinweise für den Umsetzungs-Agenten

- Bestehende Funktionen list_transaction_splits und replace_transaction_splits aus transaction_store.database verwenden; keine parallele Split-Speicherung einführen.
- Fehler fachlicher Eingaben als ValueError und fehlende Entitäten als LookupError bis zum vorhandenen HTTP-Fehlermapping führen, sofern dies dem bestehenden Stil entspricht.
- Transaktionen für schreibende Split-Operationen über die vorhandene Datenbankfunktion atomar behandeln und nicht im Request-Handler selbst nachbauen.
- Tests sollen konkrete JSON-Antworten, Statuscodes und den unveränderten Zustand nach einem abgewiesenen PUT prüfen.

## Manuelle Testhinweise

- Mit einer ausschließlich lokal erzeugten Testdatenbank einen vorhandenen Transaktionsdatensatz per GET abfragen.
- Einen gültigen Split-Satz speichern und anschließend per GET verifizieren.
- Je einen PUT mit falscher Transaktions-ID im Split, unbekanntem Feld, nichtnumerischem Cent-Betrag und nicht passender Split-Summe ausführen; danach jeweils den zuvor gespeicherten Satz erneut abfragen.

## Offene Fragen

- Keine Angaben
