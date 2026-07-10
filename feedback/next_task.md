# Nächstes Arbeitspaket

## Titel

Split-Klassifikationsfelder an bestehende Vorschlagsquellen anbinden

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 2

## Ziel

Im vorhandenen Split-Editor die Klassifikationsfelder je Split-Zeile mit denselben Datalist- und Vorschlagsmechanismen wie in der bestehenden Transaktionsklassifikation versorgen, ohne die Vorgangs- und Zuordnungsarchitektur zu ändern.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js
- banking_dashboard/server.py
- tests/test_dashboard.py
- banking_dashboard/static/index.html

## Muss umgesetzt werden

- Bestehende Vorschlagsquellen für Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre identifizieren und für Split-Zeilen wiederverwenden statt neue parallele Logik zu erfinden.
- Split-Eingabefelder im Frontend so anbinden, dass vorhandene Werte als Vorschläge erscheinen und abhängige Felder konsistent reagieren.
- Falls nötig einen bestehenden API- oder Hilfsdatenfluss für Vorschlagsdaten für den Split-Editor verfügbar machen, ohne neue fachliche Grundstruktur einzuführen.
- Tests ergänzen, die absichern, dass die Vorschlagsdaten für Split-Felder geliefert bzw. im UI verarbeitet werden.

## Soll umgesetzt werden

- Die Interaktion möglichst an das Verhalten der normalen Klassifikationsbearbeitung angleichen.
- Vorhandene Hilfsfunktionen für Datalist-Befüllung oder Kategorievorschläge konsolidiert wiederverwenden.

## Nicht Teil dieses Arbeitspakets

- Neue Split-Persistenz oder Änderungen am Datenmodell
- Mehrere Rechnungen pro Transaktion oder Teilrechnungs-Workflows
- Statuslogik für Splits außer bereits notwendiger kleiner UI-Anpassungen direkt für Vorschläge
- Neue direkte Beziehungen zwischen Transaktionen, Belegen oder anderen Entitäten außerhalb der Vorgangsarchitektur

## Akzeptanzkriterien

- Im Split-Editor bieten Transaktionstyp und Oberkategorie bestehende Werte als Vorschläge an.
- Unterkategorie und Sphäre verhalten sich im Split-Editor passend zur gewählten Kategoriekombination analog zur bestehenden Klassifikationsbearbeitung.
- Für die Vorschlagslogik des Split-Editors wird keine separate fachliche Parallelarchitektur eingeführt.
- Automatisierte Tests decken den bereitgestellten Vorschlagsdatenfluss oder das relevante UI-Verhalten ab.

## Hinweise für den Umsetzungs-Agenten

- Vorhandene Endpunkte, Server-Helfer und Frontend-Funktionen für Klassifikationsvorschläge bevorzugt erweitern statt neue Split-spezifische Strukturen einzuführen.
- Da Splits Teil des bekannten Epic sind, nur die Vorschlagsanbindung umsetzen und keine weitergehenden Split-Zuordnungsfälle vorziehen.
- Auf bestehende Terminologie und Feldnamen der Transaktionsklassifikation achten, damit spätere Split-Status- und Zuordnungslogik darauf aufbauen kann.

## Manuelle Testhinweise

- Split-Editor für eine Transaktion öffnen und prüfen, dass Vorschläge in den Klassifikationsfeldern erscheinen.
- Oberkategorie in einer Split-Zeile ändern und prüfen, dass Unterkategorie- und Sphäre-Vorschläge passend aktualisiert werden.
- Vergleichen, ob sich die Vorschlagslogik im Split-Editor konsistent zur normalen Transaktionsdetailbearbeitung verhält.

## Offene Fragen

- Ob die Split-UI bereits vollständig vorhanden ist oder nur punktuell erweitert werden muss.
- Ob bestehende Tests schon Split-spezifische Fixtures oder Hilfsroutinen enthalten, die wiederverwendet werden können.
