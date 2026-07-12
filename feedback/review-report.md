# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die nachgeladenen Dateien bestätigen die vollständige Vorabvalidierung, die unveränderte atomare Speicherung sowie die API- und Testeinbindung. Der Branch ist sauber einen Commit vor main.

## Zusammenfassung

Die Split-Vorgangszuordnung wird vor dem DELETE/INSERT atomar validiert, zulässige Vorgänge samt indirekt verknüpfter Belege werden über die Split-API geliefert, und Fehler lassen vorhandene Splits unverändert.

# Review Report

## Ergebnis

**Accepted:** ja

## Geprüfte Umsetzung

- `replace_transaction_splits` normalisiert leere `vorgangs_id` weiterhin zu `None`.
- Gesetzte Vorgangs-IDs werden vor Summenprüfung sowie vor dem `SAVEPOINT`-geschützten DELETE/INSERT-Zyklus geprüft:
  - nicht vorhandene IDs werden als `Unbekannte Vorgangs-ID` abgewiesen;
  - vorhandene, aber nicht über `transaktion_vorgaenge` mit der Ursprungstransaktion verknüpfte IDs werden mit einer verständlichen Validierungsfehlermeldung abgewiesen.
- Die Summenprüfung auf den exakten Transaktionsbetrag bleibt erhalten.
- Bei Validierungs- und Summenfehlern wird vor dem DELETE abgebrochen. Bei Fehlern während der Speicherung sichert der bestehende Savepoint den Rollback ab.
- `GET /api/transactions/{id}/splits` liefert `zulaessige_vorgaenge`. Die Auswahl enthält ausschließlich über `transaktion_vorgaenge` verknüpfte Vorgänge.
- Belege werden ausschließlich durch `vorgang_belege` und `belege` geladen und als Liste je Vorgang geliefert. Es wurde keine direkte Split- oder Transaktion-zu-Beleg-Beziehung ergänzt.
- Die vorhandene PUT-Route verwendet weiterhin den geprüften Speicherdienst und bildet `ValueError` als HTTP 400 ab.

## Tests

Die ergänzten Tests decken ab:

- das Laden zulässiger Vorgänge mit ihren über den Vorgang verknüpften Belegen;
- unbekannte Vorgangs-IDs;
- Vorgänge einer anderen Transaktion;
- unveränderte bereits gespeicherte Splits nach beiden Fehlerfällen;
- erfolgreiche Speicherung und erneutes Laden einer gültigen `vorgangs_id` über den bestehenden Split-Test.

Laut Umsetzungsbericht wurden `tests/test_dashboard.py` mit 110 erfolgreichen Tests und 6 erwarteten Skips sowie `tests/test_transactions.py` mit 33 erfolgreichen Tests ausgeführt.

## Nicht blockierender Hinweis

Ein eigenständiger HTTP-Test für den konkreten Inhalt von `zulaessige_vorgaenge` am GET-Endpunkt wäre eine sinnvolle zusätzliche Absicherung des öffentlichen API-Vertrags, ist für die Abnahme jedoch nicht erforderlich.
