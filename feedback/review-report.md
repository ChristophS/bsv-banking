# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die Nachbesserung ist fachlich stimmig, der Diff belegt nun den geforderten Dashboard-API-/UI-Flow, und der nachgeladene Kontext zeigt, dass der Split-Editor bereits vorhanden war und nun seriös um Laden, explizites Neuladen, Summenbezug zur Originaltransaktion und passende Tests ergänzt wurde.

## Zusammenfassung

Der bestehende Dashboard-Split-Editor wurde korrekt an einen expliziten Lese-/Speicher-API-Flow für bestehende Splits angebunden, serverseitige Summenvalidierung verbessert und durch API- sowie browsernahe Tests abgesichert. Keine Architekturverletzung erkennbar.

# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Kurzfazit

Die Umsetzung kann akzeptiert werden. Der vorliegende Compare belegt jetzt nachvollziehbar den geforderten Dashboard-Split-Flow für bestehende Transaktions-Splits: Laden über einen dedizierten GET-Endpunkt, Bearbeiten im bestehenden Detailbereich, Speichern über den PUT-Endpunkt, serverseitige Summenvalidierung und ergänzte Tests für API- und UI-nahes Verhalten.

## Prüfung gegen das Arbeitspaket

### 1. Nutzung bestehender Split-Persistenz / Architektur

Erfüllt.

- Im nachgeladenen Kontext ist der Split-Editor bereits als Teil des bestehenden Transaktions-Detailflows in `banking_dashboard/static/app.js` vorhanden.
- Gespeichert wird weiterhin über `replace_transaction_splits(...)` und damit über bestehende `transaction_store`-Strukturen.
- Es wurde keine neue Parallelarchitektur für Splits eingeführt.
- Es wurden keine neuen Grundbeziehungen zu Belegen, Rechnungen oder anderen Entitäten eingeführt.

Das entspricht den Architekturvorgaben des Arbeitspakets.

### 2. Kleiner API-Flow in `server.py` zum Lesen und Speichern

Erfüllt.

- Der bestehende GET-Endpunkt `/api/transactions/{id}/splits` wird im Diff sinnvoll erweitert:
  - `amount_minor`
  - `betrag_cent`
  - `betrag`
- Der PUT-Endpunkt `/api/transactions/{id}/splits` war bereits vorhanden und bleibt die Speicherschnittstelle.
- Im Kontext ist klar sichtbar, dass beide Endpunkte im Dashboard-Server korrekt verdrahtet sind.

Wichtig: Durch die GET-Erweiterung ist der Soll-Zustand „vorhandene Split-Zeilen einer Transaktion laden“ im Dashboard-API-Flow jetzt explizit belegbar.

### 3. Split-Editor im Transaktions-Detailbereich

Erfüllt.

Der Kontext zeigt, dass der Editor bereits im Transaktionsdetail existierte. Die jetzt eingecheckte Nachbesserung macht den geforderten Flow explizit und überprüfbar:

- Anzeige und Bearbeitung mehrerer Split-Zeilen ist vorhanden.
- Hinzufügen und Entfernen von Zeilen ist vorhanden.
- Neu hinzugefügt wurde ein expliziter Button **„Splits neu laden“**, der den GET-Endpunkt aufruft.
- Das bleibt innerhalb des bestehenden Detaildialogs; es wurde kein neuer Navigationsflow gebaut.
- `index.html` enthält nun einen klaren statischen Host-Marker am bestehenden Detail-Content-Container.

Damit sind die UI-bezogenen Akzeptanzkriterien erfüllt.

### 4. Summenvalidierung gegen den Originalbetrag

Erfüllt.

- Clientseitig existiert im Kontext bereits eine Summenprüfung im Editor (`updateSummary`, Differenz zum Originalbetrag, Disabled-State bei Betragsformatfehlern).
- Serverseitig validiert weiterhin `replace_transaction_splits(...)` gegen `transaction.amount_minor`.
- Der Diff verbessert die serverseitige Fehlermeldung deutlich um:
  - Erwartungswert
  - tatsächliche Split-Summe
  - Differenz

Das erfüllt die Forderung, ungültige Split-Summen zu verhindern oder klar abzuweisen. Die serverseitige Prüfung ist hier besonders wichtig und vorhanden.

### 5. Tests für Laden, Speichern und Validierungsfehler

Erfüllt.

Im Diff und im nachgeladenen Testkontext sind die geforderten Nachweise vorhanden:

- API-Test prüft den GET-/splits-Endpunkt und die zusätzlichen Betragsfelder.
- API-Test prüft weiterhin PUT-Speichern.
- API-Test prüft den 400-Fehler bei falscher Split-Summe.
- API-Test prüft, dass nach Fehler keine Teilpersistenz entstanden ist.
- Browsernaher Test prüft den Split-Editor inklusive:
  - Sichtbarkeit im Detaildialog
  - Bearbeiten
  - Hinzufügen
  - Entfernen
  - Speichern
  - Validierungsfehler
  - explizites Neuladen über GET `/api/transactions/tx_newer/splits`

Damit sind die Test-Akzeptanzkriterien ausreichend abgedeckt.

## Abgleich mit dem Implementation Report

Der Report ist im Wesentlichen konsistent mit dem Diff und dem nachgeladenen Kontext:

- Explizites Neuladen über GET-Endpunkt: belegt.
- Zusätzliche Originalbetragsfelder im Split-GET: belegt.
- Konkretisierte Fehlermeldung bei falscher Split-Summe: belegt.
- API- und UI-nahe Tests: belegt.

Es gibt keinen wesentlichen Widerspruch zwischen Report und tatsächlicher Änderung.

## Auffälligkeiten / Hinweise

### Zusätzliche Änderung in `transaction_store/database.py`

Im GitHub-Compare ist zusätzlich `transaction_store/database.py` enthalten und verbessert die Fehlermeldung der Summenvalidierung. Das ist fachlich passend und kein Scope-Creep-Problem, obwohl es gegenüber den Runner-Daten als Zusatz auffällt.

### Bereits vorhandener Split-Editor im Kontext

Der nachgeladene Kontext zeigt, dass ein großer Teil des Split-Editors schon vor dieser Nachbesserung vorhanden war. Für dieses Arbeitspaket ist das okay: Bewertet wird die tatsächlich eingecheckte Nachbesserung gegen das Soll. Diese Nachbesserung schließt genau die im vorherigen Review fehlende Belegbarkeit des Dashboard-API-/UI-Flows.

## Nicht-blockierende Vorschläge

- Die GET-Antwort für Splits enthält mit `amount_minor` und `betrag_cent` zwei semantisch gleiche Cent-Felder; mittelfristig wäre eine API-Vereinheitlichung sinnvoll.
- Der Prozess um Runner/GitHub-Compare sollte künftig sauberer sein, damit zusätzliche Dateien wie `transaction_store/database.py` nicht als Compare-Abweichung auftauchen.

## Schlussentscheidung

Die Umsetzung erfüllt das Arbeitspaket fachlich und technisch. Insbesondere sind jetzt alle wesentlichen Akzeptanzkriterien im maßgeblichen Diff und im Kontext nachvollziehbar belegt.
