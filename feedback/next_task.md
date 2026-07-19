# Nächstes Arbeitspaket

## Titel

Mail als gelesen markieren trotz erwartbarem MailboxConcurrency-Fehler ermöglichen

## Epic

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1

## Ziel

Das Markieren einer Mail als gelesen soll bei einem erwartbaren MailboxConcurrency-Fehler robust und begrenzt verarbeitet werden, ohne echte externe Mail-Aktionen in Tests auszuführen.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- Mailstatus-Aktion und Fehlerbehandlung in banking_dashboard/mail_integration.py
- Mock- oder Fake-basierte Tests in tests/test_mail_integration.py

## Muss umgesetzt werden

- Die bestehende Funktion zum Markieren einer Mail als gelesen muss einen erwartbaren MailboxConcurrency-Fehler erkennen und kontrolliert behandeln.
- Die Verarbeitung darf keine unbegrenzten Wiederholungen oder echten externen Mail-Aktionen in Tests einführen.
- Das Verhalten für erfolgreiche Markierungen und nicht erwartete Fehler muss erhalten beziehungsweise eindeutig bleiben.
- Die Fehlerbehandlung muss eine verständliche fachliche Rückmeldung an die aufrufende Mailübersicht ermöglichen.

## Soll umgesetzt werden

- Die maximale Wiederholungs- oder Wartebehandlung soll begrenzt und nachvollziehbar sein.
- Erwartbare externe Fehler sollten über die bestehende Integrationsstruktur abstrahiert und mit Mocks oder Fakes getestet werden.

## Nicht Teil dieses Arbeitspakets

- Entfernen außerhalb der Anwendung gelöschter Mails aus der Übersicht; dies ist Teil 2 des Epics.
- Allgemeine Mail-Synchronisation oder ein vollständiger Umbau der Mailintegration.
- Echte Mailbox-Aufrufe, externe Testkonten oder produktive Zugangsdaten.

## Akzeptanzkriterien

- Eine erfolgreiche Markierung als gelesen wird weiterhin als Erfolg verarbeitet.
- Ein erwartbarer MailboxConcurrency-Fehler führt nicht zu einem ungeklärten Anwendungsfehler.
- Die Behandlung des erwartbaren Fehlers ist begrenzt und endet mit einem definierten Ergebnis oder einer verständlichen Rückmeldung.
- Nicht erwartbare Fehler werden nicht stillschweigend verschluckt.
- Automatisierte Tests decken Erfolg, erwartbaren Concurrency-Fehler und mindestens einen nicht erwartbaren Fehlerfall mit Mock oder Fake ab.
- Bestehende Mailtests bleiben erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Vorhandene Mailintegrations- und Fehlerstrukturen verwenden; keine parallele Ersatzintegration anlegen.
- Die konkrete Erkennung des externen Fehlers soll an der bestehenden Abstraktion erfolgen und nicht von produktiven Maildaten abhängen.
- Falls die externe Bibliothek unterschiedliche Fehlertypen oder Fehlermeldungen liefert, diese so eng wie möglich begrenzen.

## Manuelle Testhinweise

- Eine Mailübersicht mit einer ungelesenen Mail öffnen und die Markierung als gelesen auslösen.
- Den Concurrency-Fehler im Test oder über einen Fake simulieren und prüfen, dass die Oberfläche eine verständliche Rückmeldung erhält und bedienbar bleibt.
- Eine erfolgreiche Markierung prüfen, ohne ein echtes externes Postfach zu verwenden.

## Offene Fragen

- Welche konkrete Fehlerklasse oder Fehlermeldungsstruktur stellt die bestehende Mailbibliothek für MailboxConcurrency bereit?
- Soll die Oberfläche bei einem temporären Fehler den Status unverändert lassen oder einen erneuten manuellen Versuch anbieten?
