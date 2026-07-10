# Nächstes Arbeitspaket

## Titel

Split-Grundlage in Datenmodell und API für Transaktionen anlegen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 1

## Ziel

Die bestehende Transaktions- und Vorgangsarchitektur um eine kleine, kontrollierte Split-Grundlage erweitern, damit Teilbeträge je Transaktion gespeichert, gelesen und gegen die Gesamtsumme validiert werden können, ohne bereits UI-Editor, Split-Klassifikation oder Rechnungszuordnungen umzusetzen.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- banking_dashboard/server.py
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- SQLite-Schema und Migrationslogik für neue Split-Tabellen in transaction_store/database.py
- Datenzugriffs- und Serialisierungsmodelle in transaction_store/models.py
- API-Endpunkte oder bestehende Detail-Response für Transaktionssplits in banking_dashboard/server.py
- API- und Persistenztests in tests/test_transactions.py
- Dashboard-API-Tests in tests/test_dashboard.py

## Muss umgesetzt werden

- Neue Persistenz für Split-Zeilen einer Transaktion auf Basis der bestehenden Transaktionsstruktur anlegen, ohne direkte neue Grundarchitektur außerhalb des Vorgangs-/Transaktionsmodells einzuführen.
- Pro Split mindestens stabile ID, transaktions_id, Reihenfolge, Betrag und optionale fachliche Felder für spätere Nutzung sauber speicherbar machen.
- Backend-Logik bereitstellen, um alle Splits einer Transaktion atomar zu speichern und wieder zu laden.
- Validierung einbauen, dass die Summe der Split-Beträge exakt dem Transaktionsbetrag entspricht und keine Splits für unbekannte Transaktionen gespeichert werden.
- Eine kleine read/write-API für Transaktionsdetails ergänzen, sodass Splits für genau eine Transaktion gelesen und ersetzt werden können.
- Tests für Schema, Speicherung, Laden und Summenvalidierung ergänzen.

## Soll umgesetzt werden

- Response-Strukturen so gestalten, dass spätere UI-Datalists, Split-Klassifikation und Vorgangsableitung darauf aufbauen können.
- Fehlermeldungen bei ungültigen Split-Summen konsistent und API-tauglich zurückgeben.
- Reihenfolge der Split-Zeilen stabil erhalten.

## Nicht Teil dieses Arbeitspakets

- Kein Split-Editor oder umfassender UI-Workflow im Frontend.
- Keine fachliche Ableitung von Klassifikationsstatus aus Split-Zeilen.
- Keine automatische Anpassung von Vorgangsstatus auf Basis von Splits.
- Keine Rechnungs-, Teilrechnungs- oder Belegzuordnung auf Split-Ebene.
- Keine Migration bestehender Transaktionen in künstliche Default-Splits, sofern nicht technisch zwingend nötig.

## Akzeptanzkriterien

- Die Datenbank enthält eine belastbare Struktur zur Speicherung mehrerer Split-Zeilen je bestehender Transaktion.
- Für eine Transaktion können Split-Zeilen per Backend gespeichert und anschließend vollständig wieder gelesen werden.
- Ein Speicherversuch mit Split-Summen ungleich Transaktionsbetrag wird abgewiesen.
- Ein Speicherversuch für unbekannte transaktions_id wird abgewiesen.
- Bestehende Transaktions- und Vorgangsdaten bleiben unverändert nutzbar, wenn keine Splits vorhanden sind.
- Automatisierte Tests decken mindestens erfolgreichen Split-Speicherfall, Summenfehler und erneutes Laden ab.

## Hinweise für den Umsetzungs-Agenten

- An bestehende Transaktions-IDs anknüpfen; keine neue zentrale fachliche Entität neben Vorgängen und Transaktionen erfinden.
- Split-Daten zunächst als Unterstruktur der Transaktion behandeln; spätere Vorgangs- und Rechnungslogik folgt in getrennten Teilpaketen.
- API lieber klein halten: ein Endpunkt/Flow für Lesen und ein Endpunkt/Flow für vollständiges Ersetzen der Split-Liste einer Transaktion genügt.
- Wenn bestehende Detail-Responses für Transaktionen vorhanden sind, Splits dort ergänzen statt parallele konkurrierende Strukturen aufzubauen.
- Beträge konsistent zu bestehender Minor-Unit- oder Decimal-Logik des Repos speichern und validieren.

## Manuelle Testhinweise

- Über die lokale API oder vorhandene Test-Hilfsroutinen eine bekannte Transaktion mit zwei Split-Zeilen anlegen, deren Summe dem Originalbetrag entspricht.
- Anschließend Transaktionsdetails abrufen und prüfen, dass beide Split-Zeilen in stabiler Reihenfolge zurückkommen.
- Danach einen absichtlich falschen Split mit abweichender Summe senden und prüfen, dass der Request sauber fehlschlägt.
- Eine Transaktion ohne Splits weiterhin normal im Dashboard/API abrufen und auf unverändertes Verhalten prüfen.

## Offene Fragen

- Welche fachlichen Felder sollen in Teil 1 bereits pro Split mitgeführt werden: nur Betrag und Notiz oder schon Transaktionstyp/Oberkategorie/Unterkategorie/Sphäre?
- Soll das API-Format Split-Beträge in Major- oder Minor-Units transportieren, passend zur bestehenden Server-API?
- Gibt es bereits einen bevorzugten Detail-Endpunkt für Transaktionen, der um Splits erweitert werden sollte, statt einen neuen Endpunkt einzuführen?
