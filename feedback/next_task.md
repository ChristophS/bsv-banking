# Nächstes Arbeitspaket

## Titel

Direktabschluss für manuell angelegte Vorgänge mit vorbefüllten Verknüpfungen stabilisieren

## Ziel

Beim manuellen Anlegen eines Vorgangs soll ein Nutzer ihn in einem Schritt als abgeschlossen speichern können, wenn die bereits verknüpften Transaktionen vollständig klassifiziert sind und die bestehenden Abschlussbedingungen erfüllt sind. Die UI soll dabei die vorhandenen Verknüpfungen aus dem bestehenden Kandidatenkatalog nutzen und eine klare Option zum direkten Abschluss anbieten.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- tests/test_transactions.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Erstellformular/Modal so erweitern, dass vorhandene Entitäten ausgewählt und completed=true mitgesendet werden kann, inklusive sichtbarer Fehlermeldungen aus dem Backend.
- banking_dashboard/static/index.html: Kleine Ergänzungen für Auswahlfelder/Hinweise im Vorgangs-Erstellformular, falls die vorhandene UI dafür noch keine passenden Container hat.
- banking_dashboard/server.py: POST /api/vorgaenge im Fehlerfall prüfen und nur minimal präzisieren, damit completed=true-Validierungen verständlich an das Frontend zurückgegeben werden.
- tests/test_dashboard.py: API-Tests für POST /api/vorgaenge mit completed=true, verknüpften Transaktionen und Fehlermeldungen bei unvollständiger Klassifikation ergänzen.
- tests/test_transactions.py: Bestehende Tests zum Abschluss- und Klassifikationsfluss um den Fall 'neu angelegter manueller Vorgang' ergänzen, falls dort bereits passende Prüfungen liegen.

## Muss umgesetzt werden

- Sicherstellen, dass ein per POST /api/vorgaenge neu angelegter Vorgang mit completed=true direkt abgeschlossen gespeichert werden kann, wenn die verknüpften Transaktionen vollständig klassifiziert sind und die bestehenden Regeln das zulassen.
- Die bestehende Verknüpfungsauswahl im Erstellflow so anbinden, dass mindestens Transaktionen aus dem vorhandenen Kandidatenkatalog direkt beim Anlegen gewählt werden können.
- Eine klare UI-Option für 'direkt abgeschlossen anlegen' anbieten, die completed=true an die bestehende API sendet.
- Wenn completed=true fachlich nicht zulässig ist, die Backend-Fehlermeldung im Frontend sichtbar und verständlich anzeigen, statt stillschweigend offen anzulegen.
- Keine neue Sonderlogik für manuelle Vorgänge einführen; die bestehende Abschlussvalidierung muss weiterverwendet werden.

## Soll umgesetzt werden

- Vorhandene Vorschläge/Kandidaten für Transaktionen möglichst prominent darstellen, damit der Direktabschluss ohne nachträglichen Bearbeitungsschritt funktioniert.
- Falls das Erstellformular bereits eine Vorgangsart auswählt, kurz erklären, warum ein Direktabschluss blockiert ist, wenn Pflichtklassifikation oder andere bestehende Regeln fehlen.

## Nicht Teil dieses Arbeitspakets

- Inline-Bearbeitung der Transaktionsparameter direkt innerhalb derselben Erstellmaske, falls das einen größeren neuen Bearbeitungs-Flow erfordert.
- Neuer generischer Ein-Klick-Workflow für Transaktion erstellen, klassifizieren und abschließen ohne bestehende Transaktion.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spendenbescheinigungen mit Adressdatenbank und DFBnet-Integration.
- Breite Dashboard-Usability-Überarbeitung außerhalb dieses konkreten Flows.

## Akzeptanzkriterien

- Ein Nutzer kann im Dashboard einen neuen Vorgang manuell anlegen, dabei mindestens eine bereits vorhandene Transaktion direkt verknüpfen und 'abgeschlossen' auswählen.
- Ist die verknüpfte Transaktion vollständig klassifiziert und sprechen keine bestehenden Regeln dagegen, wird der neue Vorgang unmittelbar mit Status abgeschlossen gespeichert.
- Ist completed=true fachlich nicht zulässig, liefert das Backend weiter einen Fehler und die Oberfläche zeigt diesen verständlich an; der Vorgang wird dann nicht stillschweigend in einem anderen Zustand erzeugt.
- Die Umsetzung verwendet die bestehenden Verknüpfungstabellen und vorhandene Abschlussvalidierung; es entsteht kein separater Sonderpfad für manuelle Vorgänge.
- Bestehende API-Endpunkte und das Verhalten vorhandener Vorgänge bleiben außerhalb des Erstellflows unverändert.

## Hinweise für den Umsetzungs-Agenten

- In server.py ist create_vorgang(...) fachlich schon nah am Ziel; der Schwerpunkt dürfte eher im Frontend liegen, damit completed und Link-IDs beim Erstellen tatsächlich erfasst werden.
- Die bestehende _validate_vorgang_completion_values(...) prüft unvollständige Transaktionen und Rechnung+Beleg/Transaktion-Anforderungen bereits vor dem Insert. Diese Logik sollte nicht dupliziert, sondern nur genutzt werden.
- Der vorhandene Endpunkt GET /api/vorgaenge/link-candidates kann als Datenquelle für Auswahlfelder im Erstellformular dienen.
- Falls das aktuelle Frontend schon ein Vorgangserstellformular besitzt, sollte es erweitert statt ersetzt werden. Kein neuer separater Wizard.
- Bei Fehlermeldungen aus POST /api/vorgaenge completed=true die exakte Backend-Meldung anzeigen; dadurch bleibt die bestehende Fachlogik transparent.

## Manuelle Testhinweise

- Im Dashboard eine vollständig klassifizierte bestehende Transaktion auswählen oder kennen, neuen Vorgang anlegen, diese Transaktion verknüpfen, 'abgeschlossen' setzen, speichern, Status in der Vorgangsliste prüfen.
- Dasselbe mit einer unvollständig klassifizierten Transaktion testen: Speichern muss mit verständlicher Fehlermeldung scheitern.
- Falls Vorgangstyp Rechnung gewählt wird, Abschluss ohne Beleg testen: muss blockiert werden; mit Beleg und Transaktion darf Abschluss möglich sein.
- Prüfen, dass ein offen angelegter Vorgang ohne completed weiterhin wie bisher funktioniert.

## Offene Fragen

- Ist im aktuellen Frontend die manuelle Vorgangserstellung schon vorhanden, aber noch ohne Link-Auswahl bzw. Completed-Option, oder muss nur die bestehende Maske erweitert werden?
- Soll in diesem kleinen Paket die Auswahl vorhandener Transaktionen nur per Liste/Suche erfolgen, oder existiert bereits ein Detailkontext, aus dem ein Vorgang mit vorausgewählter Transaktion geöffnet wird?
