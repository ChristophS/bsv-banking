# Nächstes Arbeitspaket

## Titel

Dashboard-Grundlage für Anzeige und Speicherung vorhandener Transaktions-Splits anbinden

## Ziel

Vorhandene `transaction_splits`-Persistenz im lokalen Dashboard sichtbar und nutzbar machen, sodass Splits zu einer Transaktion über API und UI geladen und gespeichert werden können. Damit entsteht die technische Grundlage für den späteren vollständigen Split-Bearbeitungsworkflow.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- transaction_store/database.py: vorhandene Split-Store-Funktionen als Datenquelle für API-Roundtrip nutzen, falls kleine Anpassung an Serialisierung/Mapping nötig ist.
- transaction_store/models.py: Modellfelder für Split-JSON korrekt abbilden, ohne neues Parallelmodell einzuführen.
- banking_dashboard/server.py: API-Endpunkt für Lesen/Speichern von Splits an bestehende Transaktionsdetail-Logik anbinden.
- banking_dashboard/static/app.js: Splits in der Transaktionsdetailansicht laden, anzeigen und speichern.
- banking_dashboard/static/index.html: kleiner UI-Bereich in der Transaktionsdetailansicht für Split-Liste/Formularfelder.
- tests/test_dashboard.py: API-Verhalten für Split-Read/Write und Fehlerfall ergänzen.
- tests/test_transactions.py: Persistenz-Roundtrip und Validierung für `replace_transaction_splits`/`list_transaction_splits` absichern.

## Muss umgesetzt werden

- Einen repo-konsistenten API-Zugriff im Dashboard bereitstellen, der Splits einer Transaktion ausliest und als JSON zurückgibt.
- Einen API-Zugriff zum vollständigen Ersetzen der Splits einer Transaktion bereitstellen, der intern `replace_transaction_splits` nutzt.
- JSON-Felder konsistent zu den vorhandenen Modellfeldern halten: mindestens `split_id`, `transaction_id`, `amount_minor`, `description`, `transaction_type`, `top_category`, `sub_category`, `sphere`, `professional_description`, `vorgangs_id`, `created_at`, `updated_at`.
- Im Frontend die vorhandenen Splits in der Transaktionsdetailansicht sichtbar machen.
- Im Frontend das Speichern einer kompletten Split-Liste ermöglichen, inklusive Anzeige eines verständlichen Fehlers bei ungültiger Split-Summe.
- Nach erfolgreichem Speichern die Splits erneut vom Server laden oder den Detailzustand konsistent aktualisieren, damit erzeugte `split_id`/Zeitstempel sichtbar werden.

## Soll umgesetzt werden

- Leeren Zustand klar anzeigen, wenn eine Transaktion noch keine Splits hat.
- Bei Beträgen im Frontend wenn möglich klar zwischen Anzeigeformat und `amount_minor` unterscheiden, um Rundungsfehler zu vermeiden.
- Fehlermeldungen aus dem Backend möglichst unverändert oder gut verständlich an die UI weitergeben.

## Nicht Teil dieses Arbeitspakets

- Kompletter komfortabler Split-Editor mit dynamischem Hinzufügen mehrerer Rechnungen und Kategorienlogik.
- Automatische Erzeugung oder Neuorganisation von Vorgängen aus Splits.
- Dokumenten- oder Mail-Zuordnung zu einzelnen Splits.
- Migrationstest 13→14 separat absichern.
- Entscheidung, ob `TransactionSplit`-Zeitstempel modellseitig noch anders abgebildet werden sollen, über das aktuelle API-/UI-Roundtrip-Niveau hinaus.

## Akzeptanzkriterien

- Für eine Transaktion ohne Splits liefert das Dashboard einen stabilen leeren Split-Zustand und die UI zeigt diesen ohne Fehler an.
- Für eine Transaktion mit vorhandenen Splits zeigt die Detailansicht alle gespeicherten Split-Felder an.
- Das Speichern einer gültigen Split-Liste mit exakt passender Gesamtsumme persistiert die Daten in `transaction_splits` und liefert sie anschließend wieder zurück.
- Das Speichern einer ungültigen Split-Liste mit abweichender Summe schlägt ohne Teilpersistenz fehl und zeigt im Dashboard eine verständliche Fehlermeldung an.
- Vorhandene Persistenzregeln aus `replace_transaction_splits` bleiben wirksam; der Dashboard-Code dupliziert diese Validierung nicht widersprüchlich.
- Automatisierte Tests decken mindestens einen erfolgreichen Roundtrip und einen Fehlerfall ab.

## Hinweise für den Umsetzungs-Agenten

- In `transaction_store/database.py` existiert die Kernlogik bereits; der Schwerpunkt dieses Pakets liegt auf dem sauberen Durchreichen über Server und UI.
- Da `replace_transaction_splits` vollständiges Ersetzen verwendet, sollte der API-Vertrag klar machen, dass immer die komplette Split-Liste übergeben wird.
- Falls `TransactionSplit` in `transaction_store/models.py` bereits ein Dataclass-/Modelltyp ist, sollte die Server-Serialisierung diesen Typ direkt abbilden statt ein paralleles Split-Datenmodell im Dashboard einzuführen.
- Wenn es im Server bereits Endpunkte für Transaktionsdetails gibt, ist eine Einbettung der Splits dort wahrscheinlich konsistenter als ein völlig isolierter Endpunkt; sofern beides existiert, sollte die Lösung zur bestehenden API-Struktur passen.
- Die UI sollte klein bleiben: Liste/Tabellenabschnitt im Transaktionsdetail genügt. Kein neuer Navigationspunkt.
- Bei Tests auf `amount_minor` fokussieren; nur Anzeigeumrechnung im Frontend, keine Float-basierte Fachlogik im Backend.

## Manuelle Testhinweise

- Dashboard starten, eine bestehende Transaktion öffnen und prüfen, dass ohne Splits ein leerer Bereich ohne JS-Fehler erscheint.
- Für eine Testtransaktion Splits mit exakt passender Cent-Summe speichern und die Detailansicht neu öffnen; alle Werte inklusive generierter IDs/Zeitstempel sollen sichtbar sein.
- Anschließend absichtlich eine falsche Gesamtsumme speichern und prüfen, dass nichts teilweise gespeichert wurde und eine verständliche Fehlermeldung erscheint.
- Optional Datenbankzustand kontrollieren, ob alte Splits beim Ersetzen entfernt und neue sauber eingefügt wurden.

## Offene Fragen

- Soll die Split-Anzeige ausschließlich in der Transaktionsdetailansicht erscheinen oder zusätzlich in Vorgangsdetails? Für dieses Paket wird nur die Transaktionsdetailansicht empfohlen.
- Soll das Frontend `amount_minor` direkt editieren oder Euro-Eingaben auf Cent umrechnen? Fachlich sicherer ist Backend in Cent, UX-freundlicher ist Euro-Eingabe; die Implementierung soll sich an vorhandenen Eingabemustern im Dashboard orientieren.
- Falls ein Split `vorgangs_id` setzen darf: soll die UI dieses Feld zunächst nur roh anzeigen/bearbeiten oder vorerst read-only lassen? Für ein kleines Paket ist einfache Text-/ID-Unterstützung ausreichend.
