# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Anforderungen des Arbeitspakets sind durch die bestehenden To-Do-Validierungs- und Handlerpfade erfüllt und werden mit umfangreichen lokalen HTTP-Regressionstests abgesichert. Die Tests decken ungültige Payloads, unbekannte Vorgangs- und To-Do-IDs, JSON-Fehlerantworten, Statuscodes, atomare Persistenz sowie die bestehenden N:M-Verknüpfungen ab. GitHub Compare ist sauber und enthält keine fehlenden oder zusätzlichen Änderungen.

# Technischer Review

## Ergebnis

**Accepted:** ja

## Geprüfter Umfang

- `tests/test_dashboard.py`
- `banking_dashboard/server.py`
- GitHub-Diff des Commits `cf88e42fd3256b80873b37825c2925ebe0e8c607`
- Runner- und GitHub-Compare-Status

## Bewertung der Muss-Anforderungen

Die vorhandenen To-Do-Flows verwenden weiterhin die bestehende `DashboardDataStore`- und Handler-Architektur. Es wurde keine parallele Persistenz- oder API-Architektur eingeführt und das bestehende `todo_vorgaenge`-Verknüpfungsmodell bleibt unverändert.

Die vollständige Prüfung von `banking_dashboard/server.py` bestätigt:

- `create_todo` und `update_todo` lehnen unbekannte Felder ab.
- Prioritäten werden gegen `niedrig`, `normal` und `hoch` validiert.
- Fälligkeitsdaten werden als ISO-Datum validiert.
- `vorgangs_ids` müssen Listen sein und werden gegen vorhandene Vorgänge geprüft.
- Unbekannte Vorgangsreferenzen lösen `LookupError` aus.
- Unbekannte To-Do-IDs bei Update und Delete lösen `LookupError` aus.
- Die Handler bilden `ValueError` konsistent auf HTTP 400 und `LookupError` auf HTTP 404 mit einem JSON-Objekt mit `error` ab.
- Fehler während der Linkvalidierung werden vor dem Commit ausgelöst; uncommittete Änderungen werden beim Schließen der Verbindung verworfen.
- Erfolgreiche Flows verwenden weiterhin `_replace_todo_vorgaenge` und damit die bestehende N:M-Tabelle.

## Tests

Die neuen Tests in `tests/test_dashboard.py` decken ab:

- POST mit unbekanntem Feld, ungültiger Priorität, ungültigem Datum und nicht listenförmigen `vorgangs_ids`.
- PATCH mit denselben relevanten ungültigen Eingaben.
- HTTP-400-Statuscodes und JSON-Fehlerobjekte.
- POST und PATCH mit nicht vorhandenen Vorgangs-IDs und HTTP 404.
- Keine partiellen Änderungen an To-Dos oder `todo_vorgaenge` nach fehlgeschlagenem PATCH.
- Kein zurückbleibendes To-Do nach fehlgeschlagenem POST.
- PATCH und DELETE mit unbekannter To-Do-ID und HTTP 404 einschließlich konsistentem Fehlertext.
- Erfolgreiche Erstellung, Änderung, Löschung und Vorgangsverknüpfungen über den bestehenden CRUD-Test.

Die Tests verwenden eine temporäre SQLite-Datenbank und den lokalen Testserver. Browser, Netzwerkzugriff, Secrets und produktive Laufzeitdaten sind für dieses Arbeitspaket nicht erforderlich.

## Diff- und Scope-Prüfung

Der GitHub-Diff enthält ausschließlich die präzisierten Regressionstests und die aktualisierte Implementierungsdokumentation. Es gibt keine unerlaubten Änderungen an Datenmodell, UI oder anderen API-Bereichen. Runner und GitHub Compare stimmen überein; der Branch ist einen Commit vor `main`, nicht hinterher und enthält keine fehlenden oder zusätzlichen Compare-Dateien.

## Entscheidung

Die Muss-Anforderungen und Akzeptanzkriterien sind erfüllt. Die Implementierung kann angenommen werden.
