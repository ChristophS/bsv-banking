# Nächstes Arbeitspaket

## Titel

Mail-Reiter: bestehende Zuordnung zu vorhandenem Vorgang sichtbar und direkt nutzbar machen

## Ziel

Im Mail-Reiter soll eine Mail einem bestehenden Vorgang direkt zugeordnet werden können, ohne den Mail-Import-Flow zu benutzen. Die vorhandenen Backend-Endpunkte und die Tabelle inbox_vorgaenge sollen dafür in der UI klar verfügbar gemacht werden.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/mail_integration.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Detailansicht um Liste bereits verknüpfter Vorgänge plus UI zum Hinzufügen/Entfernen einer Vorgangszuordnung ergänzen.
- banking_dashboard/static/index.html: falls nötig Container/Bedienelemente für den neuen Bereich im Mail-Detail ergänzen.
- banking_dashboard/server.py: nur falls für die UI noch kleine Antwortanpassungen oder Fehlerbehandlung fehlen; bevorzugt bestehende Endpunkte unverändert nutzen.
- banking_dashboard/mail_integration.py: nur falls die Rückgabe von linked_vorgaenge, link_vorgang oder unlink_vorgang für die UI nicht ausreichend strukturiert ist.
- tests/test_dashboard.py: API-Tests für bestehende Mail-Vorgang-Endpunkte und ggf. Response-Formate absichern/ergänzen.
- tests/test_mail_integration.py: Verknüpfungslogik zwischen Mail und Vorgang absichern, falls dort bereits Mail-Manager-Verhalten getestet wird.

## Muss umgesetzt werden

- Im Mail-Reiter in der Detailansicht einen klar sichtbaren Bereich für Zugeordnete Vorgänge anzeigen.
- Beim Öffnen einer Mail die bereits verknüpften Vorgänge über den bestehenden GET-Endpunkt laden und anzeigen.
- Eine bestehende Mail über den vorhandenen POST-Endpunkt einem bereits existierenden Vorgang zuordnen können.
- Eine bestehende Zuordnung über den vorhandenen DELETE-Endpunkt wieder lösen können.
- Für das Hinzufügen eine nutzbare Auswahl vorhandener Vorgänge anbieten; mindestens per bestehender Vorgangsliste, idealerweise mit Suche/Filter auf vorhandene Daten statt Freitext-IDs.
- Nach Hinzufügen oder Entfernen die Anzeige ohne Seitenreload aktualisieren.
- Fehler aus API-Aufrufen im Mail-Reiter verständlich anzeigen.

## Soll umgesetzt werden

- In der Vorgangsauswahl abgeschlossene und offene Vorgänge erkennbar machen.
- Die Anzeige so bauen, dass die stabile vorgangs_id sichtbar bleibt, aber nicht das einzige Orientierungskriterium ist.
- Falls einfach möglich, beim Öffnen der Auswahl die bestehenden /api/vorgaenge-Daten oder Link-Kandidaten wiederverwenden statt eine neue Spezial-API zu bauen.

## Nicht Teil dieses Arbeitspakets

- Automatische Vorgangserstellung aus Mails
- Ein-Klick-Workflow zum sofortigen Anlegen und Abschließen eines Vorgangs
- Mehrere Dokumente einer Mail verschiedenen Transaktionen innerhalb eines Vorgangs zuordnen
- Spam-Score-Korrekturen
- Größere Dashboard-Usability-Überarbeitung
- Umbau der Abschlusslogik für Vorgänge

## Akzeptanzkriterien

- In der Mail-Detailansicht sind bestehende Vorgangszuordnungen sichtbar.
- Ein Nutzer kann aus dem Mail-Reiter heraus eine Mail einem vorhandenen Vorgang zuordnen, ohne den Import-Flow zu verwenden.
- Ein Nutzer kann eine bestehende Mail-Vorgang-Zuordnung wieder entfernen.
- Die UI nutzt dafür bestehende Backend-Flows; es wird keine parallele neue Verknüpfungslogik eingeführt.
- Vorhandene Tests laufen weiter und mindestens ein Test deckt den Mail-Vorgang-Link-Flow zusätzlich ab.

## Hinweise für den Umsetzungs-Agenten

- README und Servercode zeigen, dass die Funktion fachlich schon vorgesehen ist; der Feedbackpunkt ist daher sehr wahrscheinlich primär ein Sichtbarkeits-/UX-Problem im Mail-Reiter.
- Im Server existiert bereits GET /api/vorgaenge für Kandidaten und GET/POST/DELETE für Mail-Vorgangslinks. Bevor neue Endpunkte gebaut werden, prüfen, ob die UI vollständig damit auskommt.
- Falls mail_manager.linked_vorgaenge(...) aktuell nur IDs liefert, ist eine kleine Response-Verbesserung vertretbar, aber nur wenn nötig und ohne neues Modell.
- Wenn bereits Komponenten/Renderfunktionen für verknüpfte Entitäten in app.js existieren, diese wiederverwenden statt einen separaten Spezialdialog zu bauen.
- Der Import-Button für vorgang-import sollte fachlich klar von bestehendem Vorgang zuordnen getrennt bleiben, damit kein unbeabsichtigtes Anlegen neuer Vorgänge passiert.

## Manuelle Testhinweise

- Dashboard starten, Mail-Reiter öffnen, eine geladene Mail anklicken und prüfen, ob der Bereich Zugeordnete Vorgänge sichtbar ist.
- Eine Mail einem bereits existierenden offenen Vorgang zuordnen und kontrollieren, dass die Zuordnung sofort in der UI erscheint.
- Die gleiche Zuordnung erneut versuchen und prüfen, dass kein doppelter Link entsteht.
- Die Zuordnung wieder entfernen und prüfen, dass sie sofort verschwindet.
- Eine Mail einem abgeschlossenen Vorgang zuordnen, falls erlaubt, und Statusdarstellung prüfen.
- Fehlerfall testen, z. B. wenn ein Vorgang zwischenzeitlich gelöscht wurde oder eine ungültige ID gesendet wird.

## Offene Fragen

- Ist die Vorgangszuordnung im Mail-Reiter komplett unsichtbar oder nur zu versteckt? Das Arbeitspaket sollte in beiden Fällen auf Sichtbarkeit und Direktnutzung zielen.
- Liefert mail_manager.linked_vorgaenge(...) bereits genug Metadaten für eine gute Anzeige, oder nur IDs?
