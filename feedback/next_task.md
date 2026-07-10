# Nächstes Arbeitspaket

## Titel

Split-Klassifikation und Statusableitung für Teilbeträge im Backend ergänzen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3

## Ziel

Die bestehende Split-Grundlage so erweitern, dass einzelne Teilbeträge eigene Klassifikationsfelder tragen, daraus ein konsistenter Split- und Transaktionsstatus abgeleitet wird und die Vorgangsarchitektur weiterhin über bestehende Vorgänge und Verknüpfungen genutzt wird.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/classification.py
- banking_dashboard/server.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/classification.py
- banking_dashboard/server.py
- tests/test_transactions.py

## Muss umgesetzt werden

- Bestehende Split-Datenstruktur um fachliche Klassifikationsfelder pro Split-Zeile ergänzen, ohne neue Grundarchitektur außerhalb der Vorgangslogik einzuführen.
- Regeln für die Statusableitung definieren und implementieren, mindestens für unklassifizierte, teilweise klassifizierte und vollständig klassifizierte Split-Konstellationen.
- Sicherstellen, dass sich der Gesamtstatus einer Transaktion mit Splits nachvollziehbar aus den Split-Zeilen ableitet.
- Vorhandene Klassifikationslogik so erweitern oder kapseln, dass sie Split-Zeilen fachlich gleichartig behandeln kann wie Transaktionen, soweit dies ohne UI-Großumbau möglich ist.
- API- oder Server-Ausgabe für Transaktionsdetails so ergänzen, dass Split-Klassifikation und abgeleitete Statuswerte vom Frontend konsumiert werden können.
- Automatisierte Tests für Persistenz, Statusableitung und API-Ausgabe ergänzen.

## Soll umgesetzt werden

- Bestehende Hilfsfunktionen zur Bestimmung des Klassifikationsstatus wiederverwenden oder verallgemeinern, um doppelte Logik zu vermeiden.
- Die Ableitungslogik so strukturieren, dass spätere Rechnungs- und Teilrechnungszuordnungen darauf aufbauen können.
- Wenn bereits Vorschlagslogik für Klassifikationsfelder existiert, Datenformate für Splits kompatibel halten.

## Nicht Teil dieses Arbeitspakets

- Großer Split-UI-Ausbau oder neuer Split-Editor-Flow im Frontend.
- Zuordnung mehrerer Rechnungen oder Teilrechnungen zu einer Transaktion.
- Neue direkte Beziehungen zwischen Belegen und Transaktionen außerhalb der bestehenden Vorgangs- und Verknüpfungsstrukturen.
- Mail-, Dokumenten- oder DFBnet-bezogene Erweiterungen.

## Akzeptanzkriterien

- Eine Split-Zeile kann eigene fachliche Klassifikationsfelder speichern oder im Modell transportieren.
- Für Transaktionen mit Splits wird ein konsistenter abgeleiteter Status zurückgegeben, der unklassifizierte, teilweise klassifizierte und vollständig klassifizierte Split-Zustände unterscheidet.
- Die Implementierung verwendet die bestehende Vorgangs-, Transaktions- und Klassifikationsarchitektur und führt keine neue fachliche Hauptstruktur ein.
- Bestehende Transaktionen ohne Splits verhalten sich unverändert.
- Tests decken mindestens einen vollständig klassifizierten, einen teilweise klassifizierten und einen unklassifizierten Split-Fall ab.

## Hinweise für den Umsetzungs-Agenten

- An bestehende Klassifikationsfelder und Statusbegriffe des Repos anlehnen statt neue fachliche Terminologie einzuführen.
- Falls die aktuelle Split-Grundlage noch in Detailfeldern uneinheitlich ist, nur die für Klassifikation und Status zwingend nötigen Modellergänzungen vornehmen.
- Statusableitung möglichst zentral im transaction_store halten und nicht verteilt in UI und API duplizieren.
- Vorgänge bleiben das zentrale fachliche Objekt; Split-Klassifikation darf spätere Vorgangslogik vorbereiten, aber keine direkte Ersatzstruktur schaffen.

## Manuelle Testhinweise

- Eine Transaktion mit mehreren Split-Zeilen laden und prüfen, ob die API für einzelne Splits Klassifikationsfelder und den abgeleiteten Gesamtstatus liefert.
- Einen Fall mit teils befüllten Split-Klassifikationen prüfen und sicherstellen, dass der Status nicht fälschlich als vollständig klassifiziert erscheint.
- Eine normale unsplittete Transaktion öffnen und prüfen, dass ihr bisheriges Verhalten unverändert bleibt.

## Offene Fragen

- Welche konkreten Split-Felder sind bereits im aktuellen Stand vorhanden und müssen nur erweitert statt neu angelegt werden?
- Soll der abgeleitete Status auf Transaktionsebene einen eigenen Split-bezogenen Wert erhalten oder bestehende Statuswerte wiederverwenden?
- Sollen automatische Klassifikationsregeln im ersten Schritt bereits auf Split-Zeilen anwendbar sein oder nur manuelle Split-Klassifikation unterstützt werden?
