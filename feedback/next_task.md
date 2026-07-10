# Nächstes Arbeitspaket

## Titel

Kleinen Split-Workflow im Dashboard für bestehende Transaktions-Splits fertig nutzbar machen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 2

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
- tests/test_dashboard.py: API- und Dashboard-Verhalten für Split-Anzeige und Speichern ergänzen.
- tests/test_transactions.py: vorhandene Split-Persistenz- oder Validierungsfälle bei Bedarf ergänzen.

## Muss umgesetzt werden

- In der Transaktions-Detailansicht einen Split-Bereich anzeigen, der vorhandene Splits aus den bereits gelieferten Detaildaten oder über die bestehende Split-API lädt.
- Benutzer muss mehrere Split-Zeilen für eine Transaktion anlegen, bearbeiten und entfernen können.
- Pro Split mindestens Betrag sowie die vorhandenen Klassifikationsfelder pflegbar machen: Transaktionstyp, Oberkategorie, Unterkategorie, Sphäre, fachliche Beschreibung; zusätzlich die Split-Beschreibung.
- Speichern muss die vorhandene Schnittstelle zum Ersetzen der kompletten Split-Liste verwenden.
- Vor dem Speichern oder beim Server-Response verständlich abfangen, wenn die Summe der Split-Beträge nicht exakt dem Transaktionsbetrag entspricht.
- Nach erfolgreichem Speichern muss die Detailansicht aktualisiert werden und die gespeicherten Splits sichtbar bleiben.

## Soll umgesetzt werden

- Für die Eingabe der Klassifikationsfelder dieselben Vorschlagsquellen oder Datalists wie in der bestehenden Klassifikationsbearbeitung nutzen, soweit im Frontend bereits verfügbar.
- Die UI sollte klar zwischen Transaktions-Gesamtbetrag, Split-Summe und Restdifferenz unterscheiden.
- Neue Split-Zeilen mit sinnvollen Defaults starten, wenn das klein umsetzbar ist.

## Nicht Teil dieses Arbeitspakets

- Aufteilung einer Transaktion auf mehrere Rechnungen oder Teilrechnungen
- Fachliches Modell für Rechnungshierarchien oder mehrstufige Zuordnungen
- Automatische Erzeugung oder Anpassung zusätzlicher Vorgänge je Split
- Pflege oder Auswahl von vorgangs_id pro Split, sofern dafür neuer komplexer UI-Flow nötig wäre
- Mail-/Dokumenten-Zuordnungen ohne direkten Bedarf für den kleinen Split-Editor
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Integration

## Akzeptanzkriterien

- Für eine bestehende Transaktion kann im Dashboard eine Split-Liste angezeigt werden.
- Eine Transaktion kann im Dashboard in mindestens zwei Splits mit eigener Klassifikation aufgeteilt und gespeichert werden.
- Ein erneutes Öffnen derselben Transaktion zeigt die zuvor gespeicherten Splits unverändert an.
- Wenn die Split-Summe nicht dem Transaktionsbetrag entspricht, wird nicht stillschweigend gespeichert und der Nutzer erhält einen verständlichen Fehlerhinweis.
- Bestehende Transaktions-Klassifikationsfunktionen außerhalb der Split-Ansicht funktionieren weiterhin unverändert.
- Vorhandene Tests bleiben grün und Split-bezogene Tests decken mindestens erfolgreichen Save/Reload sowie einen Validierungsfehler ab.

## Hinweise für den Umsetzungs-Agenten

- Das Arbeitspaket ist erkennbar Teil des bestehenden Epic epic-transaction-splits und baut auf bereits vorhandener Persistenz in transaction_splits auf.
- Vorhandene Vorgangs-, Beleg-, Transaktions- und Verknüpfungsstrukturen weiterverwenden; keine neue Grundarchitektur einführen.
- Da replace_transaction_splits() laut geladenem Datenbankcode bereits die Summengleichheit validiert, sollte die UI nur frühzeitig plausibilisieren und Backend-Fehler sauber anzeigen, statt doppelte Fachlogik neu zu erfinden.
- Wenn Detaildaten Splits bereits enthalten, diese bevorzugt wiederverwenden und nur bei Bedarf dedizierte Requests verwenden.
- Falls Euro-Beträge im Frontend bearbeitet werden, beim Senden sauber in Minor Units umrechnen und Rundungsfehler vermeiden.
- Änderungen klein halten: kein neuer globaler Frontend-Zustand und kein separater Split-Hauptworkflow außerhalb der bestehenden Transaktionsdetails.

## Manuelle Testhinweise

- Dashboard starten, Transaktion öffnen und prüfen, dass ein Split-Bereich sichtbar ist.
- Zwei Splits mit zusammen exakt dem Originalbetrag anlegen, speichern und dieselbe Transaktion erneut öffnen.
- Einen Split löschen oder Beträge so ändern, dass die Summe nicht mehr passt; prüfen, dass eine verständliche Fehlermeldung erscheint.
- Prüfen, dass die normale Klassifikationsbearbeitung der Transaktion weiterhin funktioniert.

## Offene Fragen

- Soll der Split-Editor in dieser Ausbaustufe bereits vorhandene Vorschlagslisten für alle Klassifikationsfelder vollständig wiederverwenden oder reicht zunächst ein einfacher Eingabeflow mit optionalen Datalists?
- Soll die UI bei leerer Split-Liste einen Standardvorschlag mit zwei Zeilen anbieten oder nur mit einer leeren Zeile starten?
