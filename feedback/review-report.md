# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die nachgeladenen vollständigen Dateien bestätigen, dass der Split-Editor ausschließlich die bereits über /api/classification-options geladenen state.classificationOptions verwendet, Klassifikationswerte im bestehenden Split-Payload überträgt und die Änderungen die geforderten Abhängigkeiten sowie den Schutz manueller Sphären korrekt ergänzen.

## Zusammenfassung

Akzeptiert: Der Split-Editor nutzt die bestehende Klassifikationsquelle, deaktiviert Unterkategorien ohne Oberkategorie, filtert Vorschläge nach Oberkategorie und überschreibt eine vorhandene/manuelle Sphäre nicht mehr. Nicht mehr angebotene gespeicherte Sphären bleiben sichtbar und im unveränderten Split-Payload erhaltbar. Der erweiterte Browser-Flow deckt Kategorienabhängigkeit, manuelle Sphäre und Persistenz ab.

# Review Report

## Ergebnis

**Accepted:** ja

## Geprüfte Umsetzung

- `banking_dashboard/static/app.js`
- `tests/test_dashboard.py`
- GitHub-Compare-Diff zum Commit `4631a68bcd2ee03c7cadd6eadec234302e4f8452`

## Bewertung

Die Implementierung erfüllt die Anforderungen des Arbeitspakets:

- Der Split-Editor verwendet weiterhin ausschließlich `state.classificationOptions`. Diese werden beim Laden des Transaktions-Workspaces über den bestehenden Endpunkt `GET /api/classification-options` bezogen; es wurde keine zweite Kategorienquelle eingeführt.
- Jede Split-Zeile erzeugt Datalists für Transaktionstyp und Oberkategorie aus den vorhandenen Optionen.
- Die Unterkategorie wird beim Initialisieren und bei Änderungen der Oberkategorie deaktiviert, solange keine Oberkategorie befüllt ist. Bei befüllter Oberkategorie wird ihre Datalist ausschließlich mit den zugeordneten Unterkategorien aufgebaut. Freie Texteingaben bleiben möglich.
- Die Sphären-Vorauswahl wird nur vorgenommen, wenn die Split-Zeile noch keine Sphäre besitzt. Damit bleiben gespeicherte und manuell gesetzte Sphären bei Kategorieänderungen erhalten.
- `splitSphereField(...)` ergänzt einen gespeicherten Sphärenwert, der nicht mehr in den aktuellen Optionen vorkommt, als auswählbare Option. Der Wert bleibt dadurch sichtbar und wird beim bestehenden PUT-Payload erneut übertragen.
- Der bestehende Persistenzweg `PUT /api/transactions/<id>/splits` und das Split-Datenmodell bleiben unverändert. `readRows()` übernimmt alle Klassifikationsfelder, und `renderRows()` rendert die vom Server zurückgegebenen Werte wieder in derselben Reihenfolge.
- Der ergänzte Playwright-Flow prüft das Deaktivieren/Aktivieren der Unterkategorie, die gefilterte Vorschlagsliste, den Schutz einer manuell gesetzten Sphäre und deren Persistenz im abgerufenen Split-Ergebnis.

## Tests

Laut Umsetzungsbericht wurde `tests/test_dashboard.py` mit **105 bestanden, 6 übersprungen** ausgeführt. Die übersprungenen Tests benötigen optional Playwright/Chromium; die Erweiterung ist in den bestehenden Browser-Test integriert und benötigt weder Bankzugang noch externe Dienste.

## Hinweis

`banking_dashboard/static/app.js` erscheint in GitHub Compare, obwohl sie nicht in den vom Runner gestagten beziehungsweise validierten Pfaden auftaucht. Der GitHub-Compare-Diff ist für die Review maßgeblich; die geänderten Stellen wurden anhand der nachgeladenen vollständigen Datei geprüft und sind fachlich konsistent.
