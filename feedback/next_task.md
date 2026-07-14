# Nächstes Arbeitspaket

## Titel

Termin-API um konsistente Validierung und Fehlerantworten ergänzen

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.5

## Ziel

Termin-Erstellung, -Änderung und -Löschung sollen Eingabefehler, ungültige Statuswerte und fehlerhafte Vorgangsverknüpfungen einheitlich ablehnen und dabei nachvollziehbare Fehlerantworten ohne unvollständige Änderungen liefern.

## Relevante Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Terminbezogene API-Endpunkte und deren Validierungslogik
- Bestehende Terminmodelle oder Service-Aufrufe
- Tests für Erstellung, Änderung und Löschung von Terminen

## Muss umgesetzt werden

- Die vorhandenen Termin-API-Flows für Erstellung, Änderung und Löschung fachlich prüfen.
- Pflichtfelder, Datumswerte, Statuswerte und zulässige Vorgangsverknüpfungen konsistent validieren.
- Ungültige Eingaben mit stabilen, nachvollziehbaren Fehlerantworten und passenden HTTP-Statuscodes zurückweisen.
- Sicherstellen, dass fehlgeschlagene Validierungen keine teilweise gespeicherten oder geänderten Termine hinterlassen.
- Bestehende Vorgangsstrukturen und Verknüpfungsservices verwenden.

## Soll umgesetzt werden

- Fehlerantworten in den betroffenen Flows auf ein einheitliches Format abstimmen, soweit dies ohne breiten API-Umbau möglich ist.
- Grenzfälle für Datumsbereiche, unbekannte Vorgänge und nicht unterstützte Statuswerte durch Tests abdecken.

## Nicht Teil dieses Arbeitspakets

- Neue Termin-Funktionen oder eine umfassende UI-Überarbeitung.
- Umbau der bestehenden Vorgangsarchitektur oder Verknüpfungstabellen.
- Änderungen an Transaktions-, Beleg-, Mail- oder To-do-APIs.
- Externe Kalender- oder andere externe Dienstintegrationen.

## Akzeptanzkriterien

- Erstellung eines Termins mit ungültigen oder fehlenden Pflichtdaten wird abgelehnt und erzeugt keinen Datensatz.
- Änderung eines Termins mit ungültigen Daten wird abgelehnt und lässt den vorherigen Zustand unverändert.
- Löschung eines nicht vorhandenen oder unzulässig referenzierten Termins liefert eine nachvollziehbare Fehlerantwort.
- Ungültige Statuswerte, Datumswerte und Vorgangsverknüpfungen werden einheitlich behandelt.
- Erfolgreiche Erstellung, Änderung und Löschung behalten das bestehende fachliche Verhalten bei.
- Automatisierte Tests decken erfolgreiche und fehlerhafte Termin-API-Flows ab und bestehen.

## Hinweise für den Umsetzungs-Agenten

- Vorhandene Validierungs- und Fehlerbehandlungsmuster des Dashboards wiederverwenden.
- Keine produktiven externen Aktionen ausführen; Tests bleiben lokal und verwenden vorhandene Testdaten oder Fixtures.
- Technische Detailentscheidungen zur konkreten Implementierungsstelle können nach Repository-Analyse getroffen werden.

## Manuelle Testhinweise

- Einen gültigen Termin anlegen, ändern und löschen.
- Jeweils fehlende Pflichtdaten, ungültige Datumswerte, unbekannte Vorgänge und ungültige Statuswerte testen.
- Nach jedem abgewiesenen Änderungsversuch prüfen, dass der ursprüngliche Termin unverändert bleibt.

## Offene Fragen

- Welches bestehende Fehlerantwortformat gilt aktuell als Standard für die Dashboard-API?
- Welche Terminstatuswerte und Datumsgrenzen sind im bestehenden Modell verbindlich definiert?
