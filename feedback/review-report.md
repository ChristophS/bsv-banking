# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der Diff ist ausreichend aussagekräftig; Umsetzung, API-Flow, UI-Anbindung und Tests decken die Muss-Anforderungen ab.

## Zusammenfassung

Die Umsetzung ergänzt einen dedizierten, idempotenten Backend-Flow zum Verknüpfen einer Transaktion mit einem bestehenden Vorgang, erweitert Vorschläge/Kandidaten um Vorgänge und bindet die Zuordnung in der Transaktionsdetailansicht ein. Erfolgsfall, Wiederholung und Fehlerfall sind getestet; es gibt keine blockierenden Auffälligkeiten.

## Review-Ergebnis

**Accepted:** ja

## Geprüfte Anforderungen

- Eine Transaktion kann über eine dedizierte Backend-Methode `link_transaction_vorgang` und den neuen Endpunkt `POST /api/transactions/{transaktions_id}/vorgaenge` einem bestehenden Vorgang zugeordnet werden.
- Die Zuordnung nutzt weiterhin die bestehende Tabelle `transaktion_vorgaenge`; es wurde keine neue Parallelstruktur eingeführt.
- Bestehende Links werden nicht ersetzt, da der Flow nicht über `update_vorgang` beziehungsweise `_replace_vorgang_links` läuft.
- Die Zuordnung ist durch `INSERT OR IGNORE` idempotent und erzeugt bei Wiederholung keine Duplikate.
- Unbekannte Vorgangs-IDs werden vor der Persistenz erkannt und führen über `LookupError` zu einem sauberen Fehlerpfad; der HTTP-Test erwartet hierfür 404.
- `suggest_related_entities` liefert für `source_type: transaction` jetzt auch `vorgaenge` in `suggestions` und `candidates`.
- Die UI lädt Vorgangsvorschläge beim Öffnen einer Transaktion, zeigt bereits verknüpfte Vorgänge an, filtert diese aus der Auswahlliste heraus und lädt die Transaktionsdetailansicht nach erfolgreicher Zuordnung neu.
- Tests wurden für Store-Erfolgsfall, idempotente Wiederholung, Fehlerfall, Vorgangsvorschläge sowie den HTTP-Endpunkt ergänzt.

## Technische Bewertung

Die Lösung folgt dem im Arbeitspaket empfohlenen Ansatz eines dedizierten Link-Flows und vermeidet dadurch das Risiko, bestehende Vorgangs-Linklisten unbeabsichtigt zu überschreiben. Die Validierung von Transaktion und Vorgang vor dem Insert ist fachlich sinnvoll. Die Vorschlagslogik nutzt bestehende Vorgangsfelder sowie Texte verknüpfter Transaktionen und integriert sich in den vorhandenen Suggestion-/Candidate-Mechanismus.

Der UI-Flow ist ausreichend: Bereits bestehende Vorgangsverknüpfungen werden angezeigt, neue Kandidaten können ausgewählt werden, doppelte Verknüpfungen werden herausgefiltert beziehungsweise backendseitig idempotent behandelt, und nach erfolgreichem POST wird die Detailansicht aktualisiert.

## Tests

Laut Implementation Report wurde `tests/test_dashboard.py` erfolgreich ausgeführt mit `92 passed, 4 skipped`. Die im Diff sichtbaren Tests decken die zentralen Akzeptanzkriterien ab.

## Blockierende Punkte

Keine.

## Nicht-blockierende Hinweise

- Ein zusätzlicher HTTP-Test für eine unbekannte Transaktions-ID wäre als Absicherung nützlich.
- Eine explizit sichtbare Erfolgsmeldung in der UI kann später verbessert werden, falls der vorhandene Statushinweis nicht ausreichend auffällt.
