# Nächstes Arbeitspaket

## Titel

Lokale Testbaseline für die Dashboard- und Transaktionspfade ausführen und Befunde dokumentieren

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 1

## Ziel

Den aktuellen Zustand der vorhandenen Unit-Tests lokal reproduzierbar feststellen und dabei nur eindeutig nachweisbare kleine Fehler in Dashboard- oder Transaktionskern beheben; alle übrigen Befunde sauber als Folgeaufgaben festhalten.

## Relevante Dateien

- tests/test_dashboard.py
- tests/test_transactions.py
- tests/test_config.py
- tests/test_detector.py
- tests/test_exporter.py
- tests/test_login.py
- tests/test_mail_integration.py
- tests/test_player_payments.py
- tests/test_player_premiums.py
- tests/test_session.py
- banking_dashboard/server.py
- transaction_store/database.py
- transaction_store/classification.py
- transaction_store/rules.py
- feedback/Review-report.md

## Wahrscheinliche Änderungsstellen

- tests/ zur Reproduktion und Absicherung konkreter Befunde
- banking_dashboard/server.py für lokale API-, Validierungs- oder Dashboard-Datenflüsse
- transaction_store/database.py für eindeutig nachweisbare Persistenz- oder Integritätsfehler
- transaction_store/classification.py und transaction_store/rules.py für eindeutig testbare Klassifikations- oder Statusinkonsistenzen
- feedback/Review-report.md für die knappe Dokumentation der Testbaseline und offener Befunde

## Muss umgesetzt werden

- Die vollständige lokale Unit-Test-Suite mit `python -m unittest discover -s tests -v` ausführen; keine echten Banking-, Microsoft-Graph-, DFBnet-, Mail- oder OpenAI-Aktionen auslösen.
- Fehlgeschlagene Tests in reproduzierbare Fehler, Umgebungsprobleme und erwartete Testanpassungen unterscheiden.
- Höchstens kleine, klar reproduzierbare Fehler im lokalen Dashboard- oder Transaktionskern beheben, wenn Ursache und erwartetes Verhalten durch bestehende Tests oder Architekturregeln eindeutig belegt sind.
- Für jede Codekorrektur einen passenden Regressionstest ergänzen oder einen vorhandenen Test gezielt präzisieren.
- Eine kurze Testbaseline mit ausgeführten Tests, Ergebnis und nicht innerhalb dieses Pakets lösbaren Befunden in `feedback/Review-report.md` festhalten.

## Soll umgesetzt werden

- Bei bestandenem Testlauf prüfen, ob die vorhandenen Dashboard-Tests die lokalen Kernpfade für Transaktionsdetails, Vorgangsverknüpfungen und Split-Endpunkte ausreichend abdecken.
- Befunde mit möglichem Einfluss auf Datenintegrität, Vorgangsverknüpfungen oder Nutzeraktionen als hohe Folgepriorität markieren.
- Keine produktiven Laufzeitdaten in die Dokumentation übernehmen; ausschließlich Testnamen, anonymisierte Fehlerbilder und technische Ursachen festhalten.

## Nicht Teil dieses Arbeitspakets

- Keine umfassende Umgestaltung des Dashboards oder neuer UI-Flow.
- Keine neue fachliche Architektur und keine direkten Beziehungen außerhalb der bestehenden Vorgangs- und Verknüpfungsstruktur.
- Keine Migration oder grundlegende Umstrukturierung bestehender Tabellen ohne konkreten, testbaren Befund.
- Keine echten externen Logins, Netzwerkanfragen, Browserprofile, Downloads, Mailaktionen oder DFBnet-Aktionen.
- Keine Bearbeitung umfangreicher Folgeprobleme, die erst aus dem Testlauf entstehen; diese werden als getrennte Backlog-Punkte geplant.
- Keine Umsetzung der ausstehend geplanten Kassierer-Usability-Verbesserungen.

## Akzeptanzkriterien

- Die vollständige lokale Unit-Test-Suite wurde ausgeführt und ihr Ergebnis ist nachvollziehbar dokumentiert.
- Alle in diesem Paket behobenen Fehler sind durch mindestens einen automatisierten Regressionstest abgesichert.
- Die geänderte Suite läuft lokal ohne echte externe Dienste, Credentials, produktive Daten oder Browserzugriffe.
- Der dokumentierte Befund unterscheidet klar zwischen bestandenem Zustand, behobenen Defekten und offenen Folgearbeiten.
- Es wurden keine produktiven Banking-, Mail-, Microsoft-Graph- oder DFBnet-Aktionen ausgelöst.

## Hinweise für den Umsetzungs-Agenten

- Bestehende Fakes, Fixtures und Dependency-Injection-Punkte der Testumgebung weiterverwenden.
- Fehler nur dort korrigieren, wo ein eindeutiger reproduzierbarer Widerspruch zwischen Test, API-Vertrag oder bestehender Vorgangsarchitektur vorliegt.
- Bei unklarer fachlicher Erwartung keine stillschweigende Verhaltensänderung vornehmen, sondern eine offene Frage oder einen Backlog-Befund dokumentieren.
- Die Auswertung soll insbesondere sicherstellen, dass lokale Validierungs- und Fehlerpfade keine unkontrollierten Serverfehler erzeugen.
- Vorgänge bleiben die zentrale fachliche Einheit; bestehende N:M-Verknüpfungen zwischen Transaktionen, Vorgängen, Belegen, Mails, To-Dos und Terminen dürfen nicht durch direkte Ersatzbeziehungen umgangen werden.

## Manuelle Testhinweise

- Kein echter externer manueller Test erforderlich.
- Optional nach einem lokalen, vollständig grünen Testlauf einen bereits vorhandenen Testdatenbank-Workflow starten und ausschließlich lokal prüfen, dass Dashboard und Transaktionsdetail erreichbar bleiben.

## Offene Fragen

- Falls der vollständige Testlauf Umgebungsabhängigkeiten offenlegt: Sind diese als projektseitige Fehler zu beheben oder als dokumentierte lokale Voraussetzung vorgesehen?
- Welche Befunde aus der Testbaseline sollen vor weiteren Funktionsausbauten zwingend als Blocker behandelt werden?
