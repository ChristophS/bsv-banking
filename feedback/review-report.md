# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Split-API validiert Cent-Beträge nun strikt als echte Ganzzahlen und weist Floats, numerische Strings sowie Booleans mit HTTP 400 beziehungsweise ValueError zurück. Die Persistenzvalidierung erfolgt zusätzlich vor dem atomaren Austausch. Bestehende Validierungen, Fehlerabbildungen, Split-Summen- und Vorgangsreferenzprüfungen bleiben erhalten und werden durch passende HTTP- und Persistenztests abgesichert. Der GitHub-Compare ist sauber und enthält keine unerwarteten Dateien.

## Review-Ergebnis

### Entscheidung

**Akzeptiert.**

### Geprüfte Anforderungen

- Der bestehende GET-/PUT-Flow für `/api/transactions/<id>/splits` verwendet weiterhin die vorhandene Split-Persistenz.
- Leere Transaktions-IDs werden als fachlicher Fehler behandelt; unbekannte Transaktionen führen zu HTTP 404.
- Ungültiges JSON, unbekannte Split-Felder und widersprüchliche Transaktions-IDs werden als HTTP 400 mit JSON-Fehlernachricht abgelehnt.
- Cent-Beträge werden im Request-Handler strikt auf echte Integer geprüft. Floats, numerische Strings und Booleans werden nicht mehr still konvertiert.
- Die gleiche Typprüfung wurde in `transaction_store.database.replace_transaction_splits` ergänzt und erfolgt vor dem Schreibvorgang.
- Split-Summen, Vorgangsreferenzen und doppelte Split-IDs werden weiterhin über die bestehende Persistenzlogik geprüft.
- Der eigentliche Austausch der Split-Zeilen bleibt durch Savepoint und die bestehende Transaktion atomar.
- Tests prüfen erfolgreiche Speicherung, ungültiges JSON, unbekannte Transaktionen, leere IDs, ungültige Cent-Typen sowie unveränderte Splits nach abgelehnten Requests.
- Die Änderungen umgehen weder Vorgangs- noch N:M-Verknüpfungsstrukturen und führen keine externen Aktionen aus.

### Diff- und Branch-Prüfung

Der GitHub-Compare ist `ahead` mit einem Commit, nicht hinter `main`, und enthält keine fehlenden oder unerwarteten Dateien. Die Änderungen liegen in den erwarteten Produktions- und Testdateien sowie im Implementierungsbericht. Es gibt keinen erkennbaren Scope Creep oder einen unbrauchbaren Branch-Zustand.

### Nicht blockierende Hinweise

Die Aliasfelder `betrag_cent` und `amount_minor` werden weiterhin nach der etablierten Priorität ausgewertet; eine zusätzliche Konfliktprüfung bei gleichzeitig gesetzten Aliasfeldern wäre lediglich eine optionale Härtung. Ebenso könnte ein zusätzlicher Test die vollständige Antwortstruktur des erfolgreichen PUT noch expliziter gegen alle etablierten Feldnamen prüfen. Beides verhindert die Freigabe nicht.
