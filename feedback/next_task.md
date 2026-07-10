# Nächstes Arbeitspaket

## Titel

Mehrere Mail-Anhänge im Vorgangsimport sichtbar und importierbar machen

## Ziel

Beim mailbasierten Vorgangsanlegen sollen alle Anhänge einer Mail in der Oberfläche sichtbar sein und mehrere aktivierte Anhänge gemeinsam als Belege in den Vorgang importiert werden können.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- tests/test_mail_integration.py
- banking_dashboard/mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Rendering der Anhangsliste, Auswahl-/Preview-Logik und Erzeugung des documents-Arrays für den Import.
- banking_dashboard/static/index.html: Container oder wiederholbare UI-Elemente für mehrere Anhänge, falls aktuell nur ein Einzelanhang vorgesehen ist.
- banking_dashboard/server.py: nur falls die Importantwort oder Attachment-Metadaten für die UI noch konsistent ergänzt werden müssen.
- tests/test_dashboard.py: Mehrfachanhang-Import und Payload mit mehreren documents absichern.
- tests/test_mail_integration.py: Mail-/Attachment-Flow für mehrere Anhänge ergänzen, falls dort noch nicht abgedeckt.

## Muss umgesetzt werden

- Alle Anhänge einer Mail in der Vorgangsanlage anzeigen, nicht nur den ersten.
- Pro Anhang attachment_index, Dateiname, Kategorie, Beschreibung und aktiv/deaktiviert-Status im bestehenden Flow darstellen oder verarbeiten.
- Sicherstellen, dass mehrere aktivierte Anhänge als mehrere Einträge im documents-Array an POST /api/mail/<id>/vorgang-import gesendet werden.
- Die Reihenfolge der UI-Anhänge an attachmentIndex bzw. der gelieferten Mailstruktur ausrichten.
- Tests ergänzen, die einen Import mit mehreren ausgewählten Anhängen abdecken.

## Soll umgesetzt werden

- Leere Zustände sauber anzeigen, wenn keine Anhänge vorhanden sind.
- Eine einfache auswählbare Liste oder Einzelvorschau pro Anhang nutzen, falls kein Mehrfach-Preview-Layout existiert.
- Bei fehlenden Metadaten für einzelne Anhänge trotzdem einen sichtbaren Default-Eintrag anzeigen statt den Anhang zu verstecken.

## Nicht Teil dieses Arbeitspakets

- Mehrere Dokumente innerhalb desselben Vorgangs unterschiedlichen Transaktionen zuordnen.
- Aktuellste Transaktionen im Mail-Vorgangsanlegen nachladen oder Refresh-Logik ändern.
- Button-Text oder Position beim Vorgangsanlegen ändern.
- Mail-Senden mit Empfängerauswahl oder Zeilenumbrüchen.
- Transaktions-Splitting oder Fehlbuchungs-Sonderfälle.

## Akzeptanzkriterien

- Wenn eine Mail mehrere Anhänge hat, zeigt die Vorgangsanlage alle Anhänge in der Oberfläche an.
- Mehrere Anhänge können gleichzeitig aktiviert bleiben und werden nach dem Import als mehrere Belege am erzeugten Vorgang verknüpft.
- Der Import verwendet weiterhin attachment_index pro Dokument und funktioniert mit mehr als einem Dokumenteintrag.
- Bei nur einem Anhang bleibt das bisherige Verhalten erhalten.
- Bei Mails ohne Anhänge bleibt der Import ohne Dokumente möglich und die UI zeigt keinen irreführenden Einzelanhang an.
- Automatisierte Tests decken den Mehrfachanhang-Fall ab.

## Hinweise für den Umsetzungs-Agenten

- Der Server-Import verarbeitet bereits ein documents-Array und iteriert über mehrere Einträge; das Problem liegt sehr wahrscheinlich primär in der Frontend-Darstellung bzw. Payload-Erzeugung.
- Die Fallback-/Analyse-Logik erzeugt bereits Dokumente für mehrere Attachments; die UI sollte daher nicht auf documents[0] begrenzt sein.
- Falls Vorschauen über /api/mail/<id>/attachments/<index> geladen werden, darauf achten, dass der Index im Frontend korrekt zur Serverlogik passt.
- Die vorhandene Belegablage über create_document_from_bytes und vorgang_belege weiterverwenden, keine neue Dokumentarchitektur einführen.

## Manuelle Testhinweise

- Mail mit mindestens drei Anhängen im Mail-Reiter öffnen und prüfen, dass alle Anhänge in der Vorgangsanlage sichtbar sind.
- Zwei Anhänge aktivieren und einen deaktiviert lassen; anschließend importieren und prüfen, dass genau zwei Belege am Vorgang hängen.
- Jeden Anhang einzeln auswählen oder vorschauen, um sicherzustellen, dass nicht nur der erste geladen wird.
- Eine Mail ohne Anhänge testen, damit der Dialog ohne Fehler bleibt.
- Eine Mail mit genau einem Anhang regressiv prüfen.

## Offene Fragen

- Reicht für die UI eine Liste mit umschaltbarer Einzelvorschau oder soll die Darstellung mehrere Vorschauen parallel zeigen?
- Soll die UI fehlende Analyseeinträge automatisch aus den rohen Anhängen ergänzen, falls Analyse und tatsächliche Attachments auseinanderlaufen?
