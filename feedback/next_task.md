# Nächstes Arbeitspaket

## Titel

Vorhandene Transaktions-Splits im Dashboard sichtbar und bearbeitbar machen

## Ziel

Die bereits vorhandene Split-Backend-Logik so in die bestehende Transaktionsdetailansicht integrieren, dass vorhandene Splits angezeigt, angepasst und über den bestehenden Split-Endpunkt gespeichert werden können.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Laden, Rendern, Bearbeiten und Speichern der Split-Zeilen in der Transaktionsdetailansicht.
- banking_dashboard/static/index.html: kleiner UI-Container für Split-Anzeige und -Bearbeitung in der bestehenden Detailansicht.
- tests/test_dashboard.py: Tests für Split-API, Persistenz und Fehlerfälle.
- banking_dashboard/server.py: nur bei Bedarf für kleine Anpassungen an Validierung oder Response-Handling.

## Muss umgesetzt werden

- In der Transaktionsdetailansicht vorhandene Splits inklusive Betrag und relevanter Klassifikationsfelder anzeigen.
- Bestehende Splits bearbeitbar machen und neue Split-Zeilen hinzufügen bzw. entfernen können.
- Beim Speichern den vorhandenen Endpunkt `PUT /api/transactions/<id>/splits` verwenden.
- Nach erfolgreichem Speichern die Detailansicht mit den vom Backend zurückgegebenen Daten aktualisieren.
- Backend-Validierungsfehler im UI sichtbar anzeigen.
- Beträge in Cent verarbeiten und keine ungenaue Float-Logik für Split-Beträge einführen.

## Soll umgesetzt werden

- Eine einfache Plausibilitätsprüfung ergänzen, dass einzelne Split-Zeilen nicht ohne Betrag gespeichert werden.
- Optional eine kurze Summenanzeige ergänzen, falls sie sich sauber in die bestehende Ansicht einfügt.
- Neue Split-Zeilen mit leeren Klassifikationsfeldern vorbefüllen.

## Nicht Teil dieses Arbeitspakets

- Kompletter fachlicher Workflow 'eine Transaktion -> mehrere Rechnungen'.
- Dokumenten- oder Rechnungszuordnung pro Split.
- Automatische Erzeugung oder Aufspaltung von Vorgängen aus Splits.
- Neue Datenbanktabellen für Rechnungspositionen oder Belegpositionen.
- Mail-Workflow mit mehreren Dokumenten auf verschiedene Transaktionen.
- Spendenbescheinigungen oder DFBnet-Integration.

## Akzeptanzkriterien

- Beim Öffnen einer Transaktion mit vorhandenen Splits werden diese im Dashboard sichtbar angezeigt.
- Der Nutzer kann mindestens Split-Betrag, Beschreibung und Klassifikationsfelder eines Splits ändern und speichern.
- Der Nutzer kann mindestens einen neuen Split hinzufügen und einen bestehenden Split entfernen; das Backend speichert den ersetzten Split-Satz über den vorhandenen Endpunkt.
- Nach erfolgreichem Speichern zeigt ein erneutes Laden der Transaktionsdetails dieselben Split-Daten an.
- Ungültige Eingaben, insbesondere fehlender oder ungültiger Cent-Betrag, führen zu einer sichtbaren Fehlermeldung im Dashboard.
- Vorhandene Transaktionsklassifikation außerhalb der Split-Funktion bleibt unverändert bedienbar.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandene API-Funktionalität `transaction_splits(...)` und `replace_transaction_splits(...)` in `DashboardDataStore` soll als Grundlage genutzt werden.
- Der Detailpayload liefert Splits bereits unter `detail["splits"]`; diese Quelle sollte für das UI verwendet werden.
- Die bestehende Detail- und Autosave-Mechanik in `app.js` ist als Muster für den Split-Editor zu nutzen.
- Die API liefert deutsche und englische Feldnamen; im UI sollte eine konsistente interne Feldverwendung gewählt werden.
- Da `replace_transaction_splits(...)` den kompletten Satz ersetzt, muss die UI beim Speichern den vollständigen aktuellen Split-Stand senden.
- Falls sinnvoll, sollte nach erfolgreichem Save der zurückgegebene `transaction`-Payload als neue Quelle der Detailansicht verwendet werden.

## Manuelle Testhinweise

- Transaktion ohne Splits öffnen: leerer, aber bedienbarer Split-Bereich.
- Neuen Split mit gültigem Cent-Betrag anlegen, speichern und die Detailansicht neu laden.
- Einen vorhandenen Split bearbeiten und einen löschen, danach neu laden.
- Ungültigen Betrag absenden und prüfen, dass eine verständliche Fehlermeldung erscheint.
- Prüfen, dass die normale Klassifikationsbearbeitung der Transaktion nach Split-Änderungen weiterhin funktioniert.

## Offene Fragen

- Soll `vorgangs_id` pro Split in diesem Paket bereits aktiv in der UI bearbeitbar sein, oder reicht vorerst Anzeige und Erhalt vorhandener Werte?
- Soll die UI das Summengleichgewicht zur Originaltransaktion nur anzeigen oder bereits vor dem Speichern strikt erzwingen?
