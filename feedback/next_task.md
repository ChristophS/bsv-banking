# Nächstes Arbeitspaket

## Titel

Vorgangsbasierte Grundlage für die Zuordnung von Mail-Dokumenten zu Transaktionsbezügen schaffen

## Epic

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 1

## Ziel

Für einen bestehenden zentralen Vorgang eine serverseitig überprüfbare Zuordnungsgrundlage schaffen, mit der mehrere Dokumente einer Mail über vorhandene Vorgänge unterschiedlichen bereits verknüpften Transaktionen zugeordnet werden können, ohne eine direkte Beleg-Transaktions-Beziehung einzuführen.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- banking_dashboard/mail_integration.py
- banking_dashboard/server.py
- tests/test_mail_integration.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Bestehende Tabellen und Hilfsfunktionen für vorgaenge, transaktion_vorgaenge, belege und vorgang_belege in transaction_store/database.py
- Bestehende Mail-Anhangs- und Inbox-Verknüpfungslogik in banking_dashboard/mail_integration.py
- Interne serverseitige Datenaufbereitung für Mail- und Vorgangsdetails in banking_dashboard/server.py
- Unit-Tests für die Datenintegrität und die Mail-/Vorgangslogik

## Muss umgesetzt werden

- Den vorhandenen Datenfluss für Inbox-Anhänge, Belege, Vorgänge und Transaktionsverknüpfungen analysieren und eine kleine, explizite serverseitige Zuordnungsrepräsentation festlegen.
- Sicherstellen, dass ein als zuordenbar angebotener Transaktionsbezug ausschließlich über einen Vorgang erreichbar ist, der bereits mit der jeweiligen Transaktion über transaktion_vorgaenge verknüpft ist.
- Die Zuordnungsgrundlage so speichern oder ableiten, dass pro Mail-Dokument nachvollziehbar bleibt, welchem zulässigen Vorgangs-/Transaktionsbezug es zugeordnet ist.
- Ausschließlich bestehende Vorgänge, transaktion_vorgaenge, belege und vorgang_belege beziehungsweise deren vorhandene Erweiterungspunkte verwenden.
- Direkte Beziehungen zwischen Belegen beziehungsweise Mail-Anhängen und Transaktionen ausdrücklich vermeiden.
- Serverseitige Validierung für unbekannte Mail-Dokumente, unbekannte Vorgänge und nicht zum Vorgangskontext gehörende Transaktionsbezüge ergänzen.
- Automatisierte Tests mit SQLite-Testdaten und Mail-Fixtures ergänzen; weder Microsoft Graph noch produktive Mails oder Anhänge verwenden.

## Soll umgesetzt werden

- Die Zuordnungsdaten in einer für den späteren API- und UI-Schritt leicht auslesbaren Form bereitstellen.
- Fehlermeldungen fachlich verständlich formulieren, insbesondere wenn ein ausgewählter Bezug nicht zum zentralen Vorgang gehört.
- Die Implementierung idempotent gestalten, sodass eine erneute Speicherung derselben Zuordnung keine Dubletten erzeugt.

## Nicht Teil dieses Arbeitspakets

- Keine neue direkte Beleg-Transaktions- oder Mail-Anhang-Transaktions-Tabelle einführen.
- Keine Mail-Detailoberfläche, Auswahlfelder oder JavaScript-Interaktion implementieren.
- Keine öffentliche oder umfangreiche Bearbeitungs-API für die Oberfläche implementieren; diese folgt als Teil 2.
- Keine automatische Vorgangserstellung oder automatische Dokumentzuordnung aus Mailinhalten durchführen.
- Keine produktiven Microsoft-Graph-Aktionen, keine echten Mails und keine realen Anhänge abrufen oder verändern.

## Akzeptanzkriterien

- Ein zentraler Vorgang mit mehreren bereits zugeordneten Transaktionen kann mehrere Mail-Dokumente mit unterschiedlichen zulässigen Transaktionsbezügen fachlich unterscheiden.
- Jede gespeicherte Dokumentzuordnung ist ausschließlich über bestehende Vorgangsverknüpfungen auflösbar; es existiert keine direkte Beziehung von Beleg oder Mail-Anhang zu einer Transaktion.
- Ein Bezug auf einen nicht existierenden Vorgang, eine nicht existierende Transaktion oder eine Transaktion außerhalb des Vorgangskontexts wird serverseitig abgelehnt.
- Wiederholtes Speichern derselben gültigen Zuordnung erzeugt keine Dublette.
- Bestehende Mail-, Vorgangs-, Beleg- und Transaktionsverknüpfungen bleiben unverändert funktionsfähig.
- Neue Tests decken mindestens einen Vorgang mit zwei Transaktionen und zwei unterschiedlich zugeordneten Mail-Dokumenten sowie ungültige Zuordnungsversuche ab.

## Hinweise für den Umsetzungs-Agenten

- Der zentrale Vorgang bleibt das fachliche Objekt, das Mail, Belege und Transaktionsbezüge zusammenführt.
- Die fachliche Differenzierung eines Dokumentbezugs muss über vorhandene beziehungsweise zulässige Vorgangsverknüpfungen modelliert werden; eine Entität-zu-Entität-Abkürzung zu transactions ist unzulässig.
- Vor einer Migration prüfen, ob die bestehende Inbox-Anhangsstruktur bereits eine stabile Referenz bietet, die mit dem Belegkatalog und vorgang_belege verbunden werden kann.
- Datenbankänderungen nur ergänzend und migrationsfähig umsetzen; vorhandene Tabellen und Altverknüpfungen nicht grundlegend umbauen.
- Die spätere Auswahl-API soll auf derselben validierten serverseitigen Grundlage aufbauen und keine zweite Zuordnungslogik enthalten.

## Manuelle Testhinweise

- Mit einer lokalen Testdatenbank einen zentralen Vorgang anlegen und zwei Transaktionen über transaktion_vorgaenge verknüpfen.
- Zwei fixture-basierte Mail-Dokumente dem Vorgangskontext zuführen und jeweils einem anderen der beiden zulässigen Transaktionsbezüge zuordnen.
- Prüfen, dass beide Zuordnungen nachvollziehbar ausgelesen werden können und keine direkte Beleg-Transaktions-Verknüpfung entsteht.
- Versuchen, ein Dokument einer nicht mit dem zentralen Vorgang verbundenen Transaktion zuzuordnen; die Operation muss fehlschlagen.
- Bestehende Mail- und Vorgangsdetailtests ausführen.

## Offene Fragen

- Soll ein Mail-Anhang bei der Zuordnung zwingend als Eintrag im bestehenden Belegkatalog geführt werden, oder existiert dafür bereits eine stabile Belegrepräsentation in der Mailintegration?
- Soll ein Dokument mehrere zulässige Transaktionsbezüge erhalten können, oder ist im ersten Ausbauschritt genau ein Bezug pro Dokument vorgesehen?
- Wie soll die Zuordnung fachlich behandelt werden, wenn der zentrale Vorgang später von einer Transaktion getrennt wird: ablehnen, entfernen oder als prüfbedürftig markieren?
