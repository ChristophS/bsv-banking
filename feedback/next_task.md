# Nächstes Arbeitspaket

## Titel

Automatische Abschlussregeln wieder wirksam machen und Vorgangsstatus in der Transaktionsliste sichtbar anzeigen

## Ziel

Transaktionen sollen in der Transaktionsliste klar erkennen lassen, ob bereits Vorgänge verknüpft sind und ob diese abgeschlossen sind. Außerdem sollen aktive automatische Abschlussregeln beim Klassifizieren wieder dazu führen, dass der zugehörige Standard-Vorgang einer Transaktion automatisch auf abgeschlossen gesetzt wird, statt offen zu bleiben.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_dashboard.py
- tests/test_transactions.py
- transaction_store/rules.py
- transaction_store/classification.py
- transaction_store/database.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: list_transactions um Vorgangs- und Statusmetadaten für die Tabellenanzeige erweitern, damit pro Transaktion sichtbar wird, ob verknüpfte Vorgänge existieren und ob darunter abgeschlossene Vorgänge sind.
- banking_dashboard/static/app.js: Rendering der Transaktionsliste bzw. Zeilendetails um Tags oder Badges für 'Vorgang vorhanden' und 'abgeschlossen' ergänzen.
- transaction_store/rules.py: apply_completion_rules prüfen und so korrigieren, dass automatisch erzeugte Standard-Vorgänge pro Transaktion wieder abgeschlossen werden, wenn alle Voraussetzungen und eine aktive Abschlussregel erfüllt sind.
- transaction_store/classification.py: prüfen, ob nach automatischer Klassifikation der Abschlussregel-Lauf zuverlässig ausgelöst wird oder ob bestehende Sperrlogik das verhindert.
- transaction_store/database.py: nur prüfen, ob Schema- oder Hilfslogik für Standard-Vorgänge oder status_manuell den automatischen Abschluss unerwartet blockiert.

## Muss umgesetzt werden

- Die Ursache beheben, warum aktive automatische Abschlussregeln derzeit nicht mehr dazu führen, dass der zugehörige Transaktions-Vorgang automatisch abgeschlossen wird.
- Sicherstellen, dass bei einer Transaktion mit passender automatischer Abschlussregel der bestehende bzw. standardmäßig erzeugte Vorgang auf abgeschlossen gesetzt wird, ohne dass manuell eingegriffen werden muss.
- Dabei respektieren, dass manuell gesetzte Vorgangsstatus laut bestehender Logik nicht ungewollt überschrieben werden dürfen.
- Die Transaktionslisten-API um klare, leichte Statusinformationen erweitern, zum Beispiel Anzahl verknüpfter Vorgänge, ob mindestens ein Vorgang existiert und ob mindestens ein verknüpfter Vorgang abgeschlossen ist.
- Im Frontend der Transaktionsliste sichtbare Tags oder Badges ergänzen, damit pro Transaktion erkennbar ist, ob schon ein Vorgang angelegt oder verknüpft wurde und ob ein Vorgang abgeschlossen ist.

## Soll umgesetzt werden

- Falls mehrere Vorgänge an einer Transaktion hängen, die UI-Kennzeichnung so wählen, dass sie nicht fälschlich 'erledigt' signalisiert, wenn nur ein Teil abgeschlossen ist; mindestens zwischen 'verknüpft' und 'abgeschlossen vorhanden' unterscheiden.
- Die neuen API-Felder so benennen, dass sie auch für spätere Mehrfachverknüpfungen brauchbar bleiben.
- Falls vorhanden, die Detailansicht oder Tooltip-Nutzung in app.js mit Vorgangs-IDs oder kurzer Statuszahl ergänzen, aber nur wenn das ohne größeren Umbau möglich ist.

## Nicht Teil dieses Arbeitspakets

- Allgemeine Sortierung der Vorgangsliste im Dashboard aus dem bisherigen next_task
- Neue Sortier- oder Filteroptionen in der Transaktionsliste
- Großer Umbau der Regelverwaltung
- Neue Fachlogik für Fehlbuchungen
- Mail-, Beleg- oder To-Do-Importverbesserungen aus dem Backlog

