# Nächstes Arbeitspaket

## Titel

Automatisierten Test für stale_mail_removed und die Entfernung aus der Mailübersicht ergänzen

## Epic

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1.2

## Ziel

Das Verhalten bei stale_mail_removed soll automatisiert abgesichert werden: Der veraltete Mail-Eintrag wird fachlich korrekt erkannt und aus der sichtbaren Mailübersicht entfernt.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_mail_integration.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- tests/test_mail_integration.py
- tests/test_dashboard.py

## Muss umgesetzt werden

- Einen automatisierten Test für den Status stale_mail_removed ergänzen.
- Im Test einen zuvor sichtbaren Mail-Eintrag als veraltet beziehungsweise entfernt simulieren.
- Überprüfen, dass der betroffene Eintrag nach der Synchronisation nicht mehr in der sichtbaren Mailübersicht erscheint.
- Bestehende Mail-, Vorgangs- und Verknüpfungsstrukturen unverändert weiterverwenden.
- Externe Maildienste ausschließlich mit Mock, Fake oder Fixture abbilden.

## Soll umgesetzt werden

- Den Test so gestalten, dass sowohl die fachliche Statusänderung als auch die resultierende Darstellung abgesichert sind.
- Falls bereits eine passende Teststruktur existiert, diese statt eines neuen Testaufbaus erweitern.

## Nicht Teil dieses Arbeitspakets

- Keine echte Verbindung zu einem externen Maildienst.
- Keine neuen Mailfunktionen oder Mailprovider-Integrationen.
- Keine Änderung der allgemeinen Mail-Synchronisationslogik außerhalb des für den Test erforderlichen Umfangs.
- Keine Änderungen an Vorgangs-, Beleg-, Transaktions- oder Verknüpfungsmodellen.

## Akzeptanzkriterien

- Ein automatisierter Test reproduziert den Fall stale_mail_removed mit vollständig isolierten Testdaten oder Mocks.
- Der Test schlägt fehl, wenn ein als stale_mail_removed markierter Mail-Eintrag weiterhin in der sichtbaren Mailübersicht erscheint.
- Der Test bestätigt, dass der veraltete Eintrag nach der Verarbeitung aus der sichtbaren Übersicht entfernt ist.
- Der Test bestätigt, dass nicht betroffene Mail-Einträge weiterhin sichtbar bleiben.
- Der Testlauf ist reproduzierbar und benötigt weder Netzwerkzugriff noch Secrets oder produktive Laufzeitdaten.
- Die bestehenden Mail- und Dashboard-Tests bleiben erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete Wahl zwischen HTTP- und Browser-Test soll sich an der vorhandenen Testinfrastruktur orientieren.
- Vorhandene Fixtures, Mock-Schnittstellen und Antwortformate der Mailintegration wiederverwenden.
- Keine direkte Ersatzbeziehung zwischen Mails und fachlichen Objekten einführen; bestehende vorgangsbasierte Beziehungen bleiben maßgeblich.

## Manuelle Testhinweise

- Optional die Mailübersicht mit einem lokalen Testdatensatz öffnen und prüfen, dass der stale_mail_removed-Eintrag nicht angezeigt wird.
- Keine Verbindung zu einem echten Mailkonto für die Prüfung verwenden.

## Offene Fragen

- Ob der bestehende Testaufbau die Entfernung bereits über eine HTTP-Antwort oder über eine Browserdarstellung prüft, soll bei der technischen Analyse des Repositorys geklärt werden.
