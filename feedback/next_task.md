# Nächstes Arbeitspaket

## Titel

Spielerprämien: DFBnet-Ergebnisliste vollständig paginieren und fehlende Spieltage melden

## Epic

**Epic-ID:** epic-player-premiums

**Epic-Titel:** Spielerprämien vollständig und zuverlässig ermitteln

**Epic-Ziel:** Spielerprämien für alle relevanten Mannschaften und Spieltage vollständig aus den verfügbaren Ergebnisdaten ermitteln, prüfen und für die weitere Vorgangsbearbeitung bereitstellen.

**Teilpaket:** Teil 1

## Ziel

Die Spielerprämienauswertung soll für jede ausgewählte Mannschaft alle verfügbaren Seiten der DFBnet-Ergebnisliste verarbeiten und fehlende Meisterschafts-Spieltage, insbesondere bei BSV - Damen, zuverlässig melden.

## Relevante Dateien

- banking_dashboard/player_premiums.py
- tests/test_player_premiums.py

## Wahrscheinliche Änderungsstellen

- DFBnet-Ergebnislisten- und Seitennavigationslogik
- Vollständigkeitsprüfung der Meisterschafts-Spieltage
- Automatisierte Tests mit lokalen Mock- oder Fixture-Daten

## Muss umgesetzt werden

- Alle verfügbaren Seiten einer paginierten Ergebnisliste müssen verarbeitet werden.
- Doppelte Ergebnisse über mehrere Seiten dürfen die Auswertung nicht verfälschen.
- Fehlende Meisterschafts-Spieltage müssen je Mannschaft zuverlässig erkannt werden.
- Die bestehende Warnung mit den fehlenden Spieltagen muss verständlich erhalten oder verbessert werden.
- Die Prüfung muss ohne echte DFBnet-Aktion durch lokale Mocks oder Fixtures testbar sein.

## Soll umgesetzt werden

- Die Seitenerkennung soll bei unveränderten oder wiederholten Seiten sicher abbrechen.
- Die Reihenfolge der ausgewerteten Spiele soll deterministisch bleiben.
- Die Tests sollen mindestens eine vollständige mehrseitige Liste, eine Liste mit ausgelassenen Spieltagen und doppelte Ergebnisse abdecken.

## Nicht Teil dieses Arbeitspakets

- Echte produktive DFBnet-Zugriffe oder neue externe Aktionen
- Auszahlung, Überweisung oder Lastschrift von Spielerprämien
- Änderungen an Mail-, Transaktions-, Adress- oder allgemeiner Vorgangs-UI
- Die vollständige fachliche Ausgestaltung weiterer Spielerprämien-Teilpakete

## Akzeptanzkriterien

- Eine lokale Fixture mit mindestens zwei Ergebnislistenseiten wird vollständig verarbeitet.
- Ein Spiel, das ausschließlich auf einer Folgeseite steht, erscheint in der Auswertung.
- Für eine Fixture mit fehlenden Spieltagen werden genau die fehlenden Spieltage je Mannschaft ausgewiesen.
- Für eine vollständige Fixture wird keine Fehlermeldung zu fehlenden Spieltagen erzeugt.
- Doppelte Ergebniszeilen oder wiederholte Seitendaten führen nicht zu doppelten Spielen.
- Die bestehenden Spielerprämien-Tests und die neuen Pagination-Tests sind erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Die bestehende _collect_matches- und _go_to_next_page-Logik soll möglichst gezielt erweitert oder abgesichert werden.
- Erwartete Spieltage sollen weiterhin aus den tatsächlich vorhandenen Meisterschafts-Spieltagsnummern abgeleitet werden; Pokal- und Freundschaftsspiele dürfen die Prüfung nicht verfälschen.
- Keine Credentials, Tokens oder produktiven Laufzeitdaten verwenden.

## Manuelle Testhinweise

- Eine lokale Mock-Sequenz mit zwei Ergebnislistenseiten und einem Spieltag auf der zweiten Seite ausführen.
- Eine lokale Fixture für BSV - Damen mit ausgelassenen Spieltagen prüfen und die Warnung mit den erwarteten Spieltagen vergleichen.

## Offene Fragen

- Ob DFBnet bei bestimmten Ergebnislisten eine numerische Seitennavigation ohne zuverlässige aktuelle Seitennummer liefert, kann der Coding-Agent anhand der vorhandenen Selektoren klären.
- Die fachlich erwartete Saisonlänge beziehungsweise eine Prüfung auf Spieltage außerhalb des beobachteten Bereichs bleibt für ein späteres Teilpaket offen.
