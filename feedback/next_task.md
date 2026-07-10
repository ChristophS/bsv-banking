# Nächstes Arbeitspaket

## Titel

Fehlbuchungs-Vorgang mit leerer Sphäre direkt abschließbar machen

## Ziel

Den eng begrenzten Sonderfall ergänzen, dass ein Vorgang mit ausschließlich Fehlbuchungs-Transaktionen trotz leerer Sphäre über den bestehenden Vorgangsfluss abgeschlossen werden kann, ohne neue Kernarchitektur einzuführen.

## Relevante Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: Vorgangsabschlussprüfung so erweitern, dass ausschließlich Fehlbuchungs-Transaktionen als zulässige Ausnahme für die leere Sphäre behandelt werden.
- banking_dashboard/server.py: ggf. kleine Hilfsfunktion ergänzen, die erkennt, ob ein Vorgang nur Fehlbuchungs-Klassifikationen enthält.
- tests/test_dashboard.py: Abschlussverhalten für den Fehlbuchungs-Sonderfall und den weiterhin blockierten Standardfall absichern.

## Muss umgesetzt werden

- Den Abschlussblocker so anpassen, dass ein Vorgang mit verknüpften Fehlbuchungs-Transaktionen und leerer Sphäre abgeschlossen werden kann, wenn er ausschließlich diesen Sonderfall abbildet.
- Die Fachregel explizit eng halten: Vorgangstyp 'Sonstige', Oberkategorie 'Sonstige', Unterkategorie 'Fehlbuchung' und Sphäre leer.
- Einen Test ergänzen, der den zulässigen Fehlbuchungs-Abschluss belegt.
- Einen Gegen-Test ergänzen, der normale unvollständige Vorgänge weiterhin blockiert.

## Soll umgesetzt werden

- Die bestehende Abschlusslogik wiederverwenden statt separate Sonderpfade für neue Statusflüsse einzuführen.
- Die Fehlermeldung bei blockierten Vorgängen so belassen oder minimal anpassen, dass der Sonderfall klar von normalen Fällen getrennt bleibt.

## Nicht Teil dieses Arbeitspakets

- Neue UI-Buttons, Dialoge oder Schnellflüsse im Dashboard.
- Neue Endpunkte für Vorgangserstellung oder neue Verknüpfungsarchitektur.
- Transaktions-Splits, Teilbeträge oder mehrere Kategorien pro Transaktion.
- Mehrere Dokumente einer Mail verschiedenen Transaktionen zuordnen.
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Verein-Integration.

## Akzeptanzkriterien

- Ein Vorgang mit ausschließlich Fehlbuchungs-Transaktionen kann trotz leerer Sphäre abgeschlossen werden.
- Normale Vorgänge mit fehlender Sphäre bleiben weiterhin nicht abschließbar.
- Es gibt mindestens einen Test für den erlaubten Sonderfall und einen Test für den weiterhin verbotenen Standardfall.
- Es werden keine neuen Kern-Tabellen oder grundlegenden Architekturänderungen benötigt.

## Hinweise für den Umsetzungs-Agenten

- Der engste und risikoärmste Eingriff ist voraussichtlich die zentrale Vorgangsabschlussprüfung in server.py, nicht die allgemeine Transaktions-Klassifikationslogik.
- Die generelle Pflichtfeldlogik für andere Vorgangstypen sollte nicht breit aufgeweicht werden.
- Die bestehende Vorgangs- und Transaktionsverknüpfung über transaktion_vorgaenge bleibt die Grundlage des Flows.

## Manuelle Testhinweise

- Im Dashboard einen Vorgang mit Fehlbuchungs-Klassifikation und leerer Sphäre abschließen und prüfen, dass dies gelingt.
- Danach einen normalen unvollständigen Vorgang abschließen versuchen und prüfen, dass er weiterhin blockiert wird.
- Prüfen, dass die Sphäre im Fehlbuchungsfall tatsächlich leer bleibt und nicht durch einen Defaultwert ersetzt wird.

## Offene Fragen

- Keine offenen Fragen für dieses kleine Paket.
