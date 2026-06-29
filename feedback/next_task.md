# Nächstes Arbeitspaket

## Titel

Vorschläge nur für bestehende Verknüpfungen vorselektieren

## Ziel

Beim Erstellen und Bearbeiten von Vorgängen sollen Vorschläge weiterhin priorisiert angezeigt werden, aber nicht mehr automatisch angehakt werden. Vorausgewählt bleiben nur bereits bestehende bzw. aus der aktuellen Quelle stammende Verknüpfungen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: createSuggestionSection(...) enthält die Auto-Auswahl per checkbox.checked = Boolean(item.selected) || (autoSelect && Number(item.score || 0) >= 0.45). Hier soll die automatische Auswahl anhand des Scores entfernt werden.
- banking_dashboard/static/app.js: renderVorgangCreateForm(...) nutzt createSuggestionSection(...) für Mails, Transaktionen, To-Dos, Dokumente und Termine; prüfen, dass nur sourceLinkPayload(...) markiert bleibt.
- banking_dashboard/static/app.js: renderMailVorgangReview(...) nutzt createSuggestionSection(...) für 'Weitere Mails verknüpfen'; hier sollen nur die aktuell importierte Mail bzw. bereits verknüpfte Einträge angehakt sein.
- banking_dashboard/static/app.js: createVorgangMetadataEditor(...) muss bestehende Verknüpfungen weiterhin als selectedIds anzeigen, ohne neue Vorschläge vorzuselektieren.
- tests/test_dashboard.py: bestehende Dashboard-/API-Tests auf Payload-Verhalten prüfen bzw. ergänzen, damit nur explizit ausgewählte IDs gesendet werden.

## Muss umgesetzt werden

- Die automatische Checkbox-Auswahl aufgrund von Vorschlags-Score entfernen.
- Bereits bestehende Verknüpfungen und die aktuelle Quelle weiterhin vorauswählen.
- Priorisierte Sortierung der Vorschläge erhalten.
- Sicherstellen, dass beim Absenden nur angehakte IDs an das Backend gesendet werden.
- Bestehende Verknüpfungen beim Bearbeiten eines Vorgangs nicht unbeabsichtigt entfernen.

## Soll umgesetzt werden

- Falls der Parameter autoSelect nach der Änderung irreführend ist, ihn entfernen oder so umbenennen, dass klar nur bestehende Verknüpfungen damit gemeint sind.
- Falls sinnvoll, eine kleine Hilfsfunktion einführen, die 'bereits ausgewählt' und 'nur Vorschlag' klar trennt.

## Nicht Teil dieses Arbeitspakets

- Spam-Score-Berechnung reparieren.
- Neue Vorschlagslogik oder bessere Matching-Scores entwickeln.
- Ein-Klick-Vorgang anlegen und erledigen inklusive Transaktionsklassifikation.
- Vorgänge manuell schließen oder den Abschluss-Button neu platzieren.
- Mail direkt einem bestehenden Vorgang zuordnen.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen zuordnen.
- Spendenbescheinigungen und DFBnet-Verein-Automation umsetzen.
- Grundlegendes Dashboard-Redesign.

## Akzeptanzkriterien

- Beim Erstellen eines Vorgangs aus einer Mail ist nur die auslösende Mail angehakt; weitere Mails werden nur als Vorschläge angezeigt.
- Beim manuellen Erstellen eines Vorgangs sind vorgeschlagene Entitäten nicht automatisch angehakt.
- Beim Bearbeiten eines bestehenden Vorgangs bleiben bereits verknüpfte Mails, Transaktionen, To-Dos, Dokumente und Termine angehakt.
- Das Speichern sendet nur tatsächlich angehakte IDs an das Backend.
- Die Sortierung der Vorschläge bleibt erhalten.

## Hinweise für den Umsetzungs-Agenten

- Der zentrale Fix liegt wahrscheinlich in createSuggestionSection(...): Die Checkbox darf nicht mehr wegen autoSelect && score >= 0.45 aktiviert werden.
- selectedIds werden bereits in ein Set übernommen und item.selected wird für passende Einträge gesetzt; diese Mechanik sollte für Quell- und Bestandsverknüpfungen genutzt werden.
- sourceLinkPayload(source) liefert z.B. mail_ids: [source.id] und muss weiterhin als Vorauswahl wirken.
- createVorgangMetadataEditor(vorgang, ...) sollte bestehende IDs aus vorgang.transaktionen, vorgang.mails, vorgang.todos, vorgang.belege und vorgang.termine weiterhin markieren.
- compareSuggestionItems(...) und die bestehende Priorisierung sollen nicht entfernt werden.

## Manuelle Testhinweise

- Dashboard starten und im Mail-Reiter eine Mail öffnen.
- Auf 'Vorgang erstellen' klicken und prüfen: Nur die aktuelle Mail ist angehakt, weitere Vorschläge nicht.
- Einen bestehenden Vorgang mit vorhandenen Links öffnen und prüfen: Diese Links sind angehakt, neue Vorschläge nicht.
- Ein Formular speichern und prüfen, dass nur explizit angehakte Verknüpfungen übernommen wurden.

## Offene Fragen

- Soll zusätzlich ein Hinweis wie 'Vorschläge sind nicht automatisch ausgewählt' angezeigt werden?
