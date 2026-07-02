# Nächstes Arbeitspaket

## Titel

Spam-Score: Ungültige Remote-Antworten sauber auf lokalen Fallback umstellen

## Ziel

Die Spam-Bewertung im Mail-Reiter soll bei fehlenden, unparsebaren oder falsch benannten Modellantworten nicht mehr stillschweigend als 0 % erscheinen. Stattdessen sollen solche Antworten zuverlässig als ungültig erkannt, auf die lokale Heuristik zurückgeführt und nachvollziehbar als lokaler Fallback dargestellt werden. Gültige 0-Werte bleiben möglich, wenn sie explizit und korrekt geliefert werden.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- tests/test_mail_integration.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/mail_integration.py: OpenAISpamScorer.score und/oder _normalize_spam_result, damit fehlende, anders benannte oder unparsebare probability-Werte nicht stillschweigend zu 0 normalisiert werden.
- banking_dashboard/mail_integration.py: _score_messages, damit fehlerhafte oder formal falsche Scorer-Ergebnisse sicher in fallback_spam_score münden.
- tests/test_mail_integration.py: Tests für ungültige OpenAI-Antworten, korrektes Fallback-Verhalten und Nicht-Verwechslung von fehlender probability mit explizit 0.

## Muss umgesetzt werden

- Analysieren und beheben, warum ungültige OpenAI-Antworten aktuell als probability=0 durchlaufen können.
- Fehlende, unparsebare oder nur implizit vorhandene Wahrscheinlichkeitswerte als ungültig behandeln, statt sie stillschweigend auf 0 zu setzen.
- Bei ungültigen Remote-Ergebnissen fallback_spam_score verwenden und spamSource nachvollziehbar als local_fallback setzen.
- Gültige 0-Werte nur dann akzeptieren, wenn die Modellantwort eindeutig eine gültige Wahrscheinlichkeit 0 oder 0.0 liefert.
- Sicherstellen, dass Ergebnisse unter MIN_REUSABLE_SPAM_PROBABILITY weiterhin nicht als verlässlicher Cachetreffer wiederverwendet werden.
- Automatisierte Tests ohne echte OpenAI-, Graph- oder Outlook-Aufrufe ergänzen.

## Soll umgesetzt werden

- Falls nötig, das OpenAI-Systemprompt so schärfen, dass die Antwort ein stabiles JSON-Schema mit probability als Zahl zwischen 0 und 1 und reasons als Liste kurzer Strings liefert.
- Bei Fallback wegen Parsing- oder Antwortfehlern einen kurzen, unkritischen Hinweis in spamReasons aufnehmen.

## Nicht Teil dieses Arbeitspakets

- Die Spam-Klassifikation fachlich neu trainieren oder ein neues Scoring-System einführen.
- Mail-Volltext oder Anhänge in die Spam-Bewertung aufnehmen.
- Automatische Löschlogik, Schwellenwert-Mechanik oder Sammellöschung funktional ändern.
- Dashboard-UI-Anzeigen außerhalb der Spam-Bewertung anpassen.
- Mail-Zuordnung zu Vorgängen oder andere Inbox-/Vorgangs-Workflows verändern.

## Akzeptanzkriterien

- Wenn OpenAI eine Antwort ohne gültige Wahrscheinlichkeit liefert, wird kein OpenAI-Score von 0 % angezeigt, sondern ein lokaler Fallback-Score mit source='local_fallback'.
- Wenn OpenAI eine gültige Wahrscheinlichkeit liefert, wird sie korrekt auf 0..1 normalisiert und als spamProbability ausgegeben.
- Eine explizit gültige probability=0 bleibt möglich; fehlende oder fehlerhafte probability wird nicht damit verwechselt.
- Sehr niedrige Scores unter MIN_REUSABLE_SPAM_PROBABILITY werden beim erneuten Laden weiterhin nicht als stabiler Cachetreffer wiederverwendet.
- Die Tests laufen ohne echte OpenAI-, Graph- oder Outlook-Netzwerkzugriffe erfolgreich durch.

## Hinweise für den Umsetzungs-Agenten

- Die bestehende Datenschutzgrenze in OpenAISpamScorer.score beibehalten: nur Betreff, Absender, Empfangszeit und bodyPreview an OpenAI senden.
- _normalize_spam_result ist der naheliegende Ort für robuste Validierung; fehlende oder unparsebare probability sollte dort nicht stillschweigend als 0 enden.
- Alternativfeldnamen nur eng begrenzt unterstützen, z. B. probability, spam_probability oder spamProbability.
- Prozentstrings wie '70%' dürfen bei klarer Erkennbarkeit auf 0.70 normalisiert werden; unbegrenzte Zahlen oder beliebige Felder nicht erraten.
- Die vorhandene Cache-Logik beibehalten; keine neue Bewertungsarchitektur einführen.
- Bei Tests HTTP/OpenAI-Aufrufe mocken, nicht den echten Endpunkt verwenden.

## Manuelle Testhinweise

- Dashboard lokal starten und den Mail-Reiter öffnen.
- Mit fehlendem OPENAI_API_KEY prüfen, dass Mails local_fallback-Scores erhalten.
- Mit vorhandenem OPENAI_API_KEY mehrere ungelesene Mails laden und kontrollieren, dass nicht auffällig viele Einträge ohne Grund als 0 % erscheinen.
- Dashboard neu laden und prüfen, dass sehr niedrige/0-nahe Scores nicht dauerhaft als scheinbar verlässliche Treffer hängen bleiben.

## Offene Fragen

- Welche minimalen alternativen Feldnamen für die Modellantwort sollen akzeptiert werden, ohne zu permissiv zu werden?
- Soll ein kurzer Fallback-Hinweis in spamReasons sichtbar sein oder nur intern für Diagnosen verwendet werden?
