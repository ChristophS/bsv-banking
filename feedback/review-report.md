# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die maßgeblichen GitHub-Diffs erfüllen die Muss-Anforderungen: bestehender POST-/Validierungsfluss wird genutzt, die UI sendet bereits completed und Verknüpfungs-IDs aus dem Kandidatenkatalog, Backend-Fehler werden nun dauerhaft im Formular angezeigt und API-Tests decken Erfolg und Ablehnung ab.

## Zusammenfassung

Akzeptiert: Der bestehende manuelle Vorgangs-Erstellflow unterstützt den Direktabschluss mit verknüpften Transaktionen bereits, und diese Umsetzung ergänzt die notwendige sichtbare Formular-Fehleranzeige sowie API-Tests für erfolgreichen und blockierten Direktabschluss.

# Review Report

## Ergebnis

**Accepted:** true

## Geprüfter Umfang

Geprüft wurden das Arbeitspaket, der Implementation Report, der GitHub-Diff und der nachgeladene Kontext zu `banking_dashboard/static/app.js`, `banking_dashboard/server.py` und `transaction_store/database.py`.

Hinweis: Der nachgeladene Vollinhalt von `banking_dashboard/static/app.js` zeigt an der geänderten Stelle nicht die im GitHub-Diff enthaltene `.form-error`-Ergänzung. Für die Bewertung ist gemäß Vorgabe der GitHub-Diff maßgeblich; der übrige Kontext war ausreichend, um den bestehenden Flow zu prüfen.

## Bewertung gegen die Anforderungen

### Direktabschluss per POST `/api/vorgaenge`

Erfüllt. `DashboardDataStore.create_vorgang(...)` verarbeitet `completed=true`, setzt den Status auf `abgeschlossen` und ruft vor dem Insert `_validate_vorgang_completion_values(...)` auf. Diese Validierung nutzt die bestehenden Abschlussbedingungen für unvollständig klassifizierte Transaktionen sowie Rechnung-Transaktion/Dokument-Anforderungen. Es wurde keine neue Sonderlogik für manuelle Vorgänge eingeführt.

Die neuen Tests in `tests/test_dashboard.py` decken ab:

- erfolgreichen Direktabschluss eines neu angelegten Vorgangs mit verknüpfter vollständig klassifizierter Transaktion,
- HTTP-400-Ablehnung bei unvollständig klassifizierter Transaktion,
- kein stilles Offen-Anlegen im Fehlerfall.

### UI-Verknüpfungsauswahl und completed-Option

Erfüllt durch den bestehenden Erstellflow in `renderVorgangCreateForm(...)`: Das Formular lädt über `loadLinkCandidates()` den vorhandenen Kandidatenkatalog aus `GET /api/vorgaenge/link-candidates`, rendert unter anderem die Sektion `Transaktionen` und sendet über `readVorgangForm(...)` sowohl `completed` als auch `transaction_ids`, `mail_ids`, `todo_ids`, `beleg_ids` und `termin_ids` an `POST /api/vorgaenge`.

Die vorhandene Kandidatendarstellung enthält bei Transaktionen zudem Klassifikationsinformationen über `transactionClassificationSummary(...)`, sodass Nutzer erkennen können, ob die Transaktion vollständig klassifiziert ist.

### Sichtbare Backend-Fehlermeldung im Frontend

Erfüllt. Der Diff ergänzt im Erstellformular ein dauerhaft sichtbares Element `.form-error`, setzt es vor jedem Submit zurück und befüllt es im Catch-Zweig mit `error.message`. Damit wird die vom Backend gelieferte konkrete Fehlermeldung nicht nur als kurzlebiger Toast angezeigt, sondern bleibt im Formular sichtbar.

### Keine unerlaubte Architekturänderung / Scope Creep

Erfüllt. Es wurden keine geschützten produktiven Daten, Secrets oder externen Dienste verändert. Die Persistenz- und Abschlusslogik bleibt unverändert und wird wiederverwendet. Die zusätzliche CSS-Regel ist klein und zweckbezogen.

### Tests und Branch-Zustand

Der Branch ist sauber vergleichbar (`ahead_by=1`, `behind_by=0`, `compare_status=ahead`). Laut Implementation Report wurde `tests/test_dashboard.py` erfolgreich ausgeführt (`72 passed, 2 skipped`). Die zwei neuen API-Tests sind fachlich passend für die Kernanforderung.

## Nicht blockierende Hinweise

- Ein UI-/Browser-Test für die neue Formular-Fehleranzeige wäre hilfreich, aber für dieses Paket nicht zwingend.
- Die Direktabschluss-Checkbox im manuellen Erstellformular könnte noch einen kurzen erläuternden Hilfetext erhalten, analog zum Mail-Flow.
