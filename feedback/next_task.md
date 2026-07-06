# Nächstes Arbeitspaket

## Titel

Mail aus dem Maileingang einem bestehenden Vorgang zuordnen

## Ziel

Die Mail-Oberfläche so ergänzen, dass eine Mail direkt aus dem Maileingang einem bereits vorhandenen Vorgang zugeordnet werden kann, ohne einen neuen Vorgang anzulegen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/server.py
- banking_dashboard/mail_integration.py
- tests/test_dashboard.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Liste und/oder Mail-Detailansicht um eine Aktion zum Verknüpfen mit bestehendem Vorgang ergänzen; Kandidaten laden und POST/DELETE auslösen.
- banking_dashboard/static/index.html: nur falls für Auswahl/მენü ein kleines UI-Element oder Dialog-Container benötigt wird.
- banking_dashboard/server.py: vorhandene Mail-Vorgang-Endpunkte und Kandidaten-APIs prüfen; nur bei Bedarf kleine Response-Anpassungen für die UI.
- banking_dashboard/mail_integration.py: bestehende Rückgaben für verknüpfte Vorgänge nur dann ergänzen, wenn die UI zusätzliche Felder benötigt.
- tests/test_dashboard.py: API-Verhalten für Mail/Vorgang-Verknüpfung absichern.
- tests/test_mail_integration.py: Verknüpfen und Entfernen von Vorgängen an einer Mail absichern.

## Muss umgesetzt werden

- In der Mail-Ansicht eine klar erkennbare Möglichkeit bereitstellen, einen bestehenden Vorgang auszuwählen und mit der Mail zu verknüpfen.
- Dafür die bereits vorhandenen Backend-Endpunkte und Kandidatenlisten verwenden, statt neue Zuordnungslogik einzuführen.
- Nach erfolgreicher Verknüpfung die verknüpften Vorgänge in der UI sofort aktualisiert anzeigen.
- Doppelte Zuordnungen desselben Vorgangs zu derselben Mail verhindern oder robust ignorieren.
- Die bestehende Funktion zum Erstellen eines neuen Vorgangs aus einer Mail unverändert lassen.

## Soll umgesetzt werden

- Wenn bereits eine Mail-Detailansicht existiert, den Flow dort möglichst kompakt integrieren.
- Falls eine Vorgangssuche bereits im Frontend existiert, diese für die Auswahl wiederverwenden.

## Nicht Teil dieses Arbeitspakets

- Automatisches Markieren von Mails als gelesen.
- Erstellen neuer To-Dos ohne Vorschlag.
- Aktuellste Transaktionen im Mail-basierten Vorgangsanlegen verfügbar machen.
- Mehrere Anhänge einer Mail in der Vorgangsanlage sichtbar machen.
- Button-Text und Position beim Vorgangsanlegen aus Mail ändern.
- Fehlbuchungs-Flow für Nullung und Abschluss.
- Mail-Senden mit Zeilenumbrüchen und Empfängerauswahl verbessern.
- Dashboard-Startseite mit Synchronisieren-Button.
- Sortierung offener Vorgänge vor abgeschlossenen Vorgängen.

## Akzeptanzkriterien

- Für eine Mail im Reiter Mails kann ein bestehender Vorgang ausgewählt und verknüpft werden, ohne einen neuen Vorgang anzulegen.
- Nach dem Verknüpfen zeigt die UI den verknüpften Vorgang direkt bei der Mail an.
- Ein erneuter Verknüpfungsversuch mit demselben Vorgang erzeugt keine doppelte Zuordnung und keinen fehlerhaften UI-Zustand.
- Die bestehende API für Mail/Vorgang-Verknüpfungen bleibt nutzbar und ist durch Tests abgesichert.
- Das bestehende Verhalten zum Erstellen eines neuen Vorgangs aus einer Mail bleibt unverändert.

## Hinweise für den Umsetzungs-Agenten

- Es existiert bereits eine Verknüpfungstabelle für Mails und Vorgänge; diese sollte weiterverwendet werden.
- Die bestehenden Endpunkte zum Verknüpfen und Lösen von Verknüpfungen sind die primäre Integrationsstelle.
- Die UI sollte möglichst klein bleiben: lieber kompakter Auswahl-/Dialogflow als großer Umbau der Mail-Ansicht.
- Nach POST oder DELETE sollte der bestehende Refresh-Pfad für die Mail-Detailansicht genutzt werden, statt lokalen Zustand separat zu pflegen.

## Manuelle Testhinweise

- Mail im Maileingang öffnen, bestehenden Vorgang auswählen und verknüpfen.
- Prüfen, dass der verknüpfte Vorgang sofort in der Mailansicht erscheint.
- Denselben Vorgang erneut verknüpfen und prüfen, dass kein Duplikat entsteht.
- Verknüpfung wieder entfernen und prüfen, dass sie verschwindet.
- Prüfen, dass das Anlegen eines neuen Vorgangs aus der Mail weiterhin funktioniert.

## Offene Fragen

- Soll die Zuordnung direkt aus der Mail-Liste oder nur aus der Mail-Detailansicht startbar sein?
- Reicht eine Auswahl aus vorhandenen Kandidaten oder ist zusätzlich eine clientseitige Suche in der Auswahl nötig?
