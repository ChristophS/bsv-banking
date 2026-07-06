# Nächstes Arbeitspaket

## Titel

ISO-Zeitlogik für Termine bei beginnt_am absichern

## Ziel

Sicherstellen, dass Termine mit ISO-Zeitpunkten in Listen, Übersichten und Filtern fachlich korrekt nach Kalendertag behandelt werden und dabei vorhandene Termin- und Vorgangslogik unverändert weiter genutzt wird.

## Relevante Dateien

- banking_dashboard/server.py
- transaction_store/database.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: Stellen prüfen, an denen beginnt_am direkt als String verglichen, sortiert oder in Tageslogik eingeordnet wird; insbesondere overview_counts(), list_termine(), _termin_result(), _parse_datetime_like() und ggf. Hilfsfunktionen zur Datumsnormalisierung.
- transaction_store/database.py: prüfen, ob dort Termin-Schema, Migrationen oder terminbezogene Abfragen/Views existieren, die ebenfalls von ISO-Zeitpunkten vs. ISO-Datum betroffen sind.
- tests/test_dashboard.py: gezielte Regressionstests für Termine mit starts_at als reines Datum und als ISO-Zeitpunkt ergänzen.

## Muss umgesetzt werden

- Konkret prüfen, ob ISO-Zeitpunkte in beginnt_am derzeit an irgendeiner Stelle fachlich falsch als ganzer Timestamp statt als Kalendertag behandelt werden.
- Falls ein Fehler vorliegt, die Logik so vereinheitlichen, dass Tagesvergleiche für anstehende Termine robust sowohl mit ISO-Datum als auch mit ISO-Zeitpunkt funktionieren.
- Regressionstests ergänzen, die den identifizierten Fall reproduzieren und absichern.
- Darauf achten, dass Sortierung und API-Ausgabe bestehender Termine weiterhin stabil bleiben.

## Soll umgesetzt werden

- Wenn sinnvoll, eine kleine interne Hilfsfunktion zur Extraktion des Vergleichstags aus ISO-Datum/ISO-Zeitpunkt verwenden, statt die Logik mehrfach inline zu verteilen.
- Auch Fälle mit Zeitzonen-Suffix nur dann anfassen, wenn sie mit der bestehenden Speicherung realistisch auftreten und ohne Architekturumbau robust testbar sind.

## Nicht Teil dieses Arbeitspakets

- Größere Überarbeitung des Terminmoduls.
- UI-Komfortfunktionen für Termine.
- Automatische Terminextraktion aus Mails erweitern.
- Andere Backlog-Themen wie Mehrfachzuordnung von Mail-Dokumenten oder Spendenbescheinigungen.

## Akzeptanzkriterien

- Ein Termin mit starts_at als ISO-Datum wird in anstehenden Terminabfragen korrekt berücksichtigt.
- Ein Termin mit starts_at als ISO-Zeitpunkt am heutigen oder zukünftigen Kalendertag wird in anstehenden Terminabfragen fachlich gleichwertig korrekt berücksichtigt.
- Die Counts upcoming_termine und unassigned_termine in /api/overview verhalten sich für ISO-Datum und ISO-Zeitpunkt konsistent.
- Die Terminliste unter /api/termine mit unassigned_upcoming bzw. hide_completed liefert keine Regression für bestehende Daten.
- Automatisierte Tests decken mindestens einen Termin mit Datum und einen mit Zeitstempel ab.

## Hinweise für den Umsetzungs-Agenten

- Der naheliegendste Risikobereich ist String-basierte Datumslogik. In server.py wird bereits SUBSTR(beginnt_am, 1, 10) verwendet; prüfe, ob alle relevanten Stellen konsequent dieselbe Tagesableitung nutzen.
- _parse_datetime_like erlaubt sowohl ISO-Datum als auch ISO-Zeitpunkt und speichert aktuell den Originalstring zurück. Dadurch kann fachlich korrekte Tageslogik nur funktionieren, wenn Vergleiche sauber normalisiert werden.
- Falls database.py terminbezogene Views, Seed-/Migrationslogik oder Konstanten enthält, dort nur minimal eingreifen.
- Testdaten sollten bewusst beide Varianten abdecken: starts_at='YYYY-MM-DD' und starts_at='YYYY-MM-DDTHH:MM:SS'.

## Manuelle Testhinweise

- Im Dashboard einen Termin mit reinem Datum und einen mit Uhrzeit am selben zukünftigen Tag anlegen.
- Prüfen, ob beide in /api/termine und in der Übersichts-Kachel für anstehende Termine erscheinen.
- Einen unzugeordneten Termin mit Uhrzeit anlegen und prüfen, ob unassigned_termine korrekt hochzählt.
- Optional einen vergangenen Termin mit Uhrzeit anlegen, um sicherzustellen, dass er nicht fälschlich als anstehend zählt.

## Offene Fragen

- Ist der Backlog-Punkt rein präventiv gemeint oder gibt es bereits einen beobachteten Fehlfall mit konkretem Beispielwert für beginnt_am?
- Soll bei ISO-Zeitpunkten mit Offset ausschließlich das Datumspräfix im gespeicherten String zählen, oder gibt es fachlich gewünschte Lokalisierungslogik?
