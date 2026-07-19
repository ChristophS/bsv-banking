# Nächstes Arbeitspaket

## Titel

Nicht mehr vorhandene Mails aus der Übersicht entfernen

## Epic

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1

## Ziel

Wenn eine in der Anwendung bekannte Mail beim Öffnen oder Aktualisieren im externen Mailbestand nicht mehr gefunden wird, soll der veraltete Mail-Eintrag lokal entfernt werden, ohne die Mailübersicht mit einem Fehler abzubrechen.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- banking_dashboard/server.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- Mail-Synchronisations- oder Abruflogik
- Fehlerbehandlung für nicht mehr vorhandene externe Mailobjekte
- Tests für das Entfernen veralteter Mail-Einträge

## Muss umgesetzt werden

- Das erwartbare Nichtvorhandensein einer zuvor bekannten Mail im externen Store erkennen.
- Den zugehörigen veralteten Eintrag aus der lokalen Mailübersicht beziehungsweise dem verwendeten Mailbestand entfernen.
- Die Mailübersicht trotz dieser erwartbaren Änderung ohne unbehandelten Fehler weiter anzeigen oder aktualisieren.
- Andere Mailfehler weiterhin gemäß der bestehenden Fehlerbehandlung behandeln und nicht pauschal verschlucken.
- Tests für eine außerhalb der Anwendung gelöschte Mail ergänzen.

## Soll umgesetzt werden

- Die Erkennung auf die bekannten Fehlerbilder für nicht gefundene Objekte und nicht ladbare Eigenschaften begrenzen.
- Das Verhalten bei wiederholter Aktualisierung idempotent absichern.

## Nicht Teil dieses Arbeitspakets

- Eine vollständige Mail-Synchronisation oder ein neues Mail-Datenmodell.
- Das automatische Löschen von Mails im externen Mailbestand.
- Die Behandlung unabhängiger Mailfunktionen wie Versand, Suche oder Anhänge.
- Änderungen an Vorgängen, Transaktionen oder anderen fachlichen Bereichen.

## Akzeptanzkriterien

- Wird eine bekannte Mail extern gelöscht und beim Öffnen nicht mehr gefunden, verschwindet sie aus der lokalen Übersicht.
- Für diesen erwartbaren Fall wird kein technischer Fehler in der Benutzeroberfläche angezeigt und der verbleibende Mailbestand bleibt nutzbar.
- Fehler, die nicht auf ein fehlendes externes Mailobjekt hindeuten, werden nicht als erfolgreiche Löschung behandelt.
- Das Verhalten ist durch automatisierte Tests abgedeckt.
- Das erneute Aktualisieren nach erfolgter Entfernung erzeugt keinen weiteren Fehler und keinen doppelten Löschvorgang.

## Hinweise für den Umsetzungs-Agenten

- Bestehende Mail-Services, Tabellen und Verknüpfungen verwenden; keine parallele Ersatzstruktur einführen.
- Externe Mailzugriffe ausschließlich mit Mocks, Fakes oder Fixtures testen.

## Manuelle Testhinweise

- Mit einem Mock für eine zuvor bekannte Mail den Fehler 'The specified object was not found in the store' auslösen und prüfen, dass die Mail aus der Übersicht entfernt wird.
- Einen nicht erwartbaren Mailfehler simulieren und prüfen, dass er weiterhin sichtbar beziehungsweise protokolliert wird.

## Offene Fragen

- Welche konkreten externen Fehlertypen beziehungsweise Exception-Klassen verwendet die bestehende Mail-Integration für nicht gefundene Objekte?
- Wird die Übersicht aus einer lokalen Persistenz, einem Cache oder ausschließlich aus dem aktuellen externen Abruf aufgebaut?
