# Nächstes Arbeitspaket

## Titel

Split-Editor im Dashboard für bestehende Transaktions-Splits bereitstellen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 2

## Ziel

Im Dashboard einen kleinen bearbeitbaren UI-Flow schaffen, mit dem vorhandene Split-Zeilen einer Transaktion geladen, bearbeitet, validiert und gespeichert werden können, ohne bereits die vollständige Split-Klassifikation oder Rechnungszuordnung umzusetzen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Muss umgesetzt werden

- Prüfen, ob die bereits vorhandene Split-Persistenz und Backend-Grundlage aus Teil 1 über bestehende transaction_store-Strukturen im Dashboard angesprochen werden kann.
- Einen kleinen API-Flow in server.py bereitstellen, um Splits einer Transaktion zu lesen und zu speichern.
- Im Transaktions-Detailbereich einen einfachen Split-Editor ergänzen, der mehrere Split-Zeilen mit Betrag und den bereits verfügbaren fachlichen Feldern anzeigen und bearbeiten kann.
- Clientseitig oder serverseitig sicherstellen, dass die Summe der Split-Beträge kontrolliert gegen den ursprünglichen Transaktionsbetrag geprüft wird.
- Vorhandene Vorgangs- und Transaktionsarchitektur beibehalten; keine direkte neue Grundbeziehung zwischen Belegen, Rechnungen oder anderen Entitäten einführen.
- Tests für den neuen API- und UI-nahen Flow ergänzen oder anpassen.

## Soll umgesetzt werden

- Die Bedienung so anlegen, dass spätere Vorschlagslisten und split-spezifische Statusableitungen anschlussfähig bleiben.
- Fehlermeldungen für ungültige Split-Summen oder unvollständige Eingaben klar im bestehenden UI-Stil anzeigen.
- Den Editor nur dort sichtbar machen, wo Transaktionsdetails ohnehin angezeigt werden, statt einen neuen größeren Navigationsflow einzuführen.

## Nicht Teil dieses Arbeitspakets

- Fachliche Statusableitung und vollständige Klassifikationslogik pro Split-Zeile.
- Zuordnung einer Transaktion zu mehreren Rechnungen oder Teilrechnungen.
- Neue Dokumenten- oder Mail-Zuordnungslogik.
- Grundlegender Umbau bestehender Tabellen oder Services.

## Akzeptanzkriterien

- Für eine bestehende Transaktion können vorhandene Split-Zeilen im Dashboard geladen werden.
- Der Nutzer kann Split-Zeilen im UI hinzufügen, bearbeiten und entfernen.
- Das Speichern läuft über einen bestehenden oder neu ergänzten kleinen API-Endpunkt im Dashboard-Backend.
- Ungültige Split-Summen werden verhindert oder mit klarer Fehlermeldung abgewiesen.
- Die Änderungen bleiben innerhalb der bestehenden Vorgangs-/Transaktionsarchitektur.
- Automatisierte Tests decken mindestens das Laden und Speichern des Split-Flows sowie einen Validierungsfehler ab.

## Hinweise für den Umsetzungs-Agenten

- Auf bestehende transaction_store-Datenstrukturen aufsetzen und keine parallele Split-Architektur im Dashboard erfinden.
- Falls Split-Felder für Klassifikation schon im Datenmodell existieren, im UI nur die minimal nötigen Felder freischalten; spätere Teilpakete können die fachliche Logik ergänzen.
- API möglichst eng auf Transaktionsdetails begrenzen, damit das Arbeitspaket klein bleibt.
- Keine produktiven Banking-, Mail-, Graph- oder DFBnet-Aktionen auslösen.

## Manuelle Testhinweise

- Transaktionsdetail öffnen und prüfen, ob vorhandene Split-Zeilen sichtbar sind.
- Eine Zeile hinzufügen und Beträge so setzen, dass die Summe exakt passt; Speichern und Neuladen prüfen.
- Eine absichtlich falsche Split-Summe speichern und prüfen, dass der Fehler verständlich angezeigt wird.
- Eine Zeile entfernen und erneut speichern.

## Offene Fragen

- Welche Split-Persistenz aus Teil 1 ist bereits konkret vorhanden und über welche Funktionen sollte der Dashboard-Flow idealerweise darauf zugreifen?
- Sollen im ersten UI-Schritt bereits alle Klassifikationsfelder pro Split editierbar sein oder nur Betrag plus minimale Metadaten?
- Wie soll mit negativen Beträgen bzw. Vorzeichen bei Ausgaben/Einnahmen im Editor genau umgegangen werden?
