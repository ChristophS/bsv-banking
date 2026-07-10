# Nächstes Arbeitspaket

## Titel

Mailbasierte Vorgangsanlage: aktuelle Transaktionen in den Verknüpfungs-Kandidaten sichtbar machen

## Ziel

Sicherstellen, dass beim Anlegen eines Vorgangs aus einer Mail die neuesten Transaktionen aus dem aktuellen Datenbankstand als Verknüpfungs-Kandidaten verfügbar sind und keine veraltete Kandidatenliste hängen bleibt.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Dialog für die Vorgangsanlage lädt oder cached vermutlich Kandidatenlisten; hier Nachladen/Neuabruf der Transaktionskandidaten beim Öffnen des Dialogs oder vor dem Absenden ergänzen.
- banking_dashboard/server.py: Falls für den Mail-Flow ein spezieller Kandidatenabruf oder Cache existiert, die vorhandene Kandidatenlogik so nutzen, dass immer der aktuelle DB-Stand ausgeliefert wird.
- banking_dashboard/static/index.html: Nur falls der Mail-Dialog einen Refresh-Hook oder ein UI-Element für aktualisierte Kandidaten braucht.
- tests/test_dashboard.py: Backend-/HTTP-Tests für frische Kandidatenauslieferung nach Datenänderung ergänzen.
- tests/test_mail_integration.py: Mail-nahe Regressionen für den Vorgangsanlage-Flow absichern.

## Muss umgesetzt werden

- Ursache beheben, warum der Mail-Vorgangsanlage-Flow nicht die aktuelle Transaktionskandidatenliste verwendet.
- Sicherstellen, dass beim Öffnen des Mail-Dialogs oder spätestens vor der Transaktionsauswahl die Kandidaten aus dem aktuellen Datenbankstand geladen werden.
- Vorhandene Kandidatenlogik des Dashboards weiterverwenden statt einen separaten Mail-Sonderweg einzuführen.
- Absichern, dass neu vorhandene Transaktionen in der Mail-Vorgangsanlage auswählbar sind, wenn sie im bestehenden Kandidatenkatalog enthalten sind.

## Soll umgesetzt werden

- Falls der UI-Status veraltet wirkt, einen kleinen, klaren Reload beim Öffnen des Dialogs oder nach erfolgreichem Refresh auslösen.
- Unnötiges Frontend-Caching für Link-Kandidaten vermeiden oder gezielt invalidieren, wenn /api/refresh erfolgreich abgeschlossen wurde.

## Nicht Teil dieses Arbeitspakets

- Mehrere Anhänge einer Mail sichtbar und nutzbar machen.
- Button-Text oder Position beim Vorgangsanlegen aus Mail verbessern.
- Transaktionen splitten oder Teilbeträge mehreren Kategorien oder Rechnungen zuordnen.
- Fehlbuchungs-Spezialflow.
- Mail-Senden mit Zeilenumbrüchen oder Empfängerauswahl.
- Dashboard-Startseite erweitern.

## Akzeptanzkriterien

- Nach einem erfolgreichen Aktualisierungslauf erscheinen neue Transaktionen in der mailbasierten Vorgangsanlage ohne Neustart des Dashboards als verknüpfbare Kandidaten.
- Der Mail-Vorgang-Import kann eine frisch hinzugekommene Transaktions-ID über links.transaction_ids erfolgreich verknüpfen.
- Es gibt keinen separaten, dauerhaft veralteten Kandidatencache nur für den Mail-Flow.
- Vorhandene Vorgangs- und Transaktions-Verknüpfungen funktionieren unverändert weiter.
- Automatisierte Tests decken mindestens ein Regressionsszenario mit nachträglich hinzugekommener Transaktion ab.

## Hinweise für den Umsetzungs-Agenten

- Prüfe in app.js zuerst, ob die Link-Kandidaten für die Mail-Vorgangsanlage nur einmal global geladen und danach wiederverwendet werden; das ist der wahrscheinlichste Fehlerort.
- Wenn die UI bereits /api/vorgaenge/link-candidates nutzt, sollte die Behebung bevorzugt im Frontend-Nachladen oder in der Cache-Invalidierung liegen, nicht in einem neuen API-Endpunkt.
- Falls serverseitig doch zwischengespeichert wird, das nur minimal und gezielt entfernen; DataStore.link_candidate_catalog() liest bereits aus der DB.
- Achte darauf, dass bestehende Importlogik in _mail_vorgang_import() unverändert mit transaction_ids arbeitet; Ziel ist bessere Verfügbarkeit der Auswahl, nicht ein neuer Importpfad.
- Falls Tests bisher nur statische Kandidaten prüfen, baue ein Szenario mit initialem Abruf, nachträglicher DB-Erweiterung und erneutem Abruf ein.

## Manuelle Testhinweise

- Dashboard starten, Mail-Reiter öffnen und eine Mail für die Vorgangsanlage auswählen.
- Ohne Dashboard-Neustart aktuelle Kontobewegungen anfordern oder Testdaten so einspielen, dass eine neue Transaktion in der DB landet.
- Danach den Mail-Dialog zur Vorgangsanlage neu öffnen oder aktualisieren und prüfen, dass die neue Transaktion als Kandidat erscheint.
- Die neue Transaktion auswählen, Vorgang anlegen und kontrollieren, dass die Verknüpfung im erzeugten Vorgang sichtbar ist.

## Offene Fragen

- Ob der Fehler ausschließlich im Frontend-Caching liegt oder ob der Mail-Dialog einen anderen, eingeschränkten Kandidaten-API-Flow verwendet, muss im Code kurz verifiziert werden.
