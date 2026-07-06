# Nächstes Arbeitspaket

## Titel

Originaldokument im Vorgangs-/Dokument-Flow zusätzlich zum Katalogeintrag öffnen

## Ziel

Im bestehenden Vorgangs- und Dokument-Flow soll neben dem bisherigen Öffnen des Katalogeintrags auch das eigentliche Originaldokument der verknüpften Datei direkt geöffnet werden können, damit Nutzer beim Verknüpfen aus einer Transaktion heraus nicht nur Metadaten sehen.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: neuen read-only Endpunkt ergänzen, der das Originaldokument eines katalogisierten `beleg_id` aus `dateipfad` ausliefert, inklusive 404 bei fehlender Datei oder ungültiger ID.
- banking_dashboard/static/app.js: an den Beleg-Aktionen in Vorgangsdetails bzw. Dokumentlisten eine zusätzliche Aktion für das Originaldokument ergänzen.
- banking_dashboard/static/index.html: falls feste Button-/Action-Container existieren, Beschriftung oder Platz für die zweite Aktion ergänzen.
- tests/test_dashboard.py: Server-Tests für den neuen Dokument-Endpunkt und Fehlerfälle ergänzen.

## Muss umgesetzt werden

- Einen serverseitigen GET-Endpunkt für `beleg_id` ergänzen, der die zugehörige Originaldatei aus `dateipfad` ausliefert.
- Den Endpunkt ausschließlich auf bereits katalogisierte Belege beschränken; keine freien Pfadparameter oder beliebige Dateisystemzugriffe zulassen.
- Bei fehlendem Beleg-Datensatz oder nicht vorhandener Datei einen klaren 404-Fehler zurückgeben.
- In der UI neben der bisherigen Öffnen-/Detail-Aktion eine separate Aktion für das Originaldokument anbieten.
- Die bestehende Beleg-Verknüpfungslogik über Vorgänge unverändert lassen.

## Soll umgesetzt werden

- Wenn möglich die UI konsistent zwischen 'Katalogeintrag öffnen' und 'Originaldokument öffnen' unterscheiden.
- Für browser-taugliche Dateitypen nach Möglichkeit inline ausliefern, für andere Typen Download erlauben, analog zum vorhandenen Attachment-Verhalten.

## Nicht Teil dieses Arbeitspakets

- Neue Dokumentenarchitektur oder neue Speicherlogik.
- Mehrere Mail-Anhänge gleichzeitig besser sichtbar machen.
- Mehrere Dokumente unterschiedlichen Transaktionen zuordnen.
- OCR-/Extraktionslogik oder komplette Dokumentenvorschau neu gestalten.
- Transaktionen bestehenden Vorgängen zuordnen oder Vorgangsvorschläge erweitern.

## Akzeptanzkriterien

- Für einen vorhandenen Beleg mit vorhandener Datei liefert der neue Endpunkt die Originaldatei mit passendem Content-Type und erfolgreichem HTTP-Status aus.
- Für einen vorhandenen Beleg mit fehlender Datei erhält der Client einen 404-Fehler mit verständlicher Fehlermeldung.
- In der UI ist zwischen Katalogeintrag/Metadaten und Originaldokument erkennbar zu unterscheiden.
- Aus dem betroffenen Flow heraus kann der Nutzer das Originaldokument direkt öffnen.
- Die bestehende Beleg-Verknüpfungslogik bleibt funktionsfähig.

## Hinweise für den Umsetzungs-Agenten

- Serverseitig ist ein Response-Muster analog zu `_attachment_response()` naheliegend; die Datenquelle kommt aus `belege.dateipfad` statt aus Mail-BLOBs.
- Nutze `beleg_detail()` oder einen kleinen internen Lookup auf `belege`, um Dateiname, Typ und `vorhanden` vor dem Ausliefern zu prüfen.
- Achte darauf, dass `dateipfad` zwar absolut gespeichert ist, aber nur katalogisierte Pfade verwendet werden.
- Wenn die bestehende UI schon Links zu `/api/belege/<id>` für JSON-Details nutzt, diesen Endpunkt nicht umdefinieren, sondern einen separaten Dateiendpunkt anlegen.

## Manuelle Testhinweise

- Dashboard starten, einen Vorgang mit verknüpftem Beleg öffnen und prüfen, dass Metadaten/Katalogansicht und Originaldokument separat erreichbar sind.
- Den Flow testen, bei dem aus einer Transaktion heraus ein Vorgang erstellt und ein Dokument verknüpft wird; anschließend direkt das Originaldokument öffnen.
- Mindestens eine PDF-Datei und ein Bild-/Textdokument testen, um Inline-Anzeige bzw. Download zu prüfen.
- Einen absichtlich nicht mehr vorhandenen Belegpfad testen und prüfen, dass die UI keinen Absturz zeigt, sondern einen verständlichen Fehler meldet.

## Offene Fragen

- Soll der bisherige Button unverändert den Katalogeintrag öffnen und nur ein zweiter Button ergänzt werden?
- An welcher konkreten UI-Stelle wird die aktuelle Beleg-Aktion gerendert, falls sie in mehreren Flows vorkommt?
