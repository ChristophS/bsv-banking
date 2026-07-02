# Nächstes Arbeitspaket

## Titel

Mail-Reiter: bestehende Vorgänge direkt einer Mail zuordnen

## Ziel

Im Mail-Reiter soll eine Mail einem bereits vorhandenen Vorgang zugeordnet und diese Zuordnung wieder entfernt werden können. Dafür werden die vorhandenen inbox_vorgaenge-API-Endpunkte und die bestehende Vorgangsliste genutzt, ohne neue Vorgangsarchitektur einzuführen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/mail_integration.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Detailansicht um Anzeige bestehender Vorgangszuordnungen, Auswahl bestehender Vorgänge und Aktionen zum Zuordnen/Entfernen erweitern.
- banking_dashboard/static/index.html: falls nötig Container/Platzhalter für die Zuordnungssektion im Mail-Bereich ergänzen.
- banking_dashboard/server.py: prüfen, ob die bestehenden /api/mail/<id>/vorgaenge-Antworten für die UI ausreichen; falls nötig Antwortformat repo-konform ergänzen.
- banking_dashboard/mail_integration.py: nur anpassen, wenn die Link-Methoden für die UI noch nicht genügend Vorgangsdaten oder Fehlerinfos zurückgeben.
- tests/test_dashboard.py: API-Tests für Mail-Vorgangszuordnung ergänzen oder präzisieren.
- tests/test_mail_integration.py: Link/Unlink-Fälle und Rückgabeformate absichern.

## Muss umgesetzt werden

- Im Mail-Reiter für eine ausgewählte Mail die bereits verknüpften Vorgänge sichtbar machen.
- Eine UI bereitstellen, mit der ein vorhandener Vorgang aus dem bestehenden Bestand ausgewählt und der Mail zugeordnet werden kann.
- Eine bestehende Mail-Vorgangszuordnung in der UI wieder entfernbar machen.
- Nach Zuordnung oder Entfernung die Mail-Ansicht ohne manuellen Reload konsistent aktualisieren.
- Fehlerfälle der API verständlich anzeigen, wenn Mail oder Vorgang nicht gefunden wurde.

## Soll umgesetzt werden

- Für die Auswahl vorhandener Vorgänge möglichst die bestehende Vorgangsliste oder vorhandene Link-Kandidaten verwenden.
- Die Anzeige im Mail-Reiter so gestalten, dass Vorgangs-ID, Titel/Bezug und Status erkennbar sind.
- Doppelte Zuordnungen in der UI sauber behandeln, passend zur vorhandenen Idempotenz.

## Nicht Teil dieses Arbeitspakets

- Automatische Vorgangserstellung aus Mails.
- Ein-Klick-Workflow für Erstellen, Klassifikation und Abschluss eines Vorgangs.
- Zuordnung mehrerer Mail-Dokumente zu unterschiedlichen Transaktionen innerhalb eines Vorgangs.
- Spam-Score-Analyse und Korrektur.
- Größere Dashboard-Usability-Überarbeitung außerhalb dieses konkreten Mail-Flows.

## Akzeptanzkriterien

- Für eine Mail im Mail-Reiter werden bestehende Vorgangszuordnungen angezeigt.
- Ein Benutzer kann aus dem Mail-Reiter einen vorhandenen Vorgang auswählen und der Mail zuordnen.
- Nach erfolgreicher Zuordnung erscheint der Vorgang direkt in der Mail-Ansicht als verknüpft.
- Ein Benutzer kann eine vorhandene Zuordnung wieder entfernen, und die Anzeige aktualisiert sich sofort.
- Ein erneuter Zuordnungsversuch desselben Vorgangs erzeugt keine doppelte Verknüpfung und keinen inkonsistenten UI-Zustand.
- Die API-Tests für Mail-Vorgangszuordnung laufen grün.

## Hinweise für den Umsetzungs-Agenten

- Der Server hat bereits GET/POST/DELETE-Routen unter /api/mail/.../vorgaenge; zuerst prüfen, ob deren Rückgabeformat für die UI schon reicht, bevor zusätzliche Endpunkte ergänzt werden.
- Da /api/vorgaenge/link-candidates bereits existiert, kann diese Liste wahrscheinlich als Auswahlquelle dienen; alternativ kann /api/vorgaenge mit Suche genutzt werden.
- Die Mail-UI sollte die neue Zuordnungssektion in den bestehenden Detailbereich integrieren, nicht als neuen separaten Screen.
- Wenn mail_manager.link_vorgang/unlink_vorgang aktuell nur minimale Daten liefern, lieber das Rückgabeformat leicht anreichern als einen komplett neuen Flow einzuführen.
- Auf Konsistenz mit vorgang_detail/_mails_for_vorgang achten: Eine Mail-Zuordnung soll auch aus Sicht des Vorgangsmodells sauber sichtbar bleiben.

## Manuelle Testhinweise

- Dashboard starten, Mail-Reiter öffnen, eine geladene Mail auswählen und prüfen, ob der Bereich für verknüpfte Vorgänge sichtbar ist.
- Einen bestehenden offenen Vorgang auswählen und verknüpfen; danach prüfen, ob die Zuordnung in der Mail sichtbar ist.
- Optional in den Vorgangsdetails desselben Vorgangs gegenprüfen, ob die Mail dort ebenfalls erscheint.
- Die Zuordnung wieder entfernen und prüfen, ob sie in der Mail-Ansicht verschwindet.
- Denselben Vorgang erneut zuordnen und verifizieren, dass keine Dublette angezeigt wird.

## Offene Fragen

- Falls sowohl /api/vorgaenge als auch /api/vorgaenge/link-candidates als Datenquelle geeignet sind: Welche davon liefert im aktuellen Frontend mit dem geringsten Zusatzaufwand die bessere Auswahl-UX?
- Soll die UI nur eine einfache Auswahl bestehender Vorgänge bieten, oder zusätzlich Vorschläge/Kandidaten hervorheben, sofern diese mit wenig Aufwand aus vorhandener Logik nutzbar sind?
