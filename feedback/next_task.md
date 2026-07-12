# Nächstes Arbeitspaket

## Titel

To-Do-API auf konsistente Eingabevalidierung und Fehlerantworten absichern

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.1

## Ziel

Die bestehenden To-Do-Endpunkte sollen für typische ungültige Eingaben und fehlende Ressourcen konsistente, überprüfbare HTTP-Fehlerantworten liefern, ohne das bestehende Vorgangs- und Verknüpfungsmodell zu verändern.

## Relevante Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- DashboardDataStore.create_todo
- DashboardDataStore.update_todo
- DashboardDataStore.delete_todo
- DashboardRequestHandler.do_POST
- DashboardRequestHandler.do_PATCH
- DashboardRequestHandler.do_DELETE
- Dashboard-API-Tests für /api/todos

## Muss umgesetzt werden

- Die bestehenden POST-, PATCH- und DELETE-Flows für /api/todos anhand der vorhandenen Validierungs- und Fehlerbehandlung prüfen.
- Für ungültige Payloads, nicht vorhandene To-Do-IDs und ungültige Vorgangsreferenzen konsistente HTTP-Statuscodes und JSON-Fehlerantworten sicherstellen.
- Regressionstests mit einer temporären Testdatenbank ergänzen oder präzisieren; Tests dürfen keine produktiven Daten, externen Dienste oder Browser verwenden.
- Sicherstellen, dass erfolgreiche Erstell-, Änderungs- und Löschvorgänge weiterhin die bestehenden todo_vorgaenge-N:M-Verknüpfungen verwenden.

## Soll umgesetzt werden

- Fehlertexte für vergleichbare To-Do-Eingabefehler sprachlich konsistent halten.
- Vorhandene Tests so strukturieren, dass sie Statuscode und Fehlerobjekt getrennt von fachlichen Erfolgsdaten prüfen.

## Nicht Teil dieses Arbeitspakets

- Änderungen am To-Do-Datenmodell oder an der Tabelle todo_vorgaenge.
- Neue To-Do-Funktionen, UI-Änderungen oder eine Überarbeitung des Dashboard-Layouts.
- Prüfung anderer API-Bereiche wie Transaktionen, Vorgänge, Belege, Termine, Mails oder externe Adapter.
- Direkte Beziehungen zwischen To-Dos und anderen Entitäten außerhalb der bestehenden Vorgangsverknüpfung.

## Akzeptanzkriterien

- POST /api/todos akzeptiert einen gültigen Payload weiterhin und liefert einen erstellten To-Do-Datensatz mit seinen Vorgangs-IDs.
- POST oder PATCH mit unbekannten Feldern, ungültiger Priorität, ungültigem Datum oder nicht listenförmigen vorgangs_ids liefert HTTP 400 und ein JSON-Objekt mit error.
- POST oder PATCH mit einer nicht existierenden Vorgangs-ID liefert HTTP 404 und verändert weder To-Do noch bestehende Verknüpfungen.
- PATCH und DELETE für eine nicht vorhandene To-Do-ID liefern HTTP 404 und ein JSON-Objekt mit error.
- Die automatisierten Tests laufen lokal ohne Browser, Netzwerkzugriff, Secrets oder produktive Laufzeitdaten durch.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandenen Validierungshelfer und DashboardDataStore-Methoden weiterverwenden; keine parallele API- oder Persistenzarchitektur einführen.
- Fehler aus ValueError als 400 und LookupError als 404 durch die vorhandenen Handlerpfade abbilden.
- Bei Tests ausschließlich temporäre SQLite-Datenbanken und lokale Fixtures verwenden.

## Manuelle Testhinweise

- Dashboard mit einer lokalen temporären oder Testdatenbank starten.
- Ein To-Do mit einer bestehenden Vorgangs-ID anlegen und anschließend ändern.
- Per HTTP-Client jeweils einen Payload mit unbekanntem Feld, ungültiger Priorität und nicht existierender Vorgangs-ID senden und Statuscode sowie JSON-Fehler prüfen.
- PATCH und DELETE für eine bewusst nicht vorhandene todo_-ID ausführen.

## Offene Fragen

- Keine Angaben
