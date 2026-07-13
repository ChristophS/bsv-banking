# Nächstes Arbeitspaket

## Titel

Persistenzintegrität der Vorgangsverknüpfungen absichern

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 3

## Ziel

Änderungen, Löschungen und Abschlussprüfungen sollen bestehende Verknüpfungen zwischen Transaktionen und Vorgängen konsistent erhalten oder kontrolliert aktualisieren, ohne unzulässige oder verwaiste Beziehungen zu erzeugen.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/pipeline.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- Persistenz- und Verknüpfungslogik im transaction_store
- Tests für Erzeugung, Änderung, Löschung und Abschlussprüfung von Transaktionen und Vorgängen

## Muss umgesetzt werden

- Die bestehenden Persistenzpfade für Transaktionen und ihre Vorgänge auf zulässige Verknüpfungen und Folgeeffekte prüfen.
- Sicherstellen, dass Änderungen und Löschungen keine unzulässigen oder verwaisten Transaktions-Vorgangs-Beziehungen hinterlassen.
- Bestehende Vorgangs- und Verknüpfungsstrukturen weiterverwenden; keine direkte Ersatzbeziehung außerhalb der Vorgangsarchitektur einführen.
- Für die geprüften Integritätsregeln reproduzierbare lokale Tests ergänzen oder bestehende Tests schärfen.
- Fehlerhafte Änderungen atomar ablehnen, sodass bei einem Validierungsfehler kein unvollständiger Persistenzzustand verbleibt.

## Soll umgesetzt werden

- Folgeeffekte bei Abschlussprüfungen und beim initialen Erzeugen eines Vorgangs dokumentieren.
- Fehlerfälle für fehlende, ungültige oder bereits gelöschte Referenzen abdecken.

## Nicht Teil dieses Arbeitspakets

- Neue UI-Funktionen oder eine Überarbeitung des Dashboards
- Die vollständige Prüfung aller API-Endpunkte
- Transaktions-Splits, Split-Editoren oder mehrere Teilrechnungen
- Externe Banking-, Mail-, Microsoft-Graph- oder DFBnet-Aktionen
- Grundlegender Umbau bestehender Tabellen, Services oder Verknüpfungsmodelle

## Akzeptanzkriterien

- Eine Transaktion kann weiterhin genau über die bestehende Vorgangsstruktur mit ihrem Vorgang verknüpft werden.
- Ungültige oder fehlende Verknüpfungsreferenzen werden mit einem nachvollziehbaren Fehler abgelehnt.
- Bei abgelehnten Änderungen oder Löschungen bleiben vorherige gültige Persistenzdaten unverändert.
- Lösch- und Änderungsfälle erzeugen keine verwaisten oder unzulässigen Beziehungen.
- Die Abschlussprüfung verwendet weiterhin die bestehenden Klassifikations- und Vorgangsdaten und umgeht keine fachlichen Sperren.
- Die relevanten lokalen Tests laufen erfolgreich und decken mindestens gültige Speicherung, ungültige Referenzen sowie atomare Fehlerbehandlung ab.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete technische Umsetzung und das Transaktionsverhalten anhand des vorhandenen Codes analysieren.
- Nur notwendige Korrekturen an der bestehenden Persistenz- und Verknüpfungslogik vornehmen.
- Keine produktiven Daten, Datenbanken außerhalb lokaler Testumgebungen oder externe Dienste verwenden.

## Manuelle Testhinweise

- Eine gültige Transaktion mit bestehendem Vorgang speichern und die Beziehung anschließend erneut laden.
- Eine Änderung mit ungültiger Vorgangsreferenz versuchen und prüfen, dass der vorherige Zustand erhalten bleibt.
- Eine zulässige Löschung ausführen und kontrollieren, dass keine verwaiste Beziehung zurückbleibt.
- Einen Abschlussversuch mit fehlenden Pflichtdaten ausführen und prüfen, dass weder Abschlussstatus noch Verknüpfungen unvollständig gespeichert werden.

## Offene Fragen

- Welche bestehenden Lösch- und Kaskadenregeln sind im Repository bereits verbindlich implementiert?
- Soll eine ungültige Verknüpfung ausschließlich abgelehnt oder zusätzlich mit einem strukturierten Fehlerstatus protokolliert werden?
