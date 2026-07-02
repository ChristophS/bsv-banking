# Nächstes Arbeitspaket

## Titel

Mail-Import mit optionalem Sofort-Abschluss robust machen

## Ziel

Den bestehenden Mail-zu-Vorgang-Import so absichern, dass ein neu angelegter Vorgang bei completed=true nur dann direkt abgeschlossen wird, wenn die vorhandenen Abschlussregeln es erlauben, und dass Fehler dabei sauber sichtbar bleiben.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: _mail_vorgang_import verarbeitet requested_completed und ist der zentrale Backend-Einstieg für die optionale Abschlusslogik.
- banking_dashboard/static/app.js: Der bestehende Mail-Import-Request muss das completed-Flag korrekt weiterreichen bzw. auslösen.
- banking_dashboard/static/index.html: Nur falls der bestehende Mail-Import-Dialog noch keinen klaren Sofort-Abschluss-Schalter hat.
- tests/test_dashboard.py: API- und Dashboard-Tests für POST /api/mail/<id>/vorgang-import mit completed=true.

## Muss umgesetzt werden

- Sicherstellen, dass der bestehende Mail-Import bei completed=true den neu angelegten Vorgang nach erfolgreicher Prüfung als abgeschlossen zurückliefert.
- Wenn der Abschluss wegen vorhandener Regeln/Validierungen scheitert, muss die API einen nachvollziehbaren Fehler liefern und den Vorgang nicht stillschweigend als abgeschlossen darstellen.
- Die bestehende Abschlusslogik verwenden; keine neue fachliche Abschlussregel erfinden.
- Automatisierte Tests für mindestens einen Erfolgsfall und einen Blockerfall ergänzen.

## Soll umgesetzt werden

- Falls im UI noch kein verständlicher Sofort-Abschluss-Schalter existiert, den bestehenden Mail-Import-Dialog minimal ergänzen.
- Nach erfolgreichem Import in der UI sichtbar machen, ob der Vorgang direkt abgeschlossen wurde.

## Nicht Teil dieses Arbeitspakets

- Generischer Ein-Klick-Workflow für manuelle Vorgangserstellung außerhalb des Mail-Imports.
- Transaktionsklassifikation direkt im selben Formular bearbeiten.
- Mehrere Dokumente derselben Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Neue Abschlusslogik oder neue fachliche Pflichtregeln einführen.
- Adressdatenbank, Spendenbescheinigungen oder DFBnet-Verein-Integration.
- Breite Dashboard-Usability-Überarbeitung.

## Akzeptanzkriterien

- Ein Mail-Import kann weiterhin einen neuen Vorgang mit verknüpfter Mail und optionalen Dokumenten, To-Dos und Terminen anlegen.
- Wird completed=true gesendet und sind die bestehenden Voraussetzungen erfüllt, ist der zurückgegebene Vorgang status='abgeschlossen'.
- Wird completed=true gesendet und sind die Voraussetzungen nicht erfüllt, liefert die API einen nachvollziehbaren Fehler aus der bestehenden Abschlussprüfung.
- Bestehende Verknüpfungen über vorgaenge bleiben unverändert; es werden keine neuen Direktverknüpfungstabellen eingeführt.
- Die Tests decken mindestens einen Erfolgs- und einen Fehlerfall des Sofort-Abschlusses beim Mail-Import ab.

## Hinweise für den Umsetzungs-Agenten

- server.py ist voraussichtlich der Hauptort, weil dort der Mail-Import bereits den optionalen Abschluss anstößt.
- Die bestehende Vorgangs-, Dokument-, To-Do- und Termin-Verknüpfung über Vorgänge soll unverändert bleiben.
- transaction_store/database.py und transaction_store/classification.py dienen hier nur als Referenz für vorhandene Abschluss- und Validierungslogik; Änderungen dort nur bei echtem Bedarf.
- Keine neue Workflow-Architektur bauen, sondern den vorhandenen Pfad minimal und konsistent nutzen.

## Manuelle Testhinweise

- Dashboard starten und im Mail-Reiter eine analysierbare Mail importieren, dabei Sofort-Abschluss aktivieren.
- Fall 1: Voraussetzungen erfüllt, der Vorgang sollte direkt als abgeschlossen erscheinen.
- Fall 2: completed=true in einem Szenario mit bestehendem Abschlussblocker testen; die UI soll einen verständlichen Fehler zeigen und keinen fälschlich abgeschlossenen Vorgang melden.
- Prüfen, dass Mail-, Dokument-, To-Do- und Termin-Verknüpfungen am Vorgang weiterhin vorhanden sind.

## Offene Fragen

- Gibt es im aktuellen Frontend bereits einen sichtbaren Schalter für completed beim Mail-Import, oder wird das Flag nur intern gesetzt?
- Soll bei einem Abschlussfehler der Vorgang trotzdem angelegt bleiben und die API den Teil-Erfolg signalisieren, oder ist das bestehende Verhalten gewünscht?
