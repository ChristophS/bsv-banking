# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der Diff ist für die fachliche Prüfung ausreichend aussagekräftig; die Umsetzung erfüllt die Muss-Anforderungen ohne erkennbare Blocker.

## Zusammenfassung

Die Umsetzung ergänzt eine minimale Tabelle `transaction_splits`, erhöht die Schema-Version, liefert Split-Daten in Transaktionsdetails read-only als `splits` aus und ergänzt passende Schema- und API-/Store-Tests. Unsplittete Transaktionen werden weiterhin mit leerer Split-Liste unterstützt. Daher akzeptiert.

## Review-Ergebnis

**Akzeptiert:** Ja

## Prüfung gegen das Arbeitspaket

### Persistenzstruktur

Die SQLite-Schema-Version wurde von 13 auf 14 angehoben. Mit `transaction_splits` wurde eine nachvollziehbar benannte Split-Grundstruktur ergänzt. Die Tabelle enthält:

- `split_id` als Primärschlüssel
- `transaction_id` mit Foreign Key auf `transactions(transaction_id)` und `ON DELETE CASCADE`
- `amount_minor`
- optionale bzw. defaultbelegte Beschreibungs- und Klassifikationsfelder
- optionale `vorgangs_id` mit Foreign Key auf `vorgaenge(vorgangs_id)` und `ON DELETE SET NULL`
- `created_at` und `updated_at`
- Indizes für `transaction_id` und `vorgangs_id`

Das ist für das geforderte kleine technische Vorbereitungspaket passend und bleibt im Scope.

### Migration / Initialisierung

Die neue Migration `_migrate_v13_to_v14` erstellt die Vorgangstabelle sicherheitshalber und danach die Split-Tabelle. Die normale Schema-Initialisierung ruft ebenfalls `_create_transaction_split_table` auf. Damit werden neue Datenbanken und migrierte Datenbanken berücksichtigt.

### Read-only-Ausgabe in Transaktionsdetails

`banking_dashboard/server.py` erweitert `transaction_detail()` um eine zusätzliche Query auf `transaction_splits` und gibt die Ergebnisse unter `detail["splits"]` zurück. Die Feldnamen sind konsistent zur bestehenden deutschsprachigen API-Ausgabe gewählt, während die Persistenz englische Spaltennamen nutzt.

Transaktionen ohne Split liefern durch die Listenbildung eine leere Liste, was die bestehende Detailausgabe nicht bricht.

### Vorgangsdetails

Laut Umsetzung und Test wird die Split-Information in Vorgangsdetails über die bereits enthaltenen Transaktionsdetails sichtbar. Das entspricht dem Soll-Kriterium, ohne Rückgabetypen grundlegend umzubauen.

### Tests

Es wurden Tests ergänzt für:

- Existenz und Spalten der Tabelle `transaction_splits`
- Foreign Keys auf `transactions` und `vorgaenge`
- Transaktionsdetails mit Split-Daten
- Transaktionsdetails ohne Split-Daten
- Vorgangsdetails mit Split-Informationen in enthaltenen Transaktionen
- HTTP-Ausgabe über `/api/transactions/<id>`

Die bestehenden Migrationserwartungen wurden auf Schema-Version 14 aktualisiert. Die im Implementation Report genannten Testläufe sind plausibel und passend.

## Blockierende Probleme

Keine.

## Nicht blockierende Hinweise

- Ein expliziter Migrationstest von Version 13 auf 14 mit Assertion auf `transaction_splits` wäre noch etwas stärker, ist aber nicht zwingend blockierend, da die Migrationslogik im Diff nachvollziehbar ist und Schemaexistenz getestet wird.
- Der neue Datentyp `TransactionSplit` enthält aktuell nicht `created_at`/`updated_at`, obwohl diese in der Tabelle und API-Ausgabe vorhanden sind. Da der Typ im Diff nicht aktiv für die API-Ausgabe genutzt wird, ist das kein Blocker.
