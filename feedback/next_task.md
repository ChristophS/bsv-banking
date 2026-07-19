# Nächstes Arbeitspaket

## Titel

Fehlende Spieltage bei Spielerprämien durch vollständige Ergebnislisten-Abfrage beheben

## Epic

**Epic-ID:** epic-player-premiums

**Epic-Titel:** Spielerprämien vollständig und zuverlässig ermitteln

**Epic-Ziel:** Spielerprämien aus den verfügbaren Spielergebnisdaten vollständig, nachvollziehbar und zuverlässig ermitteln und für die weitere Vorgangsbearbeitung bereitstellen.

**Teilpaket:** Teil 1

## Ziel

Die Spielerprämienermittlung soll alle relevanten DFBnet-Ergebnisse einschließlich der gemeldeten Spieltage 12 und 18 berücksichtigen und bei unvollständigen Ergebnislisten eine nachvollziehbare Warnung liefern.

## Relevante Dateien

- banking_dashboard/player_premiums.py
- tests/test_player_premiums.py

## Wahrscheinliche Änderungsstellen

- DFBnet-Ergebnislisten-Abfrage
- Pagination und Zusammenführung mehrerer Ergebnislistenseiten
- Vollständigkeitsprüfung der Spieltage
- Tests für mehrseitige Ergebnislisten

## Muss umgesetzt werden

- Die DFBnet-Ergebnisabfrage so korrigieren oder ergänzen, dass alle verfügbaren Ergebnislistenseiten verarbeitet werden.
- Sicherstellen, dass vorhandene Ergebnisse der Spieltage 12 und 18 nicht durch fehlerhafte Pagination oder eine zu frühe Abbruchbedingung verloren gehen.
- Die bestehende Berechnung, Spielerzuordnung und Prämienermittlung unverändert beibehalten, soweit sie nicht ursächlich für das Problem ist.
- Doppelte Ergebnisse bei der Zusammenführung mehrerer Seiten vermeiden.
- Automatisierte Tests für mehrseitige Ergebnislisten und fehlende Spieltage ergänzen oder anpassen.

## Soll umgesetzt werden

- Ein stabiles Abbruchverhalten für leere, unveränderte oder nicht mehr verfügbare Folgeseiten sicherstellen.
- Die bestehende Vollständigkeitswarnung so nutzen, dass fehlende Spieltage weiterhin klar erkennbar bleiben.

## Nicht Teil dieses Arbeitspakets

- Neue echte externe DFBnet-, Banking- oder Login-Aktionen ohne Mock, Fake oder Fixture.
- Mail-Funktionen und MailboxConcurrency- beziehungsweise Outlook-Fehler.
- Dashboard-Startseite, Tab-Navigation und Transaktionsansicht.
- Saldokorrekturen unter Transaktionen.
- Vorgangserstellung und die Option, einen Vorgang direkt abzuschließen.
- Allgemeine Erweiterungen der Spielerprämienlogik außerhalb der Ergebnislisten-Vollständigkeit.

## Akzeptanzkriterien

- Eine simulierte mehrseitige DFBnet-Ergebnisliste wird vollständig verarbeitet.
- Vorhandene Ergebnisse der Spieltage 12 und 18 erscheinen in der ermittelten Spiel- und Prämienauswertung.
- Eine einseitige Ergebnisliste funktioniert weiterhin.
- Doppelte Ergebnisse werden nicht doppelt in die Auswertung übernommen.
- Leere oder unveränderte Folgeseiten führen nicht zu einer Endlosschleife.
- Die Vollständigkeitsprüfung meldet tatsächlich fehlende Spieltage weiterhin nachvollziehbar.
- Alle Tests verwenden ausschließlich Mocks, Fakes oder Fixtures und greifen nicht auf DFBnet oder andere externe Dienste zu.

## Hinweise für den Umsetzungs-Agenten

- Die bestehende Funktion zur Seitennavigation und die vorhandene Deduplizierung sollen bevorzugt weiterverwendet und gezielt korrigiert werden.
- Die fachliche Zuordnung über bestehende Team- und Spielstrukturen bleibt unverändert.
- Technische Details der konkreten Selektoren und Mock-Strukturen kann der Coding-Agent anhand des Repositorys bestimmen.

## Manuelle Testhinweise

- Mit einem Fixture mit mindestens zwei Ergebnislistenseiten prüfen, dass alle Spieltage in der Auswertung erscheinen.
- Insbesondere kontrollieren, dass die Spieltage 12 und 18 nicht fehlen.
- Ein Fixture mit einer leeren Folgeseite und ein Fixture mit einer wiederholten Seite prüfen.

## Offene Fragen

- Ob die tatsächliche DFBnet-Seitennavigation über numerische Seiten, einen Weiter-Link oder eine andere Steuerung erfolgt, kann anhand von Fixtures und dem vorhandenen Code geklärt werden.
- Die produktive DFBnet-Abfrage darf nicht Bestandteil automatisierter Tests sein.
