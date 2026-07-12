# Nächstes Arbeitspaket

## Titel

Vorgangsbasierte Auswahl-API für Mail-Dokumentzuordnungen bereitstellen

## Epic

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 2

## Ziel

Eine kleine, validierte API bereitstellen, über die die Oberfläche für einen bestehenden Vorgang die zulässigen zugeordneten Transaktionen und Mail-Dokumente lesen sowie die vorgangsbasierte Zuordnung ändern kann, ohne direkte Transaktion-Beleg-Beziehungen einzuführen.

## Relevante Dateien

- banking_dashboard/server.py
- transaction_store/database.py
- tests/test_dashboard.py
- tests/test_mail_integration.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- DashboardDataStore in banking_dashboard/server.py: lesende und schreibende Service-Methode für die Auswahl- und Zuordnungsdaten
- DashboardRequestHandler in banking_dashboard/server.py: abgegrenzte GET- und Änderungsendpunkte unter dem bestehenden Vorgangs-/Mail-API-Namensraum
- transaction_store/database.py: nur falls die bereits vorhandene vorgangsbasierte Zuordnungsgrundlage eine kleine ergänzende Abfrage oder validierte Persistenzfunktion benötigt
- tests/test_dashboard.py: API-, Validierungs- und Architekturtests mit lokaler Testdatenbank

## Muss umgesetzt werden

- Die bestehende vorgangsbasierte Zuordnungsgrundlage wiederverwenden: Belege bleiben ausschließlich über vorgang_belege und Transaktionen ausschließlich über transaktion_vorgaenge mit Vorgängen verbunden.
- Eine lesende API bereitstellen, die für einen Vorgang mindestens dessen verknüpfte Transaktionen, die für die Zuordnung verfügbaren Mail-Dokumente beziehungsweise Belege und die aktuelle Zuordnung liefert.
- Eine klar abgegrenzte schreibende API bereitstellen, die nur zulässige Zuordnungen innerhalb des adressierten Vorgangs akzeptiert und die bestehende Validierungs- und Fehlerbehandlungsstruktur verwendet.
- Eingaben strikt validieren: Vorgang, Transaktionen und Belege müssen existieren und zum erlaubten vorgangsbasierten Kontext gehören; unbekannte Felder und widersprüchliche IDs müssen mit einem Clientfehler abgewiesen werden.
- Automatisierte Tests für erfolgreichen Abruf, erfolgreiche Änderung, nicht vorhandene IDs, unzulässige kontextfremde Zuordnungen und die Abwesenheit direkter Transaktion-Beleg-Verknüpfungen ergänzen.

## Soll umgesetzt werden

- Antwortdaten stabil und UI-tauglich strukturieren, einschließlich IDs, lesbarer Bezeichnungen und aktueller Verknüpfungsinformationen.
- Bestehende API-Statuscodes und deutschsprachige Fehlermeldungskonventionen des Dashboards beibehalten.
- Die Änderung idempotent gestalten, soweit dieselbe vorgangsbasierte Zuordnung erneut gespeichert wird.

## Nicht Teil dieses Arbeitspakets

- Mail-Detailansicht oder sonstige Frontend-Bedienung für die Dokumentzuordnung.
- Neue direkte Tabellen oder Fremdschlüssel zwischen Transaktionen und Belegen.
- Automatische Dokument- oder Vorgangserkennung aus Mails.
- Umsetzung von Transaktions-Splits, Rechnungs- oder Teilrechnungslogik.
- Microsoft-Graph-Aufrufe, produktive Mailaktionen oder Änderungen an OAuth- und Credential-Verarbeitung.

## Akzeptanzkriterien

- Für einen existierenden Vorgang kann ein API-Client die zulässigen verknüpften Transaktionen, relevanten Mail-Dokumente beziehungsweise Belege und deren aktuellen vorgangsbasierten Kontext abrufen.
- Eine gültige Änderungsanfrage aktualisiert ausschließlich bestehende, über Vorgänge modellierte Verknüpfungen und liefert den aktualisierten Zustand zurück.
- Eine Anfrage mit fehlendem Vorgang, unbekannter Transaktion, unbekanntem Beleg, fremdem Kontext oder unbekannten Payload-Feldern wird nachvollziehbar mit einem 4xx-Fehler abgelehnt.
- Es wird keine direkte Beziehung zwischen transactions und belege eingeführt oder verwendet.
- Die neuen und bestehenden Dashboard- sowie Transaktionstests laufen ohne Browser, Microsoft Graph, externe Dienste oder produktive Daten.

## Hinweise für den Umsetzungs-Agenten

- Vorhandene Link-Tabellen und die bestehenden DashboardDataStore-Methoden für Vorgänge, Transaktionen und Belege als einzige fachliche Verknüpfungspunkte verwenden.
- Die API an vorhandenen REST-Mustern wie GET/POST/DELETE für vorgangsbezogene Links ausrichten, statt einen parallelen generischen Zuordnungsmechanismus zu schaffen.
- Falls die fachliche Differenzierung mehrerer Dokumente zu verschiedenen Transaktionsbezügen mehrere Vorgangskontexte benötigt, diese über bestehende Vorgänge und deren N:M-Links abbilden; keine direkte Dokument-Transaktions-Persistenz ergänzen.
- Tests mit temporären SQLite-Testdatenbanken und vorhandenen Fakes/Fixtures durchführen.

## Manuelle Testhinweise

- Mit einer lokalen Testdatenbank einen Vorgang mit mindestens zwei Transaktionen und mehreren über den Vorgang erreichbaren Dokumenten anlegen.
- Die Auswahl-API aufrufen und prüfen, dass nur Daten aus dem adressierten Vorgangskontext angeboten werden.
- Eine gültige Änderung speichern, erneut lesen und die aktualisierte vorgangsbasierte Zuordnung prüfen.
- Je einen Änderungsversuch mit einer fremden Transaktions-ID und einer fremden Beleg-ID ausführen und die erwartete Ablehnung prüfen.

## Offene Fragen

- Welche bereits in Teil 1 eingeführte Persistenzdarstellung bildet die feingranulare Mail-Dokumentauswahl innerhalb eines Vorgangs ab, falls sie über die vorhandenen N:M-Verknüpfungen hinausgeht?
- Soll die API ausschließlich importierte Mail-Anhänge berücksichtigen oder zusätzlich bereits katalogisierte Belege, deren Quellenreferenz auf dieselbe Mail verweist?
