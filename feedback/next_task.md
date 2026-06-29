# Nächstes Arbeitspaket

## Titel

Vorgang beim Erstellen direkt klassifizieren und optional abschließen

## Ziel

Beim Anlegen eines Vorgangs sollen verknüpfte Transaktionen im selben Schritt klassifiziert werden können, sodass ein Vorgang direkt erstellt und bei erfüllten Bedingungen auch abgeschlossen werden kann.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: create_vorgang()-Flow um ein eng begrenztes optionales Payload-Feld für Klassifikationen verknüpfter Transaktionen erweitern und vor der Abschlussprüfung speichern.
- banking_dashboard/server.py: Validierung auf bereits verknüpfte transaction_ids und vorhandene CLASSIFICATION_FIELDS beschränken; bestehende update_transaction_classification()-Regeln wiederverwenden.
- banking_dashboard/static/app.js: Im Vorgang-erstellen/-bearbeiten-Dialog die Klassifikationsfelder für verknüpfte Transaktionen und eine deutlich sichtbare Option für „anlegen und abschließen“ ergänzen.
- banking_dashboard/static/index.html: Nur minimale Markup-Ergänzungen für den Erstellen-/Abschlussbereich, falls für die Bedienbarkeit nötig.
- banking_dashboard/static/styles.css: Nur minimale Styles für den klar sichtbaren Abschlussbereich, falls erforderlich.
- tests/test_dashboard.py: API-Tests für Erstellen mit transaction_classifications und completed=true sowie für Ablehnung unvollständiger oder unzulässiger Klassifikationen ergänzen.

## Muss umgesetzt werden

- Ein optionales Payload-Format für Klassifikationen verknüpfter Transaktionen definieren und serverseitig streng validieren.
- Beim Erstellen eines Vorgangs Klassifikationswerte vor der Abschlussprüfung speichern, damit completed=true in einem einzigen API-Aufruf funktionieren kann.
- Nur bereits im Vorgang verknüpfte Transaktionen klassifizieren lassen; fremde transaction_ids müssen abgelehnt werden.
- Im UI den Abschlusswunsch beim Anlegen eines Vorgangs klar und nicht versteckt darstellen.
- Im UI die vier Pflichtfelder Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre für verknüpfte Transaktionen erfassbar machen; Fachliche Beschreibung optional mitnehmen.
- Fehlermeldungen aus der bestehenden Abschlussprüfung für den Nutzer sichtbar anzeigen.

## Soll umgesetzt werden

- Wenn nur eine Transaktion verknüpft ist, die Klassifikationsfelder direkt im Erstellen-Dialog anzeigen; bei mehreren Transaktionen kompakt pro Transaktion darstellen.
- Bei erfolgreichem „Anlegen und abschließen“ eine kurze Bestätigung anzeigen und zur Vorgangsdetailansicht wechseln.
- Die vorhandene Vorschlags-/Optionslogik für Klassifikationsfelder weiterverwenden, statt neue Listen aufzubauen.

## Nicht Teil dieses Arbeitspakets

- Spam-Score verbessern.
- Vorschläge für weitere Mailverknüpfungen umbauen.
- Manuellen Abschluss-Button im Detailbereich separat umplatzieren, sofern er nicht im Zuge des Erstellen-Dialogs direkt berührt wird.
- Mail aus dem Mailreiter einem Vorgang zuordnen.
- Mehrere Dokumente und mehrere Transaktionen fachlich neu modellieren.
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Automatisierung.
- Grundlegendes Redesign des gesamten Dashboards.

## Akzeptanzkriterien

- Ein Vorgang kann per UI mit mindestens einer Transaktion angelegt werden, während die Transaktion im selben Schritt vollständig klassifiziert wird.
- Wenn „abschließen“ gewählt ist und alle Pflichtfelder gesetzt sind, ist der neue Vorgang nach dem Speichern im Status abgeschlossen.
- Wenn Pflichtfelder fehlen, wird der Vorgang nicht fälschlich abgeschlossen und die vorhandene Abschluss-Fehlermeldung erklärt den Grund.
- Die Transaktionsdetailansicht zeigt nach dem Speichern die gesetzten Klassifikationswerte.
- Bestehende Einzelbearbeitung von Transaktionsklassifikation und Vorgangsstatus funktioniert unverändert.

## Hinweise für den Umsetzungs-Agenten

- In server.py sollte die Validierung der Klassifikationswerte möglichst aus update_transaction_classification() bzw. CLASSIFICATION_FIELDS abgeleitet werden, damit Feldnamen und Längenlimits nicht auseinanderlaufen.
- Die Reihenfolge ist fachlich wichtig: erst Vorgang und Links anlegen bzw. Transaktionen zuordnen, dann Klassifikationen der verknüpften Transaktionen speichern, dann Abschlussprüfung und Status setzen.
- Wenn die Umsetzung innerhalb create_vorgang() erfolgt, darauf achten, dass bei Fehlern keine halb gespeicherten Klassifikationen oder Links zurückbleiben; die bestehende writable-Connection und Transaktion nutzen.
- Das UI sollte nicht versuchen, Abschlussbedingungen clientseitig vollständig nachzubauen; serverseitige Fehler bleiben maßgeblich.
- Für Autocomplete/Dropdowns im UI die vorhandene API /api/classification-options verwenden.

## Manuelle Testhinweise

- Dashboard starten und einen neuen Vorgang mit einer verknüpften Transaktion anlegen.
- Im Erstellen-Dialog alle vier Pflicht-Klassifikationsfelder setzen und „anlegen und abschließen“ wählen.
- Prüfen, dass der Vorgang als abgeschlossen erscheint und die Transaktion die gesetzten Werte trägt.
- Gegenprobe: ein Pflichtfeld leer lassen und prüfen, dass der Abschluss mit verständlicher Meldung blockiert wird.
- Bestehenden Vorgang öffnen und prüfen, dass die Transaktionsklassifikation nach dem Speichern sichtbar ist.

## Offene Fragen

- Soll bei mehreren verknüpften Transaktionen jede Transaktion eigene Klassifikationsfelder erhalten oder wird zunächst nur der häufige Fall einer einzelnen Transaktion optimiert?
- Soll der Vorgangstyp automatisch aus dem Transaktionstyp der ersten vollständig klassifizierten Transaktion vorbelegt werden, oder bleibt das in diesem Paket manuell?
