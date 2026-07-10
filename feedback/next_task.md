# Nächstes Arbeitspaket

## Titel

Kleinen Split-Workflow im Dashboard für bestehende Transaktions-Splits fertig nutzbar machen

## Ziel

Die bereits vorhandene Backend-Unterstützung für transaction_splits im lokalen Dashboard sichtbar und bearbeitbar machen, sodass eine einzelne Transaktion in mehrere fachlich klassifizierte Teilsummen aufgeteilt und gespeichert werden kann.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- transaction_store/database.py
- transaction_store/models.py
- tests/test_dashboard.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Transaktions-Detailansicht um Laden, Anzeigen, Bearbeiten und Speichern von Splits ergänzen.
- banking_dashboard/static/index.html: Platzhalter/Struktur für einen kleinen Split-Bereich in der bestehenden Transaktions-Detailansicht ergänzen.
- banking_dashboard/server.py: nur falls für Fehlermeldungen oder Response-Formate kleine Anpassungen nötig sind; keine neue Architektur.
- tests/test_dashboard.py: API- und/oder Dashboard-Verhalten für Splits ergänzen, insbesondere Laden und Ersetzen.
- tests/test_transactions.py: falls bereits Store-/DB-nahe Split-Tests vorhanden sind, diese um Validierungs- oder Persistenzfälle ergänzen.

## Muss umgesetzt werden

- In der Transaktions-Detailansicht einen Split-Bereich anzeigen, der vorhandene Splits aus transaction_detail.splits oder per Split-API lädt.
- Benutzer muss mehrere Split-Zeilen für eine Transaktion anlegen, bearbeiten und entfernen können.
- Pro Split mindestens Betrag in Cent/Euro sowie die vorhandenen Klassifikationsfelder pflegbar machen: Transaktionstyp, Oberkategorie, Unterkategorie, Sphäre, fachliche Beschreibung; Beschreibung des Splits ebenfalls bearbeitbar.
- Speichern muss die vorhandene PUT /api/transactions/<id>/splits-Schnittstelle nutzen und die komplette Split-Liste ersetzen.
- Vor dem Speichern clientseitig oder serverseitig klar abfangen, wenn die Summe der Split-Beträge nicht exakt dem Transaktionsbetrag entspricht; der Nutzer braucht eine verständliche Fehlermeldung.
- Nach erfolgreichem Speichern muss die Detailansicht aktualisiert werden und die gespeicherten Splits sichtbar bleiben.

## Soll umgesetzt werden

- Für die Eingabe der Klassifikationsfelder dieselben Vorschlagsquellen bzw. Auswahloptionen wie in der bestehenden Klassifikationsbearbeitung nutzen, soweit im Frontend bereits verfügbar.
- Die UI sollte klar zwischen Transaktions-Gesamtbetrag und Summe der Splits unterscheiden und eine Restdifferenz sichtbar machen.
- Falls technisch klein umsetzbar, leere/neue Split-Zeilen mit sinnvollen Defaults starten, statt alle Felder manuell leer bauen zu müssen.

## Nicht Teil dieses Arbeitspakets

- Aufteilung einer Transaktion auf mehrere Rechnungen oder Teilrechnungen
- Fachliches Modell für Rechnungshierarchien oder mehrstufige Zuordnungen
- Automatische Erzeugung oder Anpassung zusätzlicher Vorgänge je Split
- Verknüpfung mehrerer Mail-Anhänge mit unterschiedlichen Transaktionen innerhalb eines Vorgangs
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Integration

## Akzeptanzkriterien

- Für eine bestehende Transaktion kann im Dashboard eine Split-Liste angezeigt werden.
- Eine Transaktion kann im Dashboard in mindestens zwei Splits mit eigener Klassifikation aufgeteilt und gespeichert werden.
- Ein erneutes Öffnen derselben Transaktion zeigt die zuvor gespeicherten Splits unverändert an.
- Wenn die Split-Summe nicht dem Transaktionsbetrag entspricht, wird nicht stillschweigend gespeichert und der Nutzer erhält einen verständlichen Fehlerhinweis.
- Bestehende Transaktions-Klassifikationsfunktionen außerhalb der Split-Ansicht funktionieren weiterhin unverändert.
- Vorhandene Tests bleiben grün und Split-bezogene Tests decken mindestens erfolgreichen Save/Reload sowie einen Validierungsfehler ab.

## Hinweise für den Umsetzungs-Agenten

- Da transaction_detail() bereits splits liefert, sollte die Frontend-Detailansicht möglichst darauf aufsetzen und nur bei Bedarf den dedizierten Split-Endpunkt nachladen.
- Die Payload für PUT /api/transactions/<id>/splits muss dem bestehenden Parser in _transaction_splits_from_payload() entsprechen, inklusive Unterstützung der deutschen/englischen Feldnamen.
- Falls die UI Euro-Beträge bearbeitet, beim Senden sauber in amount_minor/betrag_cent umrechnen und Rundungsfehler vermeiden.
- Wenn die Backend-Funktion replace_transaction_splits() bereits Summenvalidierung enthält, diese nicht duplizieren; andernfalls mindestens im UI frühzeitig plausibilisieren und Backend-Fehler anzeigen.
- Änderungen klein halten: kein neuer globaler Zustand und kein neuer separater Split-Workflow außerhalb der bestehenden Transaktionsdetails.

## Manuelle Testhinweise

- Dashboard starten, Transaktion öffnen, Split-Bereich prüfen.
- Zwei Splits mit zusammen exakt dem Originalbetrag anlegen, speichern, Detailansicht neu öffnen und Persistenz prüfen.
- Einen Split löschen bzw. Beträge so ändern, dass die Summe nicht mehr passt; prüfen, dass eine verständliche Fehlermeldung erscheint.
- Prüfen, dass normale Transaktionsdetails und bestehende Klassifikationsbearbeitung weiterhin funktionieren.

## Offene Fragen

- Ob replace_transaction_splits() die Summengleichheit bereits serverseitig strikt validiert, ist aus dem geladenen Ausschnitt nicht eindeutig ersichtlich; falls nicht, sollte der Umsetzungs-Agent die bestehende DB-Logik zuerst prüfen und nur minimal ergänzen.
- Ob Splits zusätzlich einen vorgangs_id-Bezug in der UI pflegbar machen sollen, ist im kleinen Paket nicht zwingend; wenn das im Code schon vorgesehen, nur freischalten, wenn der Nutzen ohne neue Komplexität klar ist.
