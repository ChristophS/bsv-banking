# Nächstes Arbeitspaket

## Titel

Mail-Sofortabschluss mit Persistenzprüfung im Test absichern

## Ziel

Einen gezielten Test ergänzen, der beim Mail-Vorgang-Import mit angefordertem Sofortabschluss den Fehlerfall absichert und danach explizit prüft, dass der bereits persistierte Vorgang weiterhin geladen werden kann und nicht abgeschlossen ist.

## Relevante Dateien

- tests/test_dashboard.py
- banking_dashboard/server.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- tests/test_dashboard.py: bestehenden oder neuen Test für POST /api/mail/<inbox_id>/vorgang-import mit completed=true und blockiertem Abschluss ergänzen
- banking_dashboard/server.py: nur falls nötig prüfen, ob der Import-Endpunkt im Fehlerfall eine eindeutige Re-Load-Prüfung im Test benötigt

## Muss umgesetzt werden

- Einen automatisierten Test ergänzen, der einen Mail-Vorgang-Import mit requested completed=true ausführt, obwohl die Abschlussvoraussetzungen nicht erfüllt sind.
- Im Test sicherstellen, dass der Request den Fehlerfall auslöst, der Vorgang aber trotzdem persistiert wurde.
- Den persistierten Vorgang nach dem fehlgeschlagenen Sofortabschluss explizit erneut laden und prüfen, dass sein Status nicht 'abgeschlossen' ist.
- Wenn möglich, konkret auf den Status 'in_bearbeitung' prüfen; andernfalls mindestens auf 'nicht abgeschlossen'.

## Soll umgesetzt werden

- Zusätzlich prüfen, dass kein versehentlich abgeschlossener manueller Status gesetzt wurde, falls das im Detail leicht verfügbar ist.
- Falls bestehende Fixtures es hergeben, auch sichtbar machen, dass die Abschlussblockade aus den unvollständigen Daten resultiert.

## Nicht Teil dieses Arbeitspakets

- Generischer Ein-Klick-Workflow für manuelle Vorgangserstellung, Klassifikation und Abschluss
- Mehrfachzuordnung mehrerer Mail-Dokumente auf unterschiedliche Transaktionen
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Integration
- Allgemeine Dashboard-Usability-Überarbeitung
- Größere Änderungen am Mail-Import-Verhalten jenseits dieser gezielten Test-Absicherung

## Akzeptanzkriterien

- Es existiert ein automatisierter Test, der den fehlgeschlagenen Sofortabschluss beim Mail-Import abdeckt.
- Der Test weist explizit nach, dass der persistierte Vorgang nach dem Fehlerfall erneut geladen werden kann.
- Der Test prüft explizit, dass dieser persistierte Vorgang nicht den Status 'abgeschlossen' hat.
- Die bestehenden Dashboard-Tests laufen weiterhin erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Der relevante Ablauf im Mail-Import ist bereits: create_vorgang(... completed=False) -> optional update_vorgang_status(..., True). Genau daraus ergibt sich der gewünschte Fehlerfall: Anlage erfolgreich, Abschluss scheitert.
- Die Abschlussprüfung ist zentral in DashboardDataStore.update_vorgang_status(...) und den Hilfsfunktionen _vorgang_completion_requirements(...) / _vorgang_completion_error(...) gekapselt; diese Logik soll nicht neu gebaut werden.
- Für den Test ist ein Vorgang ohne ausreichende Abschlussvoraussetzungen wahrscheinlich am stabilsten, z. B. mit fehlender oder unvollständiger Transaktionsklassifikation oder ohne erforderliche Verknüpfungen.
- Wenn der Endpoint bei gescheitertem update_vorgang_status einen Fehler nach außen gibt, ist das in Ordnung; wichtig ist die zusätzliche Persistenzprüfung im Test danach.

## Manuelle Testhinweise

- Optional lokal einen Mail-Import mit aktiviertem Sofortabschluss starten, obwohl die Abschlussvoraussetzungen fehlen.
- Danach prüfen, dass der Vorgang im Dashboard vorhanden ist, aber nicht als abgeschlossen erscheint.

## Offene Fragen

- Welcher bestehende Testfall oder welche Fixture in tests/test_dashboard.py eignet sich am besten, um den bereits angelegten Vorgang nach einem Fehler eindeutig wiederzufinden?
- Soll der Test auf den exakten Status 'in_bearbeitung' prüfen oder bewusst nur auf 'nicht abgeschlossen', falls künftig weitere Statusvarianten denkbar sind?