## Akzeptanzkriterien

- Wenn eine Transaktion nach Klassifikation alle Abschlussvoraussetzungen erfüllt und auf mindestens eine aktive Abschlussregel passt, ist ihr zugehöriger Standard-Vorgang danach automatisch im Status abgeschlossen.
- Bestehende manuelle Statussperren bleiben erhalten; ein manuell gesetzter Status wird nicht unbeabsichtigt durch die Automatik überschrieben.
- GET /api/transactions liefert pro Transaktion zusätzliche repo-konkrete Vorgangsstatusinformationen, aus denen die UI die Kennzeichnung ableiten kann.
- In der Transaktionsliste ist ohne Öffnen der Detailansicht sichtbar, ob zu einer Transaktion bereits ein Vorgang existiert und ob ein verknüpfter Vorgang abgeschlossen ist.
- Der bestehende Filter hide_completed_vorgaenge funktioniert weiterhin unverändert.

## Hinweise für den Umsetzungs-Agenten

- In list_transactions werden aktuell nur reine Transaktionsfelder selektiert. Für die Tags dürfte eine aggregierte LEFT-JOIN- oder Subquery-Lösung auf transaktion_vorgaenge und vorgaenge am stabilsten sein.
- Da die Fachlichkeit Mehrfachzuordnungen erlaubt, sollte die API nicht nur ein einzelnes status-Feld zurückgeben, sondern aggregierte Informationen wie has_vorgaenge, has_completed_vorgaenge oder vorgaenge_count.
- update_transaction_classification ruft apply_completion_rules bereits auf; wenn die Automatik trotzdem nicht greift, liegt die Ursache wahrscheinlich in apply_completion_rules selbst oder in Voraussetzungen rund um status_manuell, Zielmengenauswahl oder Regelmatch nach Wegfall der früheren harten Kopplung.
- Besonders prüfen: ob apply_completion_rules nur bereits gruppierte Mehrfachvorgänge betrachtet, Standard-Vorgänge einer Einzeltransaktion übersieht oder wegen fehlender oder zu strenger Bedingung nicht aktualisiert wird.
- Die UI-Anforderung sagt 'Tags oder so'. Das spricht für eine kleine bestehende Tabellen- oder Badge-Erweiterung in app.js, nicht für ein neues Panel oder einen neuen Dialog.

## Manuelle Testhinweise

- Eine Transaktion auswählen, die auf eine aktive Abschlussregel passt, Klassifikation setzen beziehungsweise Regel anwenden und prüfen, dass der verknüpfte Vorgang danach automatisch abgeschlossen ist.
- Im Reiter Transaktionen prüfen, dass die betroffene Zeile einen sichtbaren Hinweis auf vorhandenen oder verknüpften und abgeschlossenen Vorgang zeigt.
- Eine Transaktion mit verknüpftem offenem Vorgang prüfen: Kennzeichnung muss sichtbar sein, aber nicht als abgeschlossen erscheinen.
- Eine Transaktion mit mehreren Vorgängen prüfen, falls im Testbestand möglich.
- Filter hide_completed_vorgaenge in der Transaktionsansicht prüfen, damit vollständig erledigte Transaktionen weiterhin korrekt ausgeblendet werden.

## Offene Fragen

- Falls eine Transaktion mehreren Vorgängen zugeordnet ist: Soll die Liste bereits bei 'mindestens ein abgeschlossener Vorgang' ein Abschluss-Tag zeigen, oder nur wenn kein offener Vorgang mehr verknüpft ist? Für dieses kleine Paket möglichst an bestehender hide_completed_vorgaenge-Semantik orientieren.
- Unklar ist ohne Umsetzungstest, ob der Fehler nur bei neu klassifizierten Transaktionen auftritt oder auch beim Anlegen oder Ändern einer Abschlussregel mit apply_now.
