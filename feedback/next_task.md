# Nächstes Arbeitspaket

## Titel

Split-Bereich in der Transaktionsdetailansicht für vorhandene Splits nutzbar machen

## Ziel

In der bestehenden Dashboard-Detailansicht einer einzelnen Transaktion die bereits vorhandenen Splits sichtbar laden, bearbeiten und per bestehender Split-API speichern können, ohne die übrige Transaktionsbearbeitung zu verändern.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Transaktionsdetailansicht um Split-Laden, Split-Liste, Editieren, Hinzufügen und Löschen ergänzen.
- banking_dashboard/static/index.html: kleine UI-Struktur für den Split-Bereich in der bestehenden Detailansicht ergänzen.
- banking_dashboard/server.py: nur falls für die bestehende PUT /api/transactions/<id>/splits-Antwort oder Fehlermeldungen minimale Anpassungen nötig sind.
- tests/test_dashboard.py: Verhalten für Laden, Speichern und Validierungsfehler der Split-Ansicht absichern.

## Muss umgesetzt werden

- In der Transaktionsdetailansicht einen Split-Bereich anzeigen, der vorhandene Splits aus der Detailantwort oder per Split-API lädt.
- Mehrere Split-Zeilen für eine Transaktion anlegen, bearbeiten und entfernen können.
- Pro Split mindestens Betrag sowie die vorhandenen Klassifikationsfelder pflegbar machen: Transaktionstyp, Oberkategorie, Unterkategorie, Sphäre, fachliche Beschreibung; Beschreibung des Splits ebenfalls bearbeitbar.
- Speichern muss die vorhandene PUT /api/transactions/<id>/splits-Schnittstelle nutzen und die komplette Split-Liste ersetzen.
- Vor dem Speichern muss eine nicht passende Split-Summe als Fehler erkennbar sein und eine verständliche Meldung auslösen.
- Nach erfolgreichem Speichern muss die Detailansicht aktualisiert werden und die gespeicherten Splits sichtbar bleiben.

## Soll umgesetzt werden

- Für die Eingabe der Klassifikationsfelder dieselben Vorschlagsquellen oder Auswahloptionen wie in der bestehenden Klassifikationsbearbeitung nutzen, soweit bereits vorhanden.
- Die UI sollte den Transaktions-Gesamtbetrag und die Summe der Splits klar unterscheiden.
- Leere neue Split-Zeilen möglichst mit sinnvollen Defaults starten.

## Nicht Teil dieses Arbeitspakets

- Aufteilung einer Transaktion auf mehrere Rechnungen oder Teilrechnungen
- Fachliches Modell für Rechnungshierarchien oder mehrstufige Zuordnungen
- Automatische Erzeugung oder Anpassung zusätzlicher Vorgänge je Split
- Verknüpfung mehrerer Mail-Anhänge mit unterschiedlichen Transaktionen innerhalb eines Vorgangs
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Integration

## Akzeptanzkriterien

- Für eine bestehende Transaktion kann im Dashboard eine Split-Liste angezeigt werden.
- Eine Transaktion kann im Dashboard in mindestens zwei Splits mit eigener Klassifikation aufgeteilt und gespeichert werden.
- Ein erneutes Öffnen derselben Transaktion zeigt die zuvor gespeicherten Splits unverändert an.
- Wenn die Split-Summe nicht dem Transaktionsbetrag entspricht, wird nicht stillschweigend gespeichert und der Nutzer erhält einen verständlichen Fehlerhinweis.
- Bestehende Transaktions-Klassifikationsfunktionen außerhalb der Split-Ansicht funktionieren weiterhin unverändert.
- Vorhandene Tests bleiben grün und Split-bezogene Tests decken mindestens erfolgreichen Save/Reload sowie einen Validierungsfehler ab.

## Hinweise für den Umsetzungs-Agenten

- Die Frontend-Detailansicht sollte möglichst auf der bereits gelieferten Split-Information aufsetzen und nur bei Bedarf den dedizierten Split-Endpunkt nutzen.
- Die Payload für PUT /api/transactions/<id>/splits muss dem bestehenden Parser entsprechen, inklusive der vorhandenen Feldnamen.
- Falls die UI Euro-Beträge bearbeitet, beim Senden sauber in Cent umrechnen und Rundungsfehler vermeiden.
- Änderungen klein halten: kein neuer globaler Zustand und kein neuer separater Split-Workflow außerhalb der bestehenden Transaktionsdetails.

## Manuelle Testhinweise

- Dashboard starten und eine Transaktion öffnen.
- Zwei Splits anlegen, die zusammen exakt den Originalbetrag ergeben, speichern und die Detailansicht erneut öffnen.
- Die Persistenz der Splits prüfen und sicherstellen, dass sie unverändert angezeigt werden.
- Die Beträge so ändern, dass die Summe nicht mehr passt, und prüfen, dass eine verständliche Fehlermeldung erscheint.
- Prüfen, dass normale Transaktionsdetails und bestehende Klassifikationsbearbeitung weiterhin funktionieren.

## Offene Fragen

- Ob die Summengleichheit bereits serverseitig strikt validiert wird, sollte vor der Umsetzung kurz geprüft werden.
- Ob Splits zusätzlich einen vorgangs_id-Bezug in der UI pflegbar machen sollen, ist für dieses kleine Paket nicht erforderlich.
