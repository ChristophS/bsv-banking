# Nächstes Arbeitspaket

## Titel

Lokale Spendenbescheinigung für einen Vorgang erzeugen und als Beleg verknüpfen

## Epic

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 2

## Ziel

Aus einem bestehenden lokalen Spendenempfänger und genau einem bestehenden Vorgang eine nachvollziehbare Spendenbescheinigung als lokale Datei erzeugen, im Belegkatalog erfassen und ausschließlich über vorgang_belege mit dem Vorgang verknüpfen.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Neue oder ergänzende Datenbank-Helper für das Lesen von Vorgangs-, Transaktions-, Empfänger- und Belegdaten sowie das katalogisierte Anlegen eines automatisch erzeugten Belegs in transaction_store/database.py
- Dataclasses oder schlanke Validierungsobjekte für die Eingabe und das Ergebnis der Bescheinigungserzeugung in transaction_store/models.py
- Lokaler Dashboard-API-Endpunkt zur expliziten Erzeugung für genau einen Vorgang in banking_dashboard/server.py
- Schmaler Auslöser in der bestehenden Vorgangsansicht, sofern dort bereits Empfänger- und Belegaktionen integriert sind, in banking_dashboard/static/app.js
- Isolierte Tests mit temporärem Verzeichnis und SQLite-Testdaten in tests/test_transactions.py und tests/test_dashboard.py

## Muss umgesetzt werden

- Für genau einen vorhandenen vorgangs_id und einen vorhandenen recipient_id eine lokale Spendenbescheinigung erzeugen; fehlende oder unbekannte IDs müssen verständlich abgewiesen werden.
- Die Bescheinigung aus bereits lokal gespeicherten Empfänger-, Vorgangs- und zugeordneten Transaktionsdaten aufbauen; Beträge müssen aus amount_minor centgenau berechnet werden.
- Eine eindeutig lesbare, lokale Ausgabe erzeugen, beispielsweise als HTML-Datei, ohne Netzwerkzugriff, DFBnet-Zugriff oder externe Dokumentdienste.
- Die erzeugte Datei als Beleg mit Quelle automatic und geeigneter Dokumentkategorie im bestehenden Belegkatalog erfassen.
- Den erzeugten Beleg ausschließlich über vorgang_belege mit dem ausgewählten Vorgang verknüpfen; keine direkte Transaktion-Beleg-Beziehung einführen.
- Wiederholtes Erzeugen für denselben Vorgang darf vorhandene Belegzuordnungen nicht beschädigen und muss ein nachvollziehbares Ergebnis liefern.
- Unit- und API-Tests für erfolgreichen Ablauf, unbekannten Empfänger, unbekannten Vorgang, centgenaue Betragsermittlung und die Vorgang-Beleg-Verknüpfung ergänzen.

## Soll umgesetzt werden

- Die Ausgabe mit Erstellzeit, stabilen Empfänger- und Vorgangsreferenzen sowie einer Liste der einbezogenen Transaktionen versehen.
- Dateinamen für lokale Dateisysteme sicher und deterministisch aus Vorgangs-ID und Erstellzeit ableiten.
- Im Vorgangsdetail einen klar beschrifteten manuellen Auslöser anbieten, falls die bestehende UI dort bereits Belegaktionen unterstützt.

## Nicht Teil dieses Arbeitspakets

- Abruf oder Pflege von Vereinsdaten über DFBnet.
- Echte Browser-, Banking-, DFBnet-, Mail- oder sonstige externe Aktionen.
- PDF-Erzeugung, digitale Signaturen, Versand per E-Mail oder steuerrechtliche Vollständigkeitsprüfung der Bescheinigungsvorlage.
- Neue direkte Beziehungen zwischen Empfängern, Transaktionen und Belegen außerhalb der bestehenden Vorgangs- und Belegverknüpfungen.
- Massenverarbeitung, Sammelbescheinigungen oder automatische Auswahl mehrerer Vorgänge.

## Akzeptanzkriterien

- Eine gültige Anfrage mit vorhandenem Empfänger und Vorgang erzeugt genau eine lokal lesbare Bescheinigungsdatei und liefert deren Belegdaten zurück.
- Der erzeugte Beleg ist im Katalog vorhanden und über vorgang_belege mit genau dem angefragten Vorgang verknüpft.
- Die Bescheinigung enthält Empfängerangaben, Vorgangsreferenz und den aus den zugeordneten Transaktionen centgenau bestimmten Betrag.
- Eine unbekannte Empfänger- oder Vorgangs-ID erzeugt keine Datei und keine Datenbankänderung.
- Die Implementierung verwendet keine direkte Transaktion-Beleg-Verknüpfung und führt keine externe Kommunikation aus.
- Die ergänzten Tests laufen ohne produktive Daten, Secrets, Browser oder Netzverbindung erfolgreich.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandenen Tabellen vorgaenge, transaktion_vorgaenge, transactions, belege und vorgang_belege sind verbindlich zu verwenden.
- Die bestehende donation_recipients-Persistenz ist als Quelle für Empfängeradressen zu verwenden; keine zweite Empfängertabelle einführen.
- Dateiablage soll innerhalb des bereits geschützten lokalen Belegverzeichnisses oder eines klar abgegrenzten Unterordners erfolgen.
- Die Erzeugung muss transaktional geplant werden: Bei Validierungs-, Schreib- oder Katalogfehlern dürfen keine unvollständigen Datenbankverknüpfungen verbleiben.
- Eine fachlich belastbare steuerliche Vorlage ist nicht zu behaupten; der lokale Dokumentinhalt soll als nachvollziehbarer erster Entwurf gekennzeichnet sein, falls keine vollständigen Vereinsdaten lokal verfügbar sind.

## Manuelle Testhinweise

- Mit einer temporären lokalen Testdatenbank einen Empfänger, einen Vorgang und mindestens eine zugeordnete Transaktion anlegen.
- Die Bescheinigung über den vorgesehenen lokalen API- oder UI-Auslöser erzeugen und Dateiinhalt, Betrag sowie Vorgangsreferenz prüfen.
- Im Vorgangsdetail kontrollieren, dass der erzeugte Beleg sichtbar beziehungsweise über die vorhandene Belegverknüpfung abrufbar ist.
- Ungültige Empfänger- und Vorgangs-IDs testen und prüfen, dass weder Datei noch Belegverknüpfung entstehen.

## Offene Fragen

- Welche lokal verfügbaren Vereinsangaben und welcher verbindliche Bescheinigungstext sollen in einer späteren rechtssicheren Vorlage verwendet werden?
- Soll eine wiederholte Erzeugung bewusst stets eine neue versionierte Bescheinigung erzeugen oder eine bestehende automatisch erzeugte Bescheinigung für denselben Vorgang ersetzen?
