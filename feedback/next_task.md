# Nächstes Arbeitspaket

## Titel

Mail-Antworten: Zeilenumbrüche erhalten und Empfänger im Reply-Flow auswählbar machen

## Ziel

Der bestehende Mail-Antwort-Flow im Dashboard soll so verbessert werden, dass eingegebene Zeilenumbrüche im gesendeten Inhalt erhalten bleiben und beim Antworten/Versenden die Empfänger nicht starr sind, sondern aus dem vorhandenen Mailkontext ausgewählt bzw. angepasst werden können.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_mail_integration.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/mail_integration.py: Reply-Payload validieren, Textformat so erzeugen/übergeben, dass Zeilenumbrüche nicht verloren gehen, und Empfängerliste für den Graph-Reply/Send-Aufruf berücksichtigen.
- banking_dashboard/server.py: vorhandenen Reply-Endpunkt kompatibel erweitern, damit zusätzliche Empfängerfelder aus dem JSON-Body angenommen und an die Mail-Integration durchgereicht werden.
- banking_dashboard/static/app.js: Reply-UI-Daten sammeln, Textarea-Inhalt unverändert senden und Empfängerauswahl/-bearbeitung im bestehenden Mail-Flow ergänzen.
- banking_dashboard/static/index.html: kleine UI-Erweiterung für Empfängeranzeige/-auswahl im Reply-Bereich, ohne neue Hauptnavigation oder neues Modul.
- tests/test_mail_integration.py: Tests für Reply-Verhalten, insbesondere Erhalt von Zeilenumbrüchen und neue Empfängersteuerung.
- tests/test_dashboard.py: API-/Handler-Tests für den Reply-Endpunkt mit erweitertem Payload.

## Muss umgesetzt werden

- Bestehenden Reply-Endpunkt so erweitern, dass Text mit echten Zeilenumbrüchen serverseitig nicht zusammengedrückt oder falsch serialisiert wird.
- Sicherstellen, dass gesendete Antwortmails die im UI eingegebenen Absatz- und Zeilenumbrüche sichtbar behalten.
- Im bestehenden Mail-Reply-UI eine Empfängerauswahl oder bearbeitbare Empfängerliste anbieten, statt ausschließlich an einen fest vorgegebenen Empfänger zu senden.
- Empfängerwerte aus dem vorhandenen Mailkontext vorbelegen, sodass der Nutzer nicht alles neu eingeben muss.
- Serverseitig die neuen Empfängerfelder validieren und an die vorhandene Mail-Integration übergeben.
- Automatisierte Tests ergänzen, die mindestens den erweiterten Reply-Payload und den Erhalt von Zeilenumbrüchen absichern.

## Soll umgesetzt werden

- Vorbelegung der Empfänger so wählen, dass typische Antwortfälle direkt funktionieren, z. B. ursprünglicher Absender als Standard.
- Mehrere Empfänger nur im Rahmen des bestehenden Modells unterstützen, wenn die Mail-Integration das bereits natürlich abbilden kann.

## Nicht Teil dieses Arbeitspakets

- Vollwertiger neuer Mail-Composer für frei neue Mails.
- Adressdatenbank oder Kontaktverwaltung.
- Formatierungseditor mit Rich-Text/HTML-Werkzeugleiste.
- Änderungen am Mail-Zusammenfassungs-, Spam- oder Vorgang-Import-Flow.
- Die anderen Backlog-Punkte wie Transaktionssplits, Dashboard-Startseite, Fehlbuchungs-Flow oder aktuelle Transaktionen im Mail-Vorgangsanlegen.

## Akzeptanzkriterien

- Beim Antworten über das Dashboard bleiben manuell eingegebene Zeilenumbrüche in der versendeten Mail in sinnvoller Form erhalten.
- Der Reply-Endpunkt akzeptiert einen erweiterten Payload für Empfänger, ohne bestehende Grundfunktion zu brechen.
- Im UI kann der Nutzer vor dem Senden sehen und beeinflussen, an wen die Mail gesendet wird.
- Ohne explizite Änderung durch den Nutzer bleibt ein sinnvoller Standard-Empfänger aus dem Mailkontext vorbelegt.
- Bestehende Tests bleiben grün und neue Tests decken Zeilenumbrüche sowie Empfängerauswahl im Reply-Flow ab.

## Hinweise für den Umsetzungs-Agenten

- Da bereits POST /api/mail/<id>/reply existiert, sollte die Erweiterung abwärtskompatibel sein: vorhandene minimale Payloads möglichst weiterhin akzeptieren.
- Der Fehlerhinweis 'Ich kann auch nicht auswählen an wen' spricht eher für eine UI-/Payload-Erweiterung im vorhandenen Reply-Dialog als für einen komplett neuen Versand-Flow.
- Der Umsetzungs-Agent sollte in mail_integration.py prüfen, an welcher Stelle der Nachrichtentext für Microsoft Graph aufgebaut wird; dort entsteht wahrscheinlich der Zeilenumbruchverlust.
- Falls Graph HTML-Body erwartet, sollten Plaintext-Zeilenumbrüche kontrolliert in ein passendes Format übertragen werden, statt sie implizit zu verlieren.
- Tests sollten nicht nur String-Gleichheit prüfen, sondern konkret die Struktur des an das Mail-Backend gegebenen Reply-Inhalts und der Empfängerliste.

## Manuelle Testhinweise

- Im Dashboard eine Mail öffnen und im bestehenden Antwortbereich mehrere Absätze mit Leerzeilen eingeben; nach dem Senden prüfen, dass die Struktur erhalten bleibt.
- Empfängerliste im Reply-UI prüfen: Standardwert muss sinnvoll vorbelegt sein, danach Empfänger ändern und Versand erneut testen.
- Falls Testkonto verfügbar ist, Antwort an verschiedene ausgewählte Empfänger schicken und prüfen, dass die Empfänger wie im UI gesetzt übernommen werden.
- Negativtest: leere oder ungültige Empfängerangaben sollten einen verständlichen Fehler liefern statt stillschweigend an falsche Empfänger zu senden.

## Offene Fragen

- Soll die Empfängerauswahl nur 'An' betreffen oder auch CC/BCC im selben kleinen Paket mit abdecken?
- Soll bei Antworten standardmäßig ausschließlich an den ursprünglichen Absender gesendet werden oder optional auch an weitere ursprüngliche Empfänger?
