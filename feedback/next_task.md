# Nächstes Arbeitspaket

## Titel

Overview-Routing gegen ungewöhnliche card.key/entity-Werte absichern

## Ziel

Die Karten-Navigation im Dashboard soll unbekannte oder ungewöhnliche Overview-Werte robust behandeln, ohne über geerbte Objekteigenschaften fehlzurouten oder Laufzeitfehler zu erzeugen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: zentrale Mapping-Tabellen oder Dispatch-Logik für Klicks auf Overview-Karten gegen prototype-basierte Lookups absichern.
- banking_dashboard/static/app.js: Fallback-Verhalten für unbekannte card.key/entity ergänzen, damit nichts crasht und keine falsche Ansicht geöffnet wird.
- tests/test_dashboard.py: gezielte Regressionstests für unbekannte Karten-Keys/Entities ergänzen.

## Muss umgesetzt werden

- Die bestehende Mapping-/Routing-Logik in app.js identifizieren, die Overview-Karten anhand von card.key oder entity auf Tabs, Filter oder Aktionen abbildet.
- Lookup-Zugriffe so absichern, dass geerbte Eigenschaften wie __proto__, constructor oder toString nicht als gültige Treffer behandelt werden.
- Falls plain objects als Lookup-Tabellen genutzt werden, entweder prototype-lose Objekte verwenden oder den Zugriff mit Object.hasOwn absichern.
- Für unbekannte Schlüssel ein sicheres Fallback beibehalten oder ergänzen: kein Crash, keine Fehlroute, keine Ausnahme im UI.
- Tests ergänzen, die explizit ungewöhnliche oder unbekannte Werte abdecken und die Regression verhindern.

## Soll umgesetzt werden

- Falls mehrere ähnliche Mapping-Tabellen für Overview-Karten existieren, die Absicherung konsistent an allen relevanten Stellen anwenden.
- Falls im UI bereits eine neutrale Fehler-/No-op-Behandlung existiert, diese statt neuer Meldungen wiederverwenden.

## Nicht Teil dieses Arbeitspakets

- Spezifischere Terminfilter für anstehende und nicht zugewiesene Termine
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen
- Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration
- Allgemeines Refactoring der gesamten Dashboard-Navigation ohne konkreten Sicherheits-/Robustheitsbezug

## Akzeptanzkriterien

- Klicks oder Routing-Entscheidungen für bekannte Overview-Karten funktionieren weiterhin unverändert.
- Ungewöhnliche Werte wie __proto__, constructor oder andere nicht explizit definierte card.key-/entity-Werte werden nicht als gültige Mapping-Treffer behandelt.
- Das Frontend produziert bei unbekannten Kartenwerten keinen Laufzeitfehler und landet nicht in einer falschen Ansicht.
- Automatisierte Tests decken mindestens einen unbekannten key und einen ungewöhnlichen Lookup-Wert ab.

## Hinweise für den Umsetzungs-Agenten

- README und server.py zeigen, dass overview_counts() bekannte Cards mit key/entity liefert; der relevante Punkt liegt damit sehr wahrscheinlich in der clientseitigen Karten-Dispatch-Logik in static/app.js.
- Wenn es bereits Konstanten oder Objektliterale für card.key -> Aktion bzw. entity -> Zielansicht gibt, dort gezielt härten statt Logik zu verstreuen.
- Falls Tests in test_dashboard.py Frontend-Verhalten über HTML/JS nicht direkt prüfen, kann alternativ die JS-nahe Entscheidungslogik in eine testbare Hilfsfunktion extrahiert werden, aber nur wenn das zur bestehenden Struktur passt.

## Manuelle Testhinweise

- Dashboard starten und prüfen, dass alle vorhandenen Overview-Karten weiterhin in die erwarteten Bereiche führen.
- Testweise im Browser mit manipulierten Overview-Daten bzw. per kleiner isolierter Funktion prüfen, dass ein unbekannter key/entity keine falsche Navigation auslöst.
- Besonders Werte wie __proto__ und constructor gegen die Routing-Logik prüfen.

## Offene Fragen

- Ob das bestehende Routing primär über card.key, über entity oder über eine Kombination aus beiden läuft, muss der Umsetzungs-Agent direkt in app.js an der konkreten Stelle verifizieren.
- Ob test_dashboard.py bereits Hilfsmuster für JS-bezogene Regressionen enthält oder ob der Test eher servernah formuliert werden muss.
