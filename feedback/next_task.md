# Nächstes Arbeitspaket

## Titel

Klassifikationsstatus für einzelne Split-Zeilen ableiten und anzeigen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.1

## Ziel

Für jede gespeicherte Split-Zeile einen nachvollziehbaren Klassifikationsstatus nach derselben fachlichen Semantik wie bei Transaktionen bereitstellen und im bestehenden Split-Editor sichtbar machen.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/classification.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Split-Lese-/Schreibfunktionen und API-Serialisierung in transaction_store/database.py und banking_dashboard/server.py
- Gemeinsame oder gezielt wiederverwendete Statusableitung in transaction_store/classification.py
- Darstellung des Status je Split-Zeile im vorhandenen Split-Editor in banking_dashboard/static/app.js
- Unit- und API-Tests für vollständige, unvollständige und leere Split-Klassifikationen

## Muss umgesetzt werden

- Für Split-Zeilen einen abgeleiteten, nicht manuell speicherbaren Klassifikationsstatus bereitstellen.
- Die Statussemantik fest an die bestehende Transaktionslogik anlehnen: alle fünf Split-Klassifikationsfelder leer ergibt unklassifiziert; alle vier Pflichtfelder Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre befüllt ergibt vollständig klassifiziert; jeder andere Zustand ergibt unvollständig klassifiziert.
- Den abgeleiteten Status in den bestehenden Split-Leseantworten verfügbar machen, ohne die gespeicherten Split-Felder oder bestehende Transaktionsantworten inkompatibel zu verändern.
- Den Status je Split-Zeile im vorhandenen Editor lesbar anzeigen und nach erfolgreichem Speichern mit den aktualisierten Split-Daten auffrischen.
- Automatisierte Tests für die drei Statuszustände sowie für die API-/Serialisierungsdarstellung ergänzen.

## Soll umgesetzt werden

- Eine vorhandene Statusableitungsfunktion wiederverwenden oder eine kleine gemeinsame Hilfsfunktion schaffen, statt die Semantik in Datenbank, Server und UI mehrfach zu duplizieren.
- Die Statusanzeige so gestalten, dass sie nicht mit dem Status des übergeordneten Vorgangs verwechselt werden kann.

## Nicht Teil dieses Arbeitspakets

- Automatische Klassifikation von Split-Zeilen durch Klassifikationsregeln.
- Vorschlagslisten oder abhängige Datalists für Klassifikationsfelder von Split-Zeilen.
- Änderungen der Statusableitung des übergeordneten Vorgangs aufgrund von Split-Zeilen.
- Neue Rechnungs-, Beleg- oder Transaktionsdirektbeziehungen.
- Zuordnung einer Transaktion zu mehreren Rechnungen oder Teilrechnungen.

## Akzeptanzkriterien

- Eine Split-Zeile ohne befüllte Klassifikationsfelder wird als unklassifiziert geliefert und angezeigt.
- Eine Split-Zeile mit allen vier Pflichtfeldern wird als vollständig klassifiziert geliefert und angezeigt; die optionale fachliche Beschreibung ist hierfür nicht erforderlich.
- Eine Split-Zeile mit nur einem Teil der Klassifikationsfelder oder ausschließlich einer fachlichen Beschreibung wird als unvollständig klassifiziert geliefert und angezeigt.
- Nach dem Speichern geänderter Split-Klassifikationsfelder zeigt der Editor den neu abgeleiteten Status ohne Browser-Neustart.
- Die Split-Summengleichheit zum Transaktionsbetrag und die bestehende Split-Persistenz bleiben unverändert geschützt.
- Die vorhandenen Tests sowie die neuen Split-Status-Tests laufen ohne Browser-, Banking- oder sonstige externe Zugriffe erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Die Klassifikation bleibt an der Split-Zeile; sie darf nicht vorschnell auf die übergeordnete Transaktion gespiegelt werden.
- Vorgänge bleiben das zentrale Objekt. Dieses Paket erstellt weder direkte Beziehungen zwischen Splits und Belegen noch umgeht es die vorhandenen Vorgangsverknüpfungen.
- Der Status soll aus den bereits vorhandenen Split-Feldern berechnet werden; eine zusätzliche persistierte Statusspalte ist für diesen Schritt nicht erforderlich.
- Bestehende API-Felder und gespeicherte Split-IDs müssen kompatibel bleiben.

## Manuelle Testhinweise

- Im lokalen Dashboard eine Transaktion mit gültiger Split-Summe öffnen und eine neue Split-Zeile ohne Klassifikation speichern.
- Nacheinander nur ein Pflichtfeld, dann alle vier Pflichtfelder und anschließend nur die fachliche Beschreibung setzen und jeweils die angezeigte Statusänderung prüfen.
- Die Seite neu laden und prüfen, dass die gespeicherten Felder und der daraus erneut abgeleitete Status konsistent bleiben.
- Sicherstellen, dass weder der Betrag noch bestehende Vorgangszuordnungen durch die Statusanzeige verändert werden.

## Offene Fragen

- Soll die Statusanzeige ausschließlich als Text erscheinen oder zusätzlich die bereits für Transaktionsstatus verwendete visuelle Kennzeichnung übernehmen?
