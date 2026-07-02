# Nächstes Arbeitspaket

## Titel

Manuellen Vorgangsabschluss im Dashboard sichtbarer und direkter bedienbar machen

## Ziel

Der vorhandene manuelle Abschluss von Vorgängen soll im Vorgangsdetail klar erkennbar und intuitiv auslösbar sein, ohne die bestehende Abschlussprüfung oder Automatik zu verändern.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Vorgangsdetail-Rendering und Event-Handling für Abschluss/Wiederöffnen an einer prominenteren Stelle anpassen.
- banking_dashboard/static/index.html: Falls nötig, strukturellen Platzhalter oder semantische Reihenfolge im Vorgangsdetailbereich verbessern.
- banking_dashboard/static/styles.css: Sichtbarkeit, Hierarchie und Platzierung des Status-/Abschlussbereichs verbessern.
- tests/test_dashboard.py: API- und ggf. HTML/JS-bezogene Dashboard-Tests für den manuellen Statuswechsel prüfen und erweitern.
- banking_dashboard/server.py: Nur falls für die UI ein vorhandenes Detailfeld sauberer exponiert werden muss; keine neue Statuslogik einbauen.

## Muss umgesetzt werden

- Im Vorgangsdetail einen klar sichtbaren primären Bedienpunkt für 'Vorgang abschließen' bzw. 'Vorgang wieder öffnen' an prominenter Stelle anbieten, statt versteckt im mittleren Formularfluss.
- Den sichtbaren Status des Vorgangs im selben Bereich klar anzeigen und den Buttontext am aktuellen Zustand ausrichten.
- Wenn abschluss_moeglich false ist, den Abschluss-Button nicht irreführend als normale Hauptaktion darstellen, sondern den blockierten Zustand mit nachvollziehbarem Hinweis aus abschluss_blocker anzeigen.
- Beim manuellen Statuswechsel weiterhin den bestehenden PATCH-Endpunkt /api/vorgaenge/<id>/status verwenden.
- Nach erfolgreichem Abschluss oder Wiederöffnen die Vorgangsdetailansicht und relevante Listen-/Zählerdaten aktualisieren, damit der neue Status sofort sichtbar ist.

## Soll umgesetzt werden

- Den Abschlussbereich visuell als eigenen Abschnitt oder Aktionsleiste hervorheben.
- Bei blockiertem Abschluss die vorhandenen Blocker kurz und gut lesbar direkt am Button oder im Statusbereich anzeigen statt nur indirekt über Fehlermeldungen.
- Die Bedienung für Wiederöffnen gleichwertig klar machen, nicht nur für Abschluss.

## Nicht Teil dieses Arbeitspakets

- Ein-Klick-Gesamtworkflow für Erstellen, Klassifikation und Abschluss.
- Mail direkt einem bestehenden Vorgang zuordnen.
- Spam-Score-Korrektur.
- Mehrfachzuordnung verschiedener Mail-Dokumente zu unterschiedlichen Transaktionen innerhalb eines Vorgangs.
- Änderung der fachlichen Voraussetzungen für Rechnungsvorgänge oder unvollständig klassifizierte Transaktionen.

## Akzeptanzkriterien

- Im Vorgangsdetail ist ohne Suchen erkennbar, ob der Vorgang in_bearbeitung oder abgeschlossen ist.
- Ein Nutzer kann einen abschließbaren Vorgang direkt über eine prominente Aktion manuell abschließen.
- Ein abgeschlossener Vorgang kann über eine ebenso klare Aktion wieder auf in_bearbeitung gesetzt werden.
- Ist ein Vorgang nicht abschließbar, bleibt die Aktion nachvollziehbar blockiert oder führt zu einer klaren Rückmeldung mit den vorhandenen Abschluss-Blockern.
- Der Statuswechsel nutzt weiterhin die bestehende Backend-Validierung; unzulässige Abschlüsse werden nicht stillschweigend durchgelassen.
- Vorhandene automatische Abschlussregeln funktionieren danach unverändert weiter.

## Hinweise für den Umsetzungs-Agenten

- Die API liefert bereits die für die UI nötigen Felder abschluss_moeglich und abschluss_blocker im Vorgangsdetail; diese sollten bevorzugt für die Darstellung genutzt werden statt Logik im Frontend zu duplizieren.
- Falls app.js derzeit nur einen generischen Bearbeitungsbereich hat, sollte der Abschluss/Wiederöffnen-Bedienpunkt im Rendering des Vorgangsdetails nach oben gezogen werden, nahe Titel/Status.
- Der manuelle Abschluss sollte über den spezialisierten Status-Endpunkt laufen, nicht über allgemeines update_vorgang() mit completed-Feld, damit die bestehende Semantik klar bleibt.
- Wenn bereits Toasts/Fehleranzeigen im Frontend existieren, diese für blockierte Abschlüsse wiederverwenden statt neue Benachrichtigungssysteme zu bauen.

## Manuelle Testhinweise

- Dashboard starten, Vorgang mit vollständig klassifizierten Transaktionen öffnen und prüfen, dass der Abschluss-Button sofort sichtbar ist und den Status auf abgeschlossen setzt.
- Danach denselben Vorgang wieder öffnen und prüfen, dass 'Wieder öffnen' ebenso klar sichtbar ist.
- Vorgang mit unvollständiger Klassifikation öffnen und prüfen, dass Abschluss nicht möglich ist und die UI die Blocker verständlich zeigt.
- Falls vorhanden: Rechnungsvorgang ohne Beleg oder ohne Transaktion prüfen und sicherstellen, dass die bestehenden Blocker weiterhin angezeigt werden.
- Nach Statuswechsel prüfen, dass Vorgangsdetail, Vorgangsliste und Übersichtskarten konsistent aktualisiert werden.

## Offene Fragen

- Keine Angaben
