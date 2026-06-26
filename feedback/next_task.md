# Nächstes Arbeitspaket

## Titel

Manuelle Gegenposition als Overlay mit Vorschlagsfeldern

## Ziel

Die manuelle Erfassung einer Gegenposition wird als Overlay/Popup geöffnet und bietet für die Pflichtfelder Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre bestehende Werte als Auswahl mit manueller Eingabe an. Damit wird die Eingabe schneller und konsistenter, ohne die bestehende Vorgangs- und Transaktionslogik umzubauen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py
- tests/test_transactions.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js für Öffnen/Schließen des Overlays, Feldbindung, Validierung und Befüllen der Vorschlagslisten aus vorhandenen Transaktionswerten.
- banking_dashboard/static/index.html für die Dialogstruktur des Overlays.
- banking_dashboard/static/styles.css für das Popup-/Overlay-Layout und die Lesbarkeit der Eingabefelder.
- banking_dashboard/server.py nur falls die bestehende Erfassungsroute serverseitig Pflichtfelder validiert oder angepasst werden muss.
- tests/test_dashboard.py für Overlay-Verhalten und UI-nahe Validierungsfälle.
- tests/test_transactions.py für Pflichtfelder und die Weiterverwendung der bestehenden Verknüpfungslogik.

## Muss umgesetzt werden

- Die manuelle Gegenpositions-Eingabe in ein Overlay/Popup verlagern, das aus der bestehenden Detailansicht geöffnet wird.
- Für Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre vorhandene Werte als auswählbare Vorschläge anbieten.
- Manuelle Freitexteingabe für diese vier Felder weiterhin erlauben.
- Die vier Felder als Pflichtfelder behandeln und das Speichern ohne vollständige Angaben verhindern.
- Die bestehende Vorgangs-/Transaktionsverknüpfung beibehalten und keine neue Datenstruktur einführen.

## Soll umgesetzt werden

- Die vorhandene Vorschlagsmechanik für Klassifikationsfelder wiederverwenden, falls sie im Dashboard bereits existiert.
- Das Overlay optisch konsistent zum restlichen Dashboard gestalten.

## Nicht Teil dieses Arbeitspakets

- Automatische Zuordnung der 100%-Übereinstimmung zwischen Deckelliste und Spielerprämien.
- DFBnet-Pagination oder Retry-Logik für fehlende Spieltage.
- Auswahl eines Dateipfads für Deckellisten.
- Umbuchungs-Sonderbehandlung.
- Mail-Dokumente direkt speichern ohne Vorgangserstellung.
- Spam-Erkennung verbessern.
- Gelesen-Status über den gesamten Mailverlauf propagieren.
- Filter für Transaktionen abgeschlossener Vorgänge.

## Akzeptanzkriterien

- Die manuelle Gegenposition öffnet sich als Overlay/Popup und ist ohne langes Scrollen erreichbar.
- Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre können über Vorschläge gewählt oder manuell eingetragen werden.
- Das Speichern ist nur möglich, wenn alle vier Pflichtfelder befüllt sind.
- Die Gegenposition wird weiterhin über die vorhandene Vorgangs-/Transaktionslogik gespeichert und angezeigt.
- Bestehende Tests laufen weiter; neue Tests decken Overlay-Öffnen und Pflichtfeldvalidierung ab.

## Hinweise für den Umsetzungs-Agenten

- Der Hauptort für die UI-Anpassung dürfte `banking_dashboard/static/app.js` sein, weil dort bestehende Detailansichten und Eingabeaktionen zusammenlaufen.
- `banking_dashboard/static/index.html` und `banking_dashboard/static/styles.css` sollten nur um die notwendige Dialogstruktur und das Styling ergänzt werden.
- Für Vorschlagswerte sollten vorhandene Transaktionsdaten genutzt werden, statt eine neue Quelle oder Struktur einzuführen.
- Falls serverseitige Validierung bereits existiert, diese direkt in den bestehenden Pfad integrieren.

## Manuelle Testhinweise

- Eine Transaktion im Dashboard öffnen und die manuelle Gegenposition über das neue Overlay starten.
- Prüfen, dass das Overlay erscheint und nicht in einer langen Seite untergeht.
- Prüfen, dass die vier Pflichtfelder nicht leer gespeichert werden können.
- Prüfen, dass vorhandene Werte als Vorschläge erscheinen und manuell ergänzt werden können.
- Prüfen, dass die Gegenposition korrekt im bestehenden Vorgang landet.

## Offene Fragen

- Gibt es im aktuellen UI bereits eine wiederverwendbare Komponente für Vorschlagsfelder mit Freitext?
- Ist für die manuelle Gegenposition bereits ein bestehender API-Pfad vorgesehen, der direkt weitergenutzt werden soll?
