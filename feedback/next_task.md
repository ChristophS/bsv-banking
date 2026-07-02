# Nächstes Arbeitspaket

## Titel

Mail-Reiter: bestehende Vorgänge direkt einer Mail zuordnen

## Ziel

Im Mail-Reiter soll eine einzelne Mail vorhandenen Vorgängen zugeordnet und wieder entkoppelt werden können, unter Nutzung der bereits vorhandenen inbox_vorgaenge-Verknüpfung und der bestehenden API-Endpunkte.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/server.py
- banking_dashboard/mail_integration.py
- tests/test_dashboard.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Detailansicht bzw. Mail-Aktionen um Anzeige der verknüpften Vorgänge sowie Hinzufügen/Entfernen einer Zuordnung ergänzen.
- banking_dashboard/static/index.html: falls nötig einen kleinen Bereich für Vorgänge im Mail-Detail oder eine passende UI-Struktur ergänzen.
- banking_dashboard/server.py: nur falls das Frontend für die Auswahl oder Anzeige noch einen kleinen Zusatz-Response braucht; bestehende /api/mail/.../vorgaenge- und /api/vorgaenge/link-candidates-Endpunkte bevorzugen.
- banking_dashboard/mail_integration.py: nur falls vorhandene linked_vorgaenge-/link_vorgang-/unlink_vorgang-Responses für das UI minimale Anpassungen brauchen.
- tests/test_dashboard.py: API-Verhalten für Mail-Vorgangsverknüpfung und Link-Kandidaten absichern.
- tests/test_mail_integration.py: vorhandene MailManager-Verknüpfungslogik und eventuelle Response-Anpassungen prüfen.

## Muss umgesetzt werden

- Im Mail-Reiter für eine einzelne Mail die aktuell verknüpften Vorgänge sichtbar machen.
- Eine Bedienmöglichkeit ergänzen, um aus vorhandenen Vorgängen einen oder mehrere bestehende Vorgänge auszuwählen und der Mail zuzuordnen.
- Die bestehende Zuordnung muss auch wieder entfernbar sein.
- Nach Hinzufügen oder Entfernen muss die Anzeige ohne manuellen Reload konsistent aktualisiert werden.
- Fehler aus den bestehenden API-Aufrufen müssen im UI verständlich angezeigt werden, statt still zu scheitern.

## Soll umgesetzt werden

- Für die Auswahl vorhandener Vorgänge bevorzugt die bereits verfügbaren Link-Kandidaten nutzen, statt eine neue Gesamtvorgangsliste zu bauen.
- In der Anzeige mindestens Vorgangs-ID plus sinnvollen Bezug anzeigen, damit die Auswahl im Mail-Kontext verständlich ist.

## Nicht Teil dieses Arbeitspakets

- Mail automatisch einem passenden Vorgang vorschlagen oder per KI klassifizieren.
- Neue Vorgänge direkt aus der Mail in einem Klick vollständig erstellen und abschließen.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spam-Score-Korrekturen.
- Usability-Überarbeitung des manuellen Vorgangsabschlusses.

## Akzeptanzkriterien

- Beim Öffnen einer Mail sind bestehende Vorgangsverknüpfungen sichtbar.
- Ein Nutzer kann im Mail-Reiter einen vorhandenen Vorgang auswählen und die Mail damit verknüpfen.
- Nach erfolgreicher Verknüpfung erscheint der Vorgang sofort in der Mailansicht und ein erneuter GET auf /api/mail/<inbox_id>/vorgaenge liefert die Zuordnung.
- Ein Nutzer kann eine bestehende Verknüpfung wieder entfernen.
- Fehlende oder ungültige Vorgangs-IDs werden sauber als Fehler behandelt.
- Vorhandene Funktionalität zum Lesen, Taggen, Antworten und Löschen von Mails bleibt unverändert nutzbar.

## Hinweise für den Umsetzungs-Agenten

- Die Tabelle inbox_vorgaenge sowie GET/POST/DELETE unter /api/mail/<id>/vorgaenge sind bereits vorhanden und sollen direkt genutzt werden.
- DashboardDataStore bietet bereits /api/vorgaenge/link-candidates; diese bestehende Kandidatenquelle soll für die Auswahl wiederverwendet werden.
- Die Mail-Details werden bereits vom DashboardMailManager geladen; die neue Funktion sollte in diesen vorhandenen Mail-Detail-/Listen-Flow integriert werden.
- Vorgänge bleiben das zentrale Fachobjekt; es wird nur eine zusätzliche Zuordnung zu bestehenden Vorgängen ergänzt.
- Auf die stabile inbox_id achten, nicht nur auf technische Graph-IDs.
- UI bewusst klein halten: ein einfacher Auswahlbereich im Mail-Detail reicht.

## Manuelle Testhinweise

- Dashboard starten und den Mail-Reiter öffnen.
- Eine Mail auswählen und prüfen, dass vorhandene Vorgangsverknüpfungen angezeigt werden.
- Einen bestehenden Vorgang zuordnen und prüfen, dass die Verknüpfung sofort sichtbar ist.
- Seite neu laden und prüfen, dass die Verknüpfung bestehen bleibt.
- Verknüpfung wieder entfernen und Persistenz erneut prüfen.
- Negativtest: ungültige Vorgangs-ID oder Backend-Fehler auslösen und prüfen, dass eine verständliche Fehlermeldung erscheint.

## Offene Fragen

- Wenn die aktuelle Frontend-Struktur eher eine Mail-Zeile als eine Detailansicht nutzt: soll die Zuordnung nur in der Detailansicht oder auch direkt in der Listenzeile möglich sein? Für dieses Paket reicht die Detailansicht.
- Falls /api/vorgaenge/link-candidates sehr viele Einträge liefert: ist eine einfache clientseitige Filterung ausreichend? Für dieses kleine Paket ja, solange die UI bedienbar bleibt.
