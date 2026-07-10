# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die nachgeladenen Dateien zeigen, dass die geforderte Split-Grundlage im aktuellen Stand bereits vorhanden ist; der GitHub-Diff enthält allerdings nur den Implementation-Report.

## Zusammenfassung

Akzeptiert: Obwohl der Branch selbst nur den Implementation-Report ändert, erfüllt der geladene aktuelle Code die fachlichen Anforderungen: Transaktionsdetails liefern Splits, die UI zeigt und ersetzt mehrere Split-Zeilen per PUT, Backend-Validierungsfehler werden sichtbar gemacht und passende API-/Store-Tests sind vorhanden.

# Review Report

## Ergebnis

**Accepted:** true

## Geprüfter Stand

- Branch: `agent2/codex-20260710-152331`
- Commit: `a1665fb9098731531d9df7d538ec00aeb1e0582d`
- GitHub Compare: `ahead`, `ahead_by=1`, `behind_by=0`
- Tatsächlicher Diff: ausschließlich `feedback/implementation_report.md`

Der erste Review hatte zusätzlichen Kontext angefordert, weil der Diff keine Code-/Teständerungen enthält. Die angeforderten Dateien wurden vollständig nachgeladen und für diese Entscheidung geprüft.

## Fachliche Bewertung gegen das Arbeitspaket

### Erfüllte Muss-Anforderungen

- **Splits in der Transaktionsdetailansicht sichtbar:**  
  `DashboardDataStore.transaction_detail()` lädt `list_transaction_splits()` und serialisiert die Splits über `_serialize_transaction_split()` mit Betrag, Beschreibung, Klassifikationsfeldern, optionaler `vorgangs_id` sowie Zeitstempeln. `appendSplitEditor()` rendert diese Daten in der Detailansicht.

- **Einfache Bearbeitung mehrerer Split-Zeilen:**  
  `appendSplitEditor()` erlaubt Hinzufügen und Entfernen von Zeilen sowie Bearbeitung von Betrag, Beschreibung, Klassifikation, fachlicher Beschreibung und Vorgangs-ID.

- **Speichern über bestehende PUT-API:**  
  Das Frontend sendet die vollständige Liste an `PUT /api/transactions/<id>/splits`. Der Server routet dies in `do_PUT()` an `DashboardDataStore.replace_transaction_splits()`, welches den bestehenden Store-Mechanismus nutzt.

- **Detailzustand nach Erfolg konsistent:**  
  Nach erfolgreichem Speichern übernimmt das Frontend `result.transaction`, zeichnet die Split-Zeilen neu und aktualisiert die Zusammenfassung.

- **Backend-Fehler im UI sichtbar:**  
  `readResponse()` wirft bei nicht erfolgreichen Antworten `payload.error`; `appendSplitEditor()` zeigt Fehler über `showError()` und setzt den Speichern-Status auf Fehler. Backend-Summenfehler werden als 400 mit konkreter Meldung geliefert.

- **Tests vorhanden:**  
  In `tests/test_dashboard.py` wird geprüft, dass Split-Daten in Transaktionsdetails zurückkommen und per PUT gespeichert werden können. Zusätzlich sichern Store-Tests in `tests/test_transactions.py` Atomarität und Tabellenstruktur ab.

### Backend/Persistenz

- `transaction_store.database.list_transaction_splits()` lädt Splits stabil nach `created_at, rowid`.
- `replace_transaction_splits()` ersetzt Split-Listen per Savepoint atomar.
- Nicht-leere Split-Listen müssen exakt dem Transaktionsbetrag entsprechen; bei Abweichung bleibt der alte Zustand erhalten.
- Leere Split-Listen entfernen vorhandene Splits vollständig.
- Positive und negative Transaktionsbeträge sind testseitig abgedeckt.

### Frontend/UI

- Der Split-Bereich wird dynamisch in der bestehenden Transaktionsdetailansicht ergänzt.
- Beträge werden als Euro-Werte angezeigt und als Centbeträge (`betrag_cent`) an das Backend gesendet.
- Originalbetrag, Split-Summe und Differenz werden sichtbar berechnet.
- Speichern wird bei nicht ausgeglichener nicht-leerer Split-Liste deaktiviert.
- Der bestehende Klassifikationseditor, Vorgangsanzeige und sonstige Detailbereiche bleiben im Codefluss erhalten.

## Auffälligkeit zum Diff

Der GitHub-Diff enthält keine Code- oder Teständerungen, sondern nur den Implementation-Report. Der Umsetzungsbericht behauptet entsprechend, dass die Funktionalität bereits im aktuellen Stand vorhanden war. Die nachgeladenen Dateien bestätigen diese Aussage hinreichend. Für die Merge-Wirkung bedeutet das: Der Branch liefert funktional keine Produktänderung gegenüber `main`, sofern `main` dem Compare entsprechend bereits denselben Code enthält.

## Nicht-blockierende Hinweise

1. **Betragsvalidierung im Frontend verbessern:**  
   `parseMinorAmount()` normalisiert ungültige Texte aktuell zu `0`. Das ist für offensichtliche Eingabefehler nicht ideal. Besser wäre eine explizite Fehlermeldung pro Zeile.

2. **Leere Zeilen behandeln:**  
   Komplett leere Split-Zeilen können insbesondere bei 0-Euro-Konstellationen gespeichert werden. Eine klare Client-Validierung oder ein bewusstes Ignorieren leerer Zeilen wäre nutzerfreundlicher.

3. **Ungültige `vorgangs_id` gezielter melden:**  
   Da die UI die Vorgangs-ID frei editierbar macht, sollte eine unbekannte ID idealerweise als 400/404 mit verständlicher Meldung zurückkommen statt über eine generische Serverfehlermeldung.

4. **Browser-Test für Split-Editor ergänzen:**  
   Die vorhandenen API-/Store-Tests decken die Kernfunktion ab. Ein zusätzlicher Browser-/DOM-Test für Hinzufügen, Entfernen und Speichern im Split-Editor wäre hilfreich.

## Schlussentscheidung

Keine blockierenden Probleme gefunden. Die fachlichen Akzeptanzkriterien sind im geladenen aktuellen Code erfüllt.
