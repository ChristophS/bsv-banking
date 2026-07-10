# Nächstes Arbeitspaket

## Titel

Transaktions-Splitting technisch vorbereiten und in Details read-only anzeigen

## Ziel

Ein kleines, zusammenhängendes erstes Paket für das Thema Transaktions-Splitting umsetzen: bestehende Datenbank- und Detailpfade minimal erweitern, sodass Split-Zuordnungen gespeichert und in Transaktionsdetails lesbar ausgegeben werden können, ohne den vollständigen Bearbeitungsworkflow zu bauen.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- banking_dashboard/server.py
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- transaction_store/database.py: bestehende SQLite-Initialisierung/Migration um eine minimale Split-Grundstruktur ergänzen.
- transaction_store/models.py: strukturierte Datentypen für Split-Daten ergänzen, falls dort DB-/API-Modelle zentral definiert sind.
- banking_dashboard/server.py: Detailausgaben für Transaktionen um read-only Split-Informationen erweitern.
- tests/test_transactions.py: Schema- und Persistenztests für Split-Grundstruktur ergänzen.
- tests/test_dashboard.py: API-Tests für die read-only Auslieferung der Split-Details ergänzen.

## Muss umgesetzt werden

- Eine minimale, repo-konforme Persistenzstruktur für Split-Zuordnungen in der bestehenden SQLite-Architektur ergänzen.
- Sicherstellen, dass unsplittete Transaktionen weiterhin unverändert funktionieren.
- GET /api/transactions/<id> um vorhandene Split-Informationen read-only erweitern.
- Tests ergänzen, die Schemaexistenz und die read-only Auslieferung der Split-Daten belegen.

## Soll umgesetzt werden

- Falls im bestehenden Datenmodell sinnvoll, Split-Einträge so benennen und strukturieren, dass spätere Zuordnungen zu Vorgängen oder Kategorien erweiterbar bleiben.
- Wenn leicht integrierbar, auch in Vorgangsdetails erkennbare Split-Informationen der zugeordneten Transaktionen mit ausgeben, ohne Rückgabetypen grundlegend umzubauen.

## Nicht Teil dieses Arbeitspakets

- Vollständige UI zum interaktiven Splitten von Transaktionen.
- Kompletter Bearbeitungsworkflow für Transaktion-Rechnung-Kategorie-Splits.
- Umbau der Klassifikationslogik von Transaktionsebene auf Split-Ebene.
- Automatische Migration aller historischen Transaktionen in Split-Zeilen.
- Mail-/Dokumenten-Thema mit mehreren Dokumenten pro Mail.
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Integration.

## Akzeptanzkriterien

- Die bestehende SQLite-Datenbank enthält eine neue, nachvollziehbar benannte Split-Grundstruktur.
- Bestehende Transaktions- und Vorgangsdetails funktionieren weiterhin ohne Fehlverhalten.
- GET /api/transactions/<id> liefert bei vorhandenen Split-Daten zusätzliche read-only Informationen zurück.
- Transaktionen ohne Split liefern weiterhin valide Detaildaten.
- Automatisierte Tests decken mindestens Schemaexistenz und die read-only Auslieferung der Split-Details ab.

## Hinweise für den Umsetzungs-Agenten

- Das Paket soll bewusst klein bleiben und nur die technische Grundlage sowie Sichtbarkeit schaffen.
- An bestehenden Mustern für zusammengesetzte Detaildaten in DashboardDataStore orientieren.
- Wenn in transaction_store.database.py bereits CREATE TABLE IF NOT EXISTS- oder Migrationslogik existiert, dort erweitern statt neue Strukturen daneben einzuführen.
- Keine neue Facharchitektur erfinden; Vorgänge bleiben zentral und bestehende Verknüpfungen sollen respektiert werden.

## Manuelle Testhinweise

- Lokales Dashboard starten und prüfen, dass Transaktionsliste und Vorgangsdetails weiterhin laden.
- Eine Testdatenbank mit mindestens einer Transaktion und manuell eingefügten Split-Zeilen verwenden und das Transaktionsdetail per API abrufen.
- Prüfen, dass Transaktionen ohne Split keine Fehler verursachen und die bisherigen Detailfelder erhalten bleiben.

## Offene Fragen

- Soll die Split-Zuordnung im ersten Schritt direkt an einen Vorgang gekoppelt werden oder zunächst nur unter der Transaktion hängen?
- Ist für die bestehende API eine zusätzliche View sinnvoll oder sollte die Ausgabe direkt aus den vorhandenen Queries zusammengesetzt werden?
