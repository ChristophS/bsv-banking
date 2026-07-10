# Nächstes Arbeitspaket

## Titel

Split-Editor im Dashboard für einfache Teilbetragsaufteilung ergänzen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 2

## Ziel

Für bestehende Transaktionen einen kleinen nutzbaren UI-Flow bereitstellen, mit dem Split-Zeilen angelegt, bearbeitet und gespeichert werden können, basierend auf der bereits vorhandenen Split-Backend-Grundlage.

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

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Muss umgesetzt werden

- Vorhandene Split-Daten pro Transaktion im Dashboard abrufbar machen oder vorhandenen API-Zugriff dafür anbinden.
- In der Transaktions-Detailansicht einen einfachen Split-Bereich ergänzen.
- Erlauben, Split-Zeilen mit Betrag und den für den einfachen Flow notwendigen Feldern anzulegen, zu bearbeiten und zu entfernen.
- Speichern an die bestehende Split-Persistenz anbinden, ohne neue fachliche Grundarchitektur einzuführen.
- Im UI sichtbar machen, ob die Summe der Split-Beträge zur Transaktionssumme passt.
- Tests für den Dashboard-Flow und die API-/Server-Anbindung ergänzen.

## Soll umgesetzt werden

- Einfache clientseitige Validierung für leere oder offensichtlich ungültige Beträge ergänzen.
- Eine kompakte Summenanzeige mit Restdifferenz oder vollständiger Übereinstimmung ergänzen.
- Bestehende Detailansicht so erweitern, dass der Split-Bereich den restlichen Bearbeitungsflow nicht stört.

## Nicht Teil dieses Arbeitspakets

- Fachliche Klassifikation einzelner Splits und Ableitung des Vorgangsstatus aus Splits.
- Zuordnung von Splits zu mehreren Rechnungen oder Teilrechnungen.
- Komplexe Folgeflows für Vorgänge, Belege oder Rechnungslogik.
- Allgemeine Mail-, Dokumenten- oder DFBnet-Funktionen.
- Grundlegender Umbau bestehender Transaktions-, Vorgangs- oder Belegarchitektur.

## Akzeptanzkriterien

- In der Transaktions-Detailansicht kann für eine bestehende Transaktion ein Split-Bereich geöffnet oder angezeigt werden.
- Benutzer können mehrere Split-Zeilen anlegen, ändern und löschen.
- Die Split-Zeilen werden über bestehende Backend-Strukturen gespeichert und nach erneutem Laden wieder angezeigt.
- Die Oberfläche zeigt an, ob die Summe der Split-Beträge der Transaktionssumme entspricht oder eine Differenz besteht.
- Der Flow bleibt auf einen einfachen Editor beschränkt und enthält keine Rechnungs- oder Statuslogik späterer Teilpakete.
- Automatisierte Tests decken den neuen Dashboard-Flow ohne externe Dienste ab.

## Hinweise für den Umsetzungs-Agenten

- Bestehende Vorgangsarchitektur nicht umgehen; dieses Paket fokussiert nur auf Split-Erfassung an der Transaktion.
- Keine direkte neue fachliche Beziehung zwischen Belegen und Transaktionen einführen.
- Falls Split-API im Server bereits teilweise vorhanden ist, diese präzise für den UI-Flow nutzen statt parallel neue Endpunkte zu erfinden.
- Beträge konsistent zu vorhandenen Datenformaten und Rundungsregeln behandeln.
- Tests nur mit lokalen Testdaten, Fixtures oder Mocks umsetzen.

## Manuelle Testhinweise

- Dashboard starten und eine Transaktion öffnen.
- Zwei oder mehr Split-Zeilen mit Teilbeträgen erfassen und speichern.
- Prüfen, dass die Summenanzeige bei passender Summe Erfolg und bei absichtlicher Abweichung eine Differenz zeigt.
- Seite neu laden und prüfen, dass die gespeicherten Split-Zeilen erhalten bleiben.
- Einen Split löschen und prüfen, dass die Änderung korrekt gespeichert wird.

## Offene Fragen

- Welche konkreten Felder sind in der bereits vorhandenen Split-Backend-Grundlage neben dem Betrag schon stabil vorgesehen?
- Soll der einfache UI-Flow bereits Vorschlagslisten für Kategorien anzeigen oder erst im Folgepaket zur Split-Klassifikation?
- Soll das Speichern bei Summendifferenz blockiert werden oder darf zunächst ein unvollständiger Split-Zustand gespeichert werden?
