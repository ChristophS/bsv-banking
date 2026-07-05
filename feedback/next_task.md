# Nächstes Arbeitspaket

## Titel

Inline-Klassifikation verknüpfter Transaktionen im Mail-Vorgang-Import ermöglichen

## Ziel

Beim Mail-Import eines Vorgangs sollen bereits verknüpfte bestehende Transaktionen im selben Schritt mit ihren Klassifikationsfeldern bearbeitet werden können, sodass ein fachlich vollständiger Vorgang direkt abgeschlossen werden kann, wenn die bestehenden Regeln danach erfüllt sind.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: Erweiterung von `_mail_vorgang_import(...)` bzw. des Endpoints `/api/mail/<id>/vorgang-import`, um optionale Klassifikationswerte pro verknüpfter Transaktion anzunehmen und vor `requested_completed` auf bestehende Transaktionen anzuwenden.
- banking_dashboard/static/app.js: Mail-Import-Flow erweitern, damit für verknüpfte bestehende Transaktionen die Klassifikationsfelder editierbar sind und im Importpayload mitgesendet werden.
- banking_dashboard/static/index.html: Kleine Ergänzung am bestehenden Mail-Import-Dialog/Formular für die Felder je verknüpfter Transaktion, falls dafür Markup fehlt.
- tests/test_dashboard.py: Tests für Import mit Transaktionsklassifikation, erfolgreichen Direktabschluss und Ablehnung bei unvollständiger Klassifikation ergänzen.
- transaction_store/database.py: Nur falls nötig die bestehende Store-Methode für Klassifikationsupdates in den Import-Flow sauber wiederverwenden statt Logik zu duplizieren.
- transaction_store/models.py: Nur falls Feld-/Modellnamen für den Payload oder die Validierung abgeglichen werden müssen.

## Muss umgesetzt werden

- Im Importpayload eine optionale Struktur für Klassifikationsänderungen verknüpfter Transaktionen unterstützen, begrenzt auf die vorhandenen Felder `transaktionstyp`, `oberkategorie`, `unterkategorie`, `sphaere`, `fachliche_beschreibung`.
- Die Änderungen nur auf bereits verknüpfte/existierende Transaktionen anwenden; keine neue Transaktionserstellung einbauen.
- Die Transaktionsklassifikation vor der Auswertung von `requested_completed` und vor `update_vorgang_status(..., True)` anwenden.
- Dabei dieselbe Validierung und Feldlogik wie bei `update_transaction_classification(...)` nutzen, damit Pflichtfelder, Längen und Typen konsistent bleiben.
- Den bestehenden Mail-Import-Flow so erweitern, dass ein direkt abgeschlossener Import funktioniert, wenn die im selben Import klassifizierten Transaktionen danach die Abschlussregeln erfüllen.

## Soll umgesetzt werden

- Im API-Response die aktualisierte Vorgangsdetailansicht zurückgeben, damit das Frontend keinen Sonderfallzustand behandeln muss.
- Bei ungültigen Klassifikationsdaten oder unbekannten Transaktions-IDs eine klare 4xx-Fehlermeldung liefern.
- Im UI deutlich machen, dass nur bereits verknüpfte Transaktionen bearbeitet werden können.

## Nicht Teil dieses Arbeitspakets

- Inline-Klassifikation im allgemeinen manuellen Vorgangserstell-Flow außerhalb des Mail-Imports.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spendenbescheinigungs-/Adressdatenbank-Integration.
- Breite Dashboard-Usability-Überarbeitung.
- Neue Regeltypen oder Änderungen an der Kernlogik der Abschlussregeln.

## Akzeptanzkriterien

- Wenn im Mail-Import eine bestehende verknüpfte Transaktion zuvor unvollständig war, kann der Nutzer im selben Flow ihre Pflichtfelder ausfüllen und den Vorgang direkt abgeschlossen importieren, sofern die bestehenden Abschlussregeln erfüllt sind.
- Werden keine Klassifikationsdaten mitgesendet, bleibt das bisherige Verhalten des Mail-Import-Endpunkts unverändert.
- Ungültige Klassifikationsfelder oder unbekannte Transaktions-IDs im Importpayload führen zu einer klaren 4xx-Fehlermeldung; es gibt kein stilles Wegwerfen der Daten.
- Der Vorgang wird nicht abgeschlossen, wenn trotz Inline-Klassifikation weiterhin Pflichtfelder fehlen oder andere Abschlussbedingungen verletzt sind.
- Tests decken mindestens den Erfolgsfall und einen Ablehnungsfall des Direktabschlusses nach Mail-Import ab.

## Hinweise für den Umsetzungs-Agenten

- `server.py` ist die natürliche Änderungsstelle, weil dort bereits `links.transaction_ids` gelesen, der Vorgang angelegt/verknüpft und anschließend der Direktabschluss versucht wird.
- Die Reihenfolge ist fachlich wichtig: Vorgang anlegen/verknüpfen, Transaktionsklassifikation anwenden, dann erst `update_vorgang_status(..., True)` aufrufen.
- Wenn möglich die vorhandene Store-Methode für Klassifikationsupdates nutzen, damit Validierung und Rückgabestruktur konsistent bleiben.
- Die bestehende N:M-Verknüpfung `transaktion_vorgaenge` und das zentrale Objekt `vorgaenge` bleiben die Grundlage; keine direkte Beleg-zu-Transaktion-Architektur einführen.
- Frontend-seitig sollte der bestehende Importdialog wiederverwendet werden; keine neue Seite einführen.

## Manuelle Testhinweise

- Im Dashboard eine Mail mit einem Vorgang importieren und eine bereits bestehende unvollständige Transaktion verknüpfen.
- Im Importdialog die erforderlichen Klassifikationsfelder der Transaktion ausfüllen, Direktabschluss aktivieren und importieren.
- Prüfen, dass der Vorgang nach dem Import den Status `abgeschlossen` hat, falls die Regeln passen.
- Den gleichen Flow ohne vollständige Pflichtfelder testen; der Import soll den Vorgang anlegen, aber offen lassen und eine erklärende Meldung liefern.
- Prüfen, dass ein Import ohne Inline-Klassifikation weiterhin wie bisher funktioniert.

## Offene Fragen

- Soll das Paket strikt nur den Mail-Import-Flow (`/api/mail/<id>/vorgang-import`) erweitern, oder existiert im Frontend zusätzlich ein separater manueller Direktabschluss-Dialog außerhalb des Mail-Reiters, der denselben Bedarf schon heute hat? Für dieses Paket nur der Mail-Import.
- Falls mehrere Transaktionen an den neuen Vorgang verknüpft werden: Sollen alle editierbar sein oder nur unvollständige? Für ein kleines Paket ist die Anzeige aller verknüpften Transaktionen mit Fokus auf die bearbeitbaren ausreichend.
