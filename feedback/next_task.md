# Nächstes Arbeitspaket

## Titel

Manuelle, nachvollziehbare Saldo-Korrektur für abweichende Volksbank-Saldoanker bereitstellen

## Epic

**Epic-ID:** epic-balance-correction

**Epic-Titel:** Manuelle Behandlung abweichender Kontostandsanker

**Epic-Ziel:** Abweichungen zwischen exportierten Bank-Salden und importierten Umsatz-Saldoketten kontrolliert, nachvollziehbar und ohne Veränderung von Originaldaten behandeln.

**Teilpaket:** Teil 1

## Ziel

Ein Kassierer kann für ein Konto einen ausdrücklich bestätigten lokalen Saldoanker hinterlegen, damit ein nachweislich fehlerhafter oder abweichender Saldo aus der Kontoübersicht den Import nicht dauerhaft blockiert, ohne CSV-Originaldaten oder Bankdaten zu verändern.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/pipeline.py
- banking_readonly/balance_snapshot.py
- banking_dashboard/server.py
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Schlanke, versionierte SQLite-Migration und Persistenzfunktionen für explizite manuelle Saldoanker in transaction_store/database.py
- Import- beziehungsweise Saldoabgleichspfad in transaction_store/pipeline.py und gegebenenfalls banking_readonly/balance_snapshot.py
- Lokaler Dashboard-API-Endpunkt zur validierten Anlage und Abfrage einer Saldo-Korrektur in banking_dashboard/server.py
- Unit-Tests mit temporären SQLite-Datenbanken und synthetischen Volksbank-Exportdaten

## Muss umgesetzt werden

- Die Ursache einer Saldoabweichung weiterhin als Import- beziehungsweise Validierungsfehler erkennbar halten; eine manuelle Korrektur darf nicht stillschweigend erfolgen.
- Eine separate, auditierbare lokale Korrektur speichern, mindestens mit Kontoidentität, korrigiertem Saldo in Cent, Stichtag, Begründung, Erstellzeitpunkt und Kennzeichnung als manuelle Korrektur.
- Keine archivierte CSV-Datei, keine Rohtransaktion und keinen aus der Bank gelesenen Übersichts-Saldo überschreiben.
- Einen lokalen, validierten API-Flow bereitstellen, der nur für ein bestehendes Konto eine Korrektur mit vollständigen Pflichtangaben anlegt und die gespeicherte Korrektur abrufbar macht.
- Den Saldoabgleich so ergänzen, dass eine passende bestätigte manuelle Korrektur als lokaler Saldoanker verwendet wird und der Import bei dadurch aufgelöster Abweichung fortgesetzt werden kann.
- Ungültige Beträge, fehlende Konto- oder Stichtagsangaben, unbekannte Konten und unpassende Korrekturen mit verständlichen lokalen Fehlerantworten ablehnen.
- Regressionstests für den bisherigen Abbruch bei nicht korrigierter Volksbank-Abweichung, die erfolgreiche Behandlung mit passender Korrektur sowie die Unverändertheit der Rohdaten ergänzen.

## Soll umgesetzt werden

- Die API-Antworten so strukturieren, dass die spätere Oberfläche Abweichung, verwendeten lokalen Korrekturanker, Betrag, Stichtag und Begründung eindeutig anzeigen kann.
- Mehrfaches Anlegen derselben fachlichen Korrektur idempotent oder eindeutig konfliktbehaftet behandeln, statt unklare parallele Anker zuzulassen.
- Die Korrekturfunktion mit einem knappen Hinweis dokumentieren, dass sie nur nach manueller Prüfung des Kontoauszugs beziehungsweise Bankstands verwendet werden soll.

## Nicht Teil dieses Arbeitspakets

- Keine echte Banking-Anmeldung, kein CSV-Download und keine produktive Bankaktion.
- Keine Änderung der Volksbank-Exportautomatisierung oder ihrer Selektoren.
- Keine nachträgliche Massenkorrektur historischer Kontostände außerhalb der durch den neuen Anker eindeutig betroffenen Berechnung.
- Keine umfassende Dashboard-Oberfläche, kein komplexer Korrekturverlauf und keine Freigabe-Workflows mit mehreren Rollen.
- Keine Umgestaltung der bestehenden Vorgangs-, Transaktions- oder Belegverknüpfungsarchitektur.

## Akzeptanzkriterien

- Eine manuelle Saldo-Korrektur wird getrennt von Rohdaten und Transaktionen lokal persistiert und enthält Konto, Saldo, Stichtag, Begründung sowie einen auditierbaren Herkunftshinweis.
- Ohne passende manuelle Korrektur bleibt die bekannte Volksbank-Saldoabweichung ein verständlicher, reproduzierbarer Validierungsfehler.
- Mit einer passenden Korrektur kann der betroffene lokale Saldoabgleich den korrigierten Anker verwenden, ohne CSV- oder Bankoriginalwerte zu ändern.
- Der lokale API-Flow lehnt unvollständige und fachlich unzulässige Eingaben mit einem kontrollierten Clientfehler ab.
- Die neuen und bestehenden relevanten Unit-Tests laufen ohne Browser, Netzwerk, Credentials, Bankzugriff oder produktive Laufzeitdaten.

## Hinweise für den Umsetzungs-Agenten

- Für Geldbeträge ausschließlich Integer-Centwerte verwenden; keine Float-Vergleiche einführen.
- Die Korrektur ist ein zusätzlicher lokaler Fakt mit Quelle und Begründung, nicht eine Änderung des von der Bank gelieferten Snapshots.
- Vorhandene Kontoidentifikation und Saldo-Rekonstruktionslogik wiederverwenden.
- Die Korrektur darf keine direkte Beziehung zu Belegen oder anderen Entitäten einführen; Vorgänge und bestehende N:M-Verknüpfungen bleiben unverändert.
- Bei konkurrierenden oder zeitlich nicht passenden Ankern muss der Import weiterhin sicher abbrechen statt einen Wert zu raten.

## Manuelle Testhinweise

- Ausschließlich mit einer temporären lokalen Testdatenbank und synthetischen Volksbank-CSV-/Saldo-Fixtures prüfen.
- Eine bekannte Differenz simulieren, den erwarteten Validierungsfehler prüfen, danach eine begründete Korrektur über den lokalen API-Flow hinterlegen und den erfolgreichen erneuten Abgleich prüfen.
- Kontrollieren, dass die gespeicherten Rohtransaktionen und archivierten Quelldaten vor und nach der Korrektur identisch bleiben.

## Offene Fragen

- Soll eine manuelle Korrektur nur für einen einzelnen Exportstichtag gelten oder bis zu einem späteren verifizierten Bank-Saldoanker fortwirken?
- Soll eine spätere Oberfläche bestehende Korrekturen nur anzeigen oder auch bewusst widerrufen beziehungsweise ersetzen können?
