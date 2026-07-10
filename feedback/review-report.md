# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die Umsetzung erfüllt die fachlichen Muss-Anforderungen auf Basis des GitHub-Diffs; Branch-Zustand ist sauber und es sind passende UI-/API-Tests ergänzt.

## Zusammenfassung

Der Split-Editor ist in der Transaktionsdetailansicht nutzbar, zeigt vorhandene Splits an, erlaubt Bearbeiten/Hinzufügen/Entfernen und speichert über den bestehenden PUT-Endpunkt. Cent-Beträge werden als Ganzzahlen verarbeitet, lokale Betragsfehler und Backend-Validierungsfehler werden sichtbar angezeigt. Keine blockierenden Probleme gefunden.

# Review Report

## Ergebnis

**Accepted:** true

## Geprüfter Umfang

Geändert wurden laut GitHub Compare:

- `banking_dashboard/static/app.js`
- `tests/test_dashboard.py`
- `feedback/implementation_report.md`

Der Branch ist sauber gegenüber `main`: `ahead_by=1`, `behind_by=0`, keine Abweichungen zwischen Runner-Validierung und GitHub Compare.

## Fachliche Bewertung gegen das Arbeitspaket

### Erfüllte Muss-Anforderungen

- Vorhandene Splits werden weiterhin aus `transaction.splits` in der Transaktionsdetailansicht gerendert.
- Split-Zeilen enthalten Betrag, Beschreibung und Klassifikationsfelder inklusive Transaktionstyp, Oberkategorie, Unterkategorie, Sphäre, fachlicher Beschreibung und Vorgangs-ID.
- Split-Zeilen können bearbeitet, hinzugefügt und über den bestehenden Entfernen-Button entfernt werden.
- Das Speichern verwendet weiterhin `PUT /api/transactions/<id>/splits`.
- Nach erfolgreichem Speichern werden die vom Backend zurückgegebenen Split-Daten in den Editor übernommen und neu gerendert.
- Backend-Validierungsfehler werden jetzt im Split-Bereich über `.form-error` angezeigt und zusätzlich weiterhin über den allgemeinen Fehler-Toast gemeldet.
- Die bisherige Float-/Euro-Parsing-Logik wurde für Split-Eingaben durch eine ganzzahlige Cent-Validierung ersetzt.
- Leere und nicht ganzzahlige Beträge werden lokal sichtbar abgewiesen.

### Tests

Der neue Playwright-basierte Browser-Test deckt zentrale Akzeptanzkriterien ab:

- Anzeigen vorhandener Splits
- Bearbeiten vorhandener Split-Beträge
- Hinzufügen einer neuen Split-Zeile
- Speichern über den Split-Endpunkt
- Persistenzprüfung nach erneutem API-Laden
- lokale Fehlermeldung bei leerem Betrag
- Backend-400 bei unpassender Split-Summe und sichtbare Fehlermeldung
- keine Persistenzänderung nach fehlgeschlagenem Save

Laut Implementation Report wurde `pytest tests/test_dashboard.py` erfolgreich ausgeführt: 102 Tests bestanden, 6 übersprungen.

## Nicht blockierende Hinweise

- Der neue Browser-Test prüft das Entfernen bestehender Split-Zeilen nicht explizit. Die UI-Funktion ist vorhanden, aber ein dedizierter Test wäre sinnvoll.
- Für extreme Eingaben könnte zusätzlich geprüft werden, dass Cent-Beträge innerhalb von `Number.MAX_SAFE_INTEGER` liegen, bevor sie als JSON-Zahl gesendet werden.

## Kontext-Hinweis

Die nachgeladene vollständige `app.js`/`tests/test_dashboard.py` wirkte im Split-Bereich nicht vollständig deckungsgleich mit dem GitHub-Diff. Für die Entscheidung war das nicht blockierend, da der GitHub-Diff gemäß Review-Regeln maßgeblich ist und ausreichend Kontext zur Integration vorhanden war.

## Schlussbewertung

Keine blockierenden fachlichen oder technischen Probleme gefunden. Die Umsetzung erfüllt das Arbeitspaket und kann akzeptiert werden.
