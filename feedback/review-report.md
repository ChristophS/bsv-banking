# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Muss-Anforderungen sind im GitHub-Diff umgesetzt: lokale HTML-Bescheinigung, centgenaue Summe aus amount_minor, Empfänger- und Vorgangsvalidierung, automatische Belegkatalogisierung sowie ausschließliche Verknüpfung über vorgang_belege. Erfolgs-, Fehler-, API-, Atomicitäts- und UI-nahe Tests wurden ergänzt. Der GitHub-Branch ist gegenüber main um vier Commits voraus und enthält keine fehlenden Compare-Dateien.

# Technischer Review

## Entscheidung

**Akzeptiert.**

## Geprüfte Anforderungen

- Für einen vorhandenen Vorgang und einen vorhandenen Spendenempfänger wird eine lokale Bescheinigung erzeugt.
- Unbekannte Vorgangs- und Empfänger-IDs werden vor Datei- und Datenbankschreibzugriffen abgewiesen.
- Empfänger-, Vorgangs- und zugeordnete Transaktionsdaten werden aus den bestehenden Tabellen gelesen.
- Der Betrag wird als Summe der ganzzahligen `amount_minor`-Werte berechnet und ohne Gleitkommaarithmetik als Centbetrag formatiert.
- Die Ausgabe ist eine lokal gespeicherte UTF-8-HTML-Datei und als steuerrechtlich ungeprüfter Entwurf gekennzeichnet.
- Erstellzeit, Empfänger-ID, Vorgangsreferenz und die einbezogenen Transaktionen werden ausgegeben.
- Die Datei wird im bestehenden geschützten Belegverzeichnis unter einer geeigneten Kategorie abgelegt.
- Der Beleg wird mit Quelle `automatic` und Kategorie `spendenbescheinigungen` im bestehenden Katalog gespeichert.
- Die Verknüpfung erfolgt ausschließlich über `vorgang_belege`; eine direkte Transaktion-Beleg-Beziehung wurde nicht eingeführt.
- Wiederholte Erzeugungen beschädigen bestehende Verknüpfungen nicht und erzeugen versionierte Dateien.
- Der API-Endpunkt akzeptiert exakt ein nichtleeres String-Feld `recipient_id`.
- Der manuelle Auslöser ist im Vorgangsdetail vorhanden.

## Transaktionalität und Fehlerbehandlung

Die Validierung der Quelldaten erfolgt vor dem Dokumentaufbau. `create_document_from_bytes` verwendet weiterhin den bestehenden Katalogpfad. Bei einem Fehler während Datei-, Katalog- oder Verknüpfungsschreibzugriff wird die Datenbanktransaktion zurückgerollt und eine in diesem Aufruf geschriebene Datei bereinigt. Die ergänzten Tests prüfen insbesondere, dass nach einem erzwungenen Katalogfehler weder Beleg noch Vorgang-Beleg-Link noch HTML-Datei verbleiben.

## Tests

Die Änderungen ergänzen Unit- und API-Tests für:

- erfolgreichen API-Ablauf,
- centgenaue Betragsermittlung,
- Inhalt der HTML-Datei,
- Katalogdaten und Quelle,
- Verknüpfung mit genau dem angefragten Vorgang,
- unbekannten Empfänger,
- unbekannten Vorgang,
- ungültige `recipient_id`-Typen und Leerwerte,
- Fehlerbereinigung nach Katalogfehlern.

Die gemeldete relevante Testsuite umfasst 155 bestandene Tests und sechs übersprungene Tests. Die Tests verwenden temporäre SQLite-Datenbanken und synthetische Daten ohne externe Kommunikation.

## Scope und Architektur

Die vorhandenen Tabellen, Services und der bestehende Belegkatalog werden verwendet. Es wurde keine zweite Empfängertabelle und keine unerlaubte direkte Transaktion-Beleg-Verknüpfung eingeführt. PDF, Signatur, Versand, DFBnet und externe Dokumentdienste bleiben außerhalb des Scopes.

## Compare- und Runner-Prüfung

Der GitHub-Compare ist nutzbar: Der Agent-Branch ist gegenüber `main` vier Commits voraus und nicht hinterher. `missing_from_github_compare` ist leer. Die Runner-Metadaten sind allerdings nicht vollständig synchron: Dort wurde lediglich der Implementation Report als validierter beziehungsweise gestagter Pfad angegeben, obwohl der GitHub-Compare die eigentlichen Quell- und Teständerungen enthält. Das ist ein Prozesshinweis, aber kein fachlicher Blocker für den geprüften GitHub-Commit.
