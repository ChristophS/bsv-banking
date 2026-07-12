# Nächstes Arbeitspaket

## Titel

Lokale Testbaseline für Dashboard- und Transaktionspfade ausführen und Befunde dokumentieren

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 1

## Ziel

Die bestehende Unit-Test-Suite reproduzierbar lokal ausführen, eindeutig belegte kleine Kernbefunde festhalten und ausschließlich unmittelbar klar abgrenzbare Test- oder Konsistenzfehler korrigieren.

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
- transaction_store/pipeline.py
- feedback/backlog.md
- feedback/implementation_report.md

## Wahrscheinliche Änderungsstellen

- Tests unter tests/, falls ein vorhandener Test eindeutig fehlerhaft, instabil oder nicht mehr mit dem spezifizierten lokalen Verhalten vereinbar ist.
- Die jeweils unmittelbar betroffene kleine Implementierungsstelle in banking_dashboard/server.py, transaction_store/database.py oder transaction_store/pipeline.py, falls ein reproduzierbarer Kernfehler mit engem Fix nachgewiesen ist.
- feedback/implementation_report.md zur nachvollziehbaren Dokumentation von Testlauf, Befunden, vorgenommenen Korrekturen und bewusst verschobenen Punkten.

## Muss umgesetzt werden

- Die vollständige lokale Unit-Test-Suite mit python -m unittest discover -s tests -v ausführen.
- Sicherstellen, dass der Testlauf keine echten Banking-, Microsoft-Graph-, OpenAI- oder DFBnet-Zugriffe, keine Browserprofile und keine produktiven Laufzeitdaten benötigt.
- Fehlschläge, Überspringungen oder auffällige Warnungen nach Reproduzierbarkeit, betroffenem Modul und vermuteter Ursache erfassen.
- Nur eindeutig belegte, kleine und lokal testbare Kernfehler beheben; für jeden Fix einen passenden Regressionstest ergänzen oder einen vorhandenen Test gezielt präzisieren.
- Den Testbefehl, Ergebnisstatus, korrigierte Befunde und verbleibende Folgebefunde strukturiert in feedback/implementation_report.md dokumentieren.
- Nicht eindeutig abgrenzbare oder größere Befunde als konkrete Folgepunkte für die bestehenden Teile 2 bis 4 des Konsistenz-Epics dokumentieren, statt sie in diesem Paket breit umzubauen.

## Soll umgesetzt werden

- Bei einem grünen Lauf stichprobenartig prüfen, ob die wichtigsten Dashboard- und Transaktions-Tests tatsächlich ausschließlich temporäre Testdaten und Mocks verwenden.
- Bei fehlender lokaler Abhängigkeit die Ursache knapp dokumentieren und nur requirements.txt oder Test-Setup anpassen, wenn die Abweichung eindeutig projektbedingt und ohne externe Konfiguration behebbar ist.
- Vorhandene Testnamen und Assertions auf verständliche fachliche Aussagekraft prüfen und nur bei unmittelbarer Unklarheit verbessern.

## Nicht Teil dieses Arbeitspakets

- Breite Überarbeitung der Dashboard-API-Validierung oder aller Fehlerantworten.
- Umfassende Prüfung oder Umbau sämtlicher Persistenz- und Vorgangsverknüpfungen.
- Neue Produktfeatures, UI-Redesigns oder Änderungen an Transaktions-Splits.
- Echte Logins, Browserstarts, Netzwerkzugriffe oder Aktionen gegen Banking, Microsoft Graph, OpenAI oder DFBnet.
- Anforderung oder Verarbeitung von Credentials, Tokens, Datenbanken, Exporten, Kontoauszügen, Belegen oder Logs aus produktiven Umgebungen.

## Akzeptanzkriterien

- Die vollständige Unit-Test-Suite wurde lokal mit dem dokumentierten Befehl ausgeführt.
- Der dokumentierte Lauf enthält eine klare Angabe zu Anzahl erfolgreicher, fehlgeschlagener und gegebenenfalls übersprungener Tests.
- Alle innerhalb dieses Pakets behobenen Fehler sind reproduzierbar durch einen passenden Test abgesichert.
- Der Testlauf nutzt ausschließlich lokale Testdaten, Mocks, Fakes oder Fixtures und löst keine produktiven externen Aktionen aus.
- feedback/implementation_report.md enthält nachvollziehbar Testkommando, Ergebnis, kleine Korrekturen und klar abgegrenzte offene Folgepunkte.
- Größere Befunde wurden nicht verdeckt in diesem Paket umgesetzt, sondern den passenden Folgepaketen des Konsistenz-Epics zugeordnet.

## Hinweise für den Umsetzungs-Agenten

- Vorgänge bleiben das zentrale fachliche Objekt; bei einem nachgewiesenen Fehler keine direkte Ersatzbeziehung zwischen Transaktionen und Belegen einführen.
- Für testbare Fehlerkorrekturen die vorhandenen Datenbank-, Pipeline- und Dashboard-Services nutzen und keine neue fachliche Grundarchitektur schaffen.
- Externe Adapter ausschließlich über vorhandene Mocks, Fakes oder Fixtures prüfen; Tests dürfen keine echten HTTP-, Browser- oder Login-Abläufe verlangen.
- Den Umfang auf einen einzelnen reproduzierbaren Baseline-Lauf mit eng begrenzten Korrekturen beschränken.

## Manuelle Testhinweise

- Den Unit-Test-Befehl in einer lokalen virtuellen Umgebung ausführen.
- Prüfen, dass während des Laufs kein sichtbarer Browser geöffnet wird und keine Aufforderung zur Eingabe von Zugangsdaten erscheint.
- Nach einem möglichen Fix die vollständige Suite erneut ausführen und das Ergebnis in der Dokumentation aktualisieren.

## Offene Fragen

- Falls die Suite fehlschlägt: Handelt es sich um einen echten Produktfehler, eine veraltete Testannahme oder eine fehlende lokale Entwicklungsabhängigkeit?
- Falls ein Befund mehrere API-, UI- und Persistenzpfade betrifft: Welchem der Folgepakete Teil 2 bis Teil 4 des Konsistenz-Epics ist er konkret zuzuordnen?
