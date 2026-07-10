# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der Diff ist für die fachliche Prüfung ausreichend und erfüllt die Anforderungen ohne erkennbare blockierende Probleme.

## Zusammenfassung

Die Umsetzung ersetzt die missverständliche Beschriftung, ergänzt eine obere und untere Aktionsleiste mit identischer Submit-Logik, aktualisiert die Button-Texte live abhängig vom Abschluss-Häkchen und lässt den bestehenden Import-Payload einschließlich completed unverändert. Der Branch ist sauber vergleichbar und die ergänzten Tests decken die zentrale UI-Logik ab.

## Review-Ergebnis

**Accepted:** Ja

## Geprüfte Anforderungen

- Die alte Beschriftung `Bestätigt importieren` wurde aus dem Mail-Vorgang-Import entfernt.
- Die primäre Aktion wird abhängig vom Zustand von `vorgang_completed` beschriftet:
  - ohne Abschluss: `Vorgang anlegen`
  - mit Abschluss: `Vorgang abschließen`
- Es gibt nun zwei Aktionsleisten im Formular, oben und unten, beide mit Submit-Buttons derselben Formular-Submit-Logik.
- Die obere Aktionsleiste ist zusätzlich als sticky Bereich gestaltet und damit besser erreichbar.
- Die Beschriftung wird bei Änderung des Abschluss-Häkchens live über `updateMailVorgangImportActions(form)` aktualisiert.
- Der bestehende Request-Flow bleibt erhalten: `submitMailVorgangImport` verwendet weiterhin das Formular und damit den bestehenden Payload-Aufbau über `readMailVorgangReviewForm(form)`, einschließlich `completed` aus `form.elements.vorgang_completed.checked`.
- Sekundäre Aktionen bleiben als `secondary-action` optisch und strukturell von der primären Aktion getrennt.

## Technische Bewertung

Die Änderung ist gezielt frontendseitig umgesetzt und greift nicht in Backend-Validierung, Import-Fachlogik oder andere Mail-Aktionen ein. Die Einführung von `createMailVorgangImportActions`, `mailVorgangImportSubmitLabel` und `updateMailVorgangImportActions` ist nachvollziehbar und vermeidet doppelte Submit-Implementierungen. Beim Absenden werden beide Submit-Buttons deaktiviert und bei Fehlern wieder freigegeben; Statusanzeigen werden ebenfalls für beide Aktionsleisten aktualisiert.

Die CSS-Erweiterung ist auf `.mail-vorgang-import-actions` beschränkt und verursacht keinen offensichtlichen Scope Creep.

## Tests

Der ergänzte Test in `tests/test_dashboard.py` prüft die zentralen Akzeptanzkriterien sinnvoll:

- zwei Aktionsleisten vorhanden,
- initiale Labels `Vorgang anlegen`,
- Live-Wechsel auf `Vorgang abschließen`,
- `completed` wird weiterhin aus dem Formular übernommen,
- alte Beschriftung ist nicht mehr vorhanden.

Laut Implementation Report wurden `tests/test_dashboard.py` und `node --check banking_dashboard/static/app.js` erfolgreich ausgeführt.

## Blockierende Probleme

Keine.

## Nicht-blockierende Hinweise

- Die tatsächliche visuelle/sticky Erreichbarkeit ist nicht per Screenshot-Test abgesichert, aber durch die obere Aktionsleiste und CSS plausibel erfüllt.
- Da der Browser-Test bei fehlendem Playwright/Chromium übersprungen wird, könnte eine zusätzliche leichtere DOM-/JS-Absicherung die Regressionserkennung verbessern, ist aber für dieses Arbeitspaket nicht zwingend.
