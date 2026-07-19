# Nächstes Arbeitspaket

## Titel

Vorgang beim Anlegen optional direkt abschließen

## Epic

**Epic-ID:** epic-vorgangsabschluss

**Epic-Titel:** Vorgänge beim Erstellen kontrolliert abschließen

**Epic-Ziel:** Vorgänge sollen bei ihrer Erstellung optional direkt in den abgeschlossenen Status überführt werden können, ohne die bestehende vorgangsbasierte Struktur zu umgehen.

**Teilpaket:** Teil 1

## Ziel

Beim Erstellen eines Vorgangs soll eine fachliche Option verfügbar sein, den Vorgang unmittelbar nach der Anlage in den abgeschlossenen Status zu überführen.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Eine fachliche Option zum kombinierten Anlegen und Abschließen eines Vorgangs vorsehen.
- Die bestehende vorgangsbasierte Struktur und vorhandene Vorgangsservices beziehungsweise Verknüpfungen weiterverwenden.
- Das bisherige Verhalten zum reinen Anlegen eines Vorgangs unverändert beibehalten.
- Die Abschlussaktion nur ausführen, wenn die neue Option ausdrücklich gewählt wurde.

## Soll umgesetzt werden

- Die neue Option in der bestehenden Erstellungsoberfläche beziehungsweise dem bestehenden Erstellungsfluss verständlich benennen.
- Erfolgreiches Anlegen und Abschließen sowie relevante Validierungs- oder Fehlerfälle durch Tests absichern.

## Nicht Teil dieses Arbeitspakets

- Kein grundsätzlicher Umbau der Vorgangs-, Beleg-, Transaktions- oder Verknüpfungsstrukturen.
- Keine Änderung bestehender Vorgänge oder nachträglicher Massenabschluss.
- Keine neuen externen Integrationen.
- Keine weiteren Status- oder Workflow-Erweiterungen über den direkten Abschluss beim Anlegen hinaus.

## Akzeptanzkriterien

- Ein Vorgang kann weiterhin ohne Abschlussoption angelegt werden und erhält dabei das bisherige Verhalten.
- Bei aktivierter Option wird der neue Vorgang in einem kontrollierten Ablauf angelegt und anschließend als abgeschlossen gespeichert.
- Die bestehende vorgangsbasierte Beziehung zwischen dem Vorgang und seinen Entitäten bleibt erhalten.
- Fehler beim Anlegen verhindern einen Abschluss eines nicht erfolgreich angelegten Vorgangs.
- Der kombinierte Anlege-und-Abschluss-Fluss ist durch automatisierte Tests abgedeckt.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete technische Änderungsstelle soll anhand der vorhandenen Erstellungslogik und Statusverwaltung ermittelt werden.
- Bestehende Statuswerte und Services sollen verwendet werden; keine parallele Abschlusslogik einführen.

## Manuelle Testhinweise

- Einen Vorgang ohne aktivierte Option anlegen und den bisherigen Anfangsstatus prüfen.
- Einen Vorgang mit aktivierter Option anlegen und den Status als abgeschlossen prüfen.
- Prüfen, dass die zugehörigen Entitäten weiterhin korrekt mit dem Vorgang verknüpft sind.

## Offene Fragen

- An welcher bestehenden Oberfläche oder API wird der Vorgang aktuell angelegt?
- Welcher vorhandene Statuswert beziehungsweise Abschlussservice ist für den Vorgangsabschluss maßgeblich?
