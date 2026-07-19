# Nächstes Arbeitspaket

## Titel

Transaktionsansicht ohne dominanten Saldokorrektur-Block anzeigen

## Epic

**Epic-ID:** epic-dashboard-navigation

**Epic-Titel:** Dashboard-Navigation und fachliche Übersichten entlasten

**Epic-Ziel:** Das Dashboard soll je Fachbereich unmittelbar die relevanten Inhalte zeigen, ohne dauerhaft sichtbare globale Blöcke als Sichtblocker.

**Teilpaket:** Teil 2

## Ziel

Beim Öffnen des Transaktionsbereichs sollen die Transaktionen unmittelbar sichtbar sein. Saldokorrekturen dürfen die Transaktionsliste nicht als dauerhaft dominanter Sichtblock verdrängen; der relevante Datenstand soll weiterhin erkennbar bleiben.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Die Transaktionsliste muss beim Öffnen des Transaktionsbereichs unmittelbar sichtbar sein.
- Die Darstellung der Saldokorrekturen darf die eigentliche Transaktionsliste nicht dauerhaft verdrängen.
- Der Datenstand beziehungsweise das Datum des zugrunde liegenden Datenstands muss weiterhin erkennbar sein.
- Die bestehende vorgangsbasierte Struktur und vorhandene Transaktionsdaten müssen weiterverwendet werden.

## Soll umgesetzt werden

- Die Saldokorrekturen platzsparend oder nachrangig darstellen, ohne ihren fachlichen Informationsgehalt zu verlieren.
- Die gewählte Darstellung konsistent in die bestehende Dashboard-Navigation und das vorhandene Layout integrieren.

## Nicht Teil dieses Arbeitspakets

- Keine Änderung der Transaktionsimport- oder Saldenberechnungslogik.
- Keine Einführung einer direkten Ersatzbeziehung außerhalb der bestehenden Vorgangsstrukturen.
- Keine fachliche Neugestaltung oder Erweiterung der Saldokorrekturen.
- Keine Bearbeitung unabhängiger Mail- oder Vorgangsabschluss-Themen.

## Akzeptanzkriterien

- Beim Aufruf der Transaktionsansicht ist die Transaktionsliste ohne vorheriges Wegklicken eines großen Saldokorrektur-Blocks sichtbar.
- Saldokorrekturen bleiben auffindbar und werden nicht aus dem fachlichen Bereich entfernt.
- Ein Nutzer kann den relevanten Datenstand beziehungsweise dessen Datum in der Transaktionsansicht erkennen.
- Bestehende Transaktions- und Vorgangsfunktionen bleiben nutzbar.
- Für die angepasste Darstellung existieren passende automatisierte Tests oder bestehende Tests werden entsprechend erweitert.

## Hinweise für den Umsetzungs-Agenten

- Die konkrete UI-Umsetzung soll sich an der vorhandenen Dashboard-Struktur orientieren.
- Keine neuen externen Dienste oder produktiven Datenquellen verwenden.

## Manuelle Testhinweise

- Transaktionsansicht öffnen und prüfen, dass die Transaktionsliste sofort im sichtbaren Bereich erscheint.
- Prüfen, dass Saldokorrekturen weiterhin erreichbar und verständlich dargestellt sind.
- Prüfen, dass der Datenstand beziehungsweise das Datum sichtbar ist.

## Offene Fragen

- Welche bestehende Darstellung der Saldokorrekturen bietet sich im aktuellen UI am besten als kompakter oder nachrangiger Bereich an?
