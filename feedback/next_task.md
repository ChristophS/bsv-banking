# Nächstes Arbeitspaket

## Titel

Finanzübersicht: fehlende Zuordnungen und Belege aggregieren

## Epic

**Epic-ID:** epic-finanzuebersicht

**Epic-Titel:** Finanzübersicht für Kassenprüfung und Steuerberatung

**Epic-Ziel:** Eine periodenbezogene Finanzübersicht bereitstellen, die finanzielle Vollständigkeit, Klassifikationen, Belege, Kategorien und Transaktionsdetails für Kassenprüfung und Steuerberatung auswertbar macht.

**Teilpaket:** Teil 1

## Ziel

Die gewünschte Finanzübersicht soll zunächst für einen beliebigen Zeitraum fehlende Klassifizierungszuordnungen und fehlende Belege je Transaktion ausweisen.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Eine aktuelle Übersicht für einen beliebigen Zeitraum erstellen können.
- Man soll zunächst sehen welche Zuordnungen fehlen.
- Dann bei welchen Transaktionen Belege fehlen.

## Soll umgesetzt werden

- Die vorhandene Architektur und bestehende fachliche Verknüpfungen weiterverwenden.
- Die konkret betroffenen Repository-Dateien vor der Umsetzung selbstständig analysieren.
- Passende automatisierte Tests ergänzen oder vorhandene Tests gezielt erweitern.

## Nicht Teil dieses Arbeitspakets

- Keine weiteren unabhängigen Backlog-Punkte ungeplant mit umsetzen.
- Keine grundlegende neue Architektur ohne ausdrückliche fachliche Notwendigkeit einführen.
- Keine echten externen Aktionen oder produktiven Daten in Tests verwenden.

## Akzeptanzkriterien

- Das im Titel und Ziel beschriebene Verhalten ist vollständig umgesetzt.
- Die fachlichen Anforderungen aus dem Feedback sind erfüllt.
- Neue oder geänderte Logik ist durch passende lokale Tests abgesichert.
- Bestehende relevante Tests bleiben erfolgreich.
- Vorhandene zentrale Vorgangs- und Verknüpfungsstrukturen bleiben erhalten.

## Hinweise für den Umsetzungs-Agenten

- Codex analysiert die konkret betroffenen Dateien und technischen Änderungsstellen selbstständig.
- Vorgänge bleiben das zentrale fachliche Objekt.
- Bestehende Tabellen, Services und Verknüpfungen nicht grundlos umgehen oder ersetzen.

## Manuelle Testhinweise

- Nur lokale und sichere Tests durchführen.
- Externe Dienste ausschließlich mit Mocks, Fakes oder Fixtures prüfen.

## Offene Fragen

- Keine Angaben
