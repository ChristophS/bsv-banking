# Nächstes Arbeitspaket

## Titel

Direktabschluss im Mail-Vorgang-Import um Inline-Klassifikation verknüpfter Transaktionen erweitern

## Ziel

Im bestehenden Mail-Vorgang-Import sollen verknüpfte Transaktionen direkt mit Klassifikationswerten mitgeschickt und gespeichert werden, bevor der optionale Direktabschluss gegen die vorhandenen Abschlussregeln geprüft wird.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: _mail_vorgang_import(...) um die Annahme und Verarbeitung eines optionalen Klassifikations-Blocks für referenzierte transaction_ids erweitern; erst speichern, dann optionalen Direktabschluss auslösen.
- banking_dashboard/static/app.js: Mail-Import-Dialog so erweitern, dass für verknüpfte Transaktionen bearbeitbare Klassifikationsfelder angezeigt und im Request mitgesendet werden.
- banking_dashboard/static/index.html: nur falls nötig Container/Markup für den zusätzlichen Klassifikationsbereich im Mail-Import ergänzen.
- tests/test_dashboard.py: API-Tests für den erweiterten Import-Request und das Verhalten bei Direktabschluss nach Inline-Klassifikation ergänzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Vorgang-Import ein optionales Feld für transaktionsbezogene Klassifikationswerte unterstützen, eindeutig referenziert über transaction_id.
- Vor einem angeforderten Direktabschluss alle mitgesendeten Klassifikationswerte für die betreffenden verknüpften Transaktionen über die vorhandene Store-Logik speichern.
- Danach den Direktabschluss erneut gegen die bestehenden Abschlussbedingungen prüfen und nur bei vollständigen Pflichtfeldern erfolgreich abschließen.
- Im Import-Response transparent zurückgeben, ob der Direktabschluss geklappt hat oder wegen unvollständiger/ungültiger Klassifikation abgelehnt wurde.
- Validierungsfehler pro Request sauber behandeln, damit keine stillen Teilzustände entstehen.

## Soll umgesetzt werden

- Im UI vorhandene Transaktionsdaten wie Zahlungsbeteiligter, Verwendungszweck und Betrag neben den Eingabefeldern anzeigen.
- Bereits vorhandene Klassifikationswerte vorbefüllen, falls die verknüpfte Transaktion teilweise oder vollständig klassifiziert ist.
- Die direkte Abschlussmeldung im UI konkret formulieren, z. B. mit Hinweis auf noch unvollständige Transaktionen.

## Nicht Teil dieses Arbeitspakets

- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Neue automatische Vorschlagslogik oder KI-Klassifikation für Transaktionsparameter.
- Große Überarbeitung des gesamten Vorgang-Erstellflows außerhalb des Mail-Imports.
- Spendenbescheinigungen/Adressdatenbank/DFBnet-Verein-Integration.
- Allgemeine Dashboard-Usability-Überarbeitung.

## Akzeptanzkriterien

- Beim Mail-Vorgang-Import kann der Client für verknüpfte Transaktionen Klassifikationsfelder mitsenden, ohne einen separaten Nachbearbeitungsschritt in der Transaktions- oder Vorgangsdetailansicht zu benötigen.
- Werden alle Pflichtfelder der relevanten Transaktionen im Import korrekt gesetzt und ist Direktabschluss angefordert, wird der erzeugte Vorgang direkt auf abgeschlossen gesetzt.
- Fehlen nach dem Import bei mindestens einer verknüpften Transaktion Pflichtfelder, bleibt der Vorgang offen und die Antwort enthält eine verständliche Ablehnungsnachricht aus der bestehenden Abschlusslogik.
- Bestehendes Verhalten ohne mitgesendete Inline-Klassifikation bleibt unverändert.
- Die Klassifikationswerte werden in den bestehenden Transaktionsfeldern gespeichert und sind anschließend in Vorgangs-/Transaktionsdetails sichtbar.

## Hinweise für den Umsetzungs-Agenten

- Naheliegend ist eine Request-Erweiterung in _mail_vorgang_import(...) um ein zusätzliches Array/Dikt für transaction classifications; dabei erst Vorgang anlegen/verknüpfen, dann Klassifikationen auf die referenzierten transaction_ids anwenden, dann optional update_vorgang_status(..., True) aufrufen.
- Da update_transaction_classification(...) bereits apply_completion_rules(...) ausführt, sollte keine zweite Abschlussregel-Auswertung im Import gebaut werden; stattdessen die vorhandene Reihenfolge bewusst nutzen.
- Die UI sollte möglichst dieselben Feldnamen verwenden wie der PATCH-Endpoint /api/transactions/<id>/classification, damit keine unnötige Übersetzungslogik entsteht.
- Wenn Transaktionen im Import verknüpft werden, sollte das UI nur diese Transaktionen inline bearbeitbar machen, nicht den gesamten Transaktionsbestand.
- Falls der Import mehrere Transaktionen enthält, sollte der Direktabschluss erst nach Verarbeitung aller Klassifikationsupdates versucht werden.

## Manuelle Testhinweise

- Mail im Dashboard öffnen, Vorgang-Import starten, mindestens eine verknüpfte unklassifizierte Transaktion auswählen, alle Pflichtfelder im Import setzen und Direktabschluss aktivieren: Erwartung = Vorgang wird erstellt und direkt abgeschlossen.
- Gleicher Test mit absichtlich fehlender Unterkategorie oder Sphäre: Erwartung = Vorgang wird erstellt, bleibt aber in_bearbeitung und zeigt verständlichen Blocker.
- Test ohne Inline-Klassifikation wie bisher ausführen: Erwartung = bisheriges Verhalten unverändert.
- Nach erfolgreichem Import erzeugten Vorgang und die verknüpften Transaktionen öffnen und prüfen, dass die gespeicherten Klassifikationswerte sichtbar sind.

## Offene Fragen

- Welches genaue Request-Format ist im aktuellen Frontend für links.transaction_ids im Mail-Import bereits etabliert, und an welcher UI-Stelle werden diese Transaktionen aktuell ausgewählt?
- Soll die Inline-Klassifikation im UI nur für explizit ausgewählte transaction_ids erscheinen oder für alle vorgeschlagen/verknüpften Transaktionen im Importdialog?
