# Nächstes Arbeitspaket

## Titel

Mail nach dem Erstellen eines Vorgangs sofort als gelesen markieren

## Epic

**Epic-ID:** epic-mail-vorgang-status

**Epic-Titel:** Mail-zu-Vorgang-Nachbearbeitung automatisieren

**Epic-Ziel:** Nach dem Erstellen eines Vorgangs aus einer Mail sollen passende Mail-Statusänderungen automatisch und ohne manuelle Nacharbeit ausgeführt werden.

**Teilpaket:** Teil 1

## Ziel

Wird aus einer Mail ein Vorgang erstellt, soll die zugrunde liegende Mail anschließend automatisch den Status „Gelesen“ erhalten.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- Mail-zu-Vorgang-Erstellungsablauf
- Mail-Statusaktualisierung
- Tests der Mail-Integration

## Muss umgesetzt werden

- Nach erfolgreicher Erstellung eines Vorgangs aus einer Mail die Mail als gelesen markieren.
- Die Statusänderung nur nach erfolgreicher Vorgangserstellung ausführen.
- Den bestehenden Vorgangs-Erstellungsablauf und vorhandene Mail-Strukturen verwenden.
- Bei einer fehlgeschlagenen Vorgangserstellung die Mail nicht als gelesen markieren.

## Soll umgesetzt werden

- Die Statusänderung über die bestehende Mail-Integrationsabstraktion ausführen.
- Den Ablauf mit einem Mock oder Fake testen, ohne einen externen Mail-Dienst aufzurufen.

## Nicht Teil dieses Arbeitspakets

- Änderungen an Mail-Postfächern oder echten externen Mail-Diensten.
- Einführung einer neuen Mail- oder Vorgangsarchitektur.
- Änderungen an der manuellen Funktion zum Markieren von Mails als gelesen.
- Weitere Mail-Aktionen wie Verschieben, Löschen oder Beantworten.

## Akzeptanzkriterien

- Nach erfolgreicher Vorgangserstellung wird der Read-Status der Ausgangsmail auf gelesen gesetzt.
- Bei einem Fehler während der Vorgangserstellung bleibt der Read-Status unverändert.
- Der bestehende Erstellungsablauf funktioniert für Mails weiterhin vollständig.
- Automatisierte Tests decken den Erfolgsfall und den Fehlerfall ab.
- Die Tests verwenden ausschließlich Mocks, Fakes oder Fixtures.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete technische Änderungsstelle soll anhand der vorhandenen Mail-Integrations-API ermittelt werden.
- Die Statusänderung sollte erst erfolgen, wenn die Vorgangserstellung erfolgreich abgeschlossen und bestätigt ist.

## Manuelle Testhinweise

- Eine Mail-Fixture auswählen und daraus einen Vorgang erstellen.
- Prüfen, dass die Mail danach als gelesen angezeigt wird.
- Einen simulierten Fehler bei der Vorgangserstellung auslösen und prüfen, dass die Mail ungelesen bleibt.

## Offene Fragen

- Keine Angaben
