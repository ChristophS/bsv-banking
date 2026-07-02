# Nächstes Arbeitspaket

## Titel

Spam-Score-Nullwerte und Cache-Verhalten in der Mailbewertung korrigieren

## Ziel

Sicherstellen, dass sehr kleine oder nullartige Spam-Werte in der Mailbewertung konsistent behandelt werden und nicht durch Cache-, Normalisierungs- oder Anzeigeeffekte fälschlich als dauerhafter 0-%-Wert wirken.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- tests/test_mail_integration.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/mail_integration.py: zentrale Stelle für _score_messages(), _normalize_spam_result(), MailProcessingCache.get()/put() und Fallback-/Cache-Entscheidungen.
- tests/test_mail_integration.py: Grenzfälle für 0, sehr kleine Wahrscheinlichkeiten, Cache-Wiederverwendung und Fallback-Verhalten absichern.
- tests/test_dashboard.py: prüfen, ob Listen- und Detailantworten dieselben spamProbability-Werte ausgeben, falls die Darstellung betroffen ist.

## Muss umgesetzt werden

- Repo-konkret analysieren, warum sehr kleine Spam-Werte als 0 % erscheinen und ob das durch Normalisierung, Rundung, Cache-Wiederverwendung oder Fallback entsteht.
- Die bestehende Grenze MIN_REUSABLE_SPAM_PROBABILITY so anwenden, dass Werte darunter nicht als verlässlicher Cachetreffer behandelt werden, aber innerhalb eines Ladevorgangs keine inkonsistenten Ergebnisse entstehen.
- Verhindern, dass legitime kleine Wahrscheinlichkeiten unnötig auf 0 gedrückt werden, wenn dadurch ein irreführender Dauer-0-Eindruck entsteht.
- Automatisierte Tests für die relevanten Grenzfälle ergänzen oder anpassen.

## Soll umgesetzt werden

- Falls nötig, die API-/Dashboard-Ausgabe so absichern, dass sehr kleine Werte konsistent angezeigt werden und nicht widersprüchlich zwischen Listen- und Detailansicht sind.
- Im Code kurz dokumentieren, welche fachliche Bedeutung die Grenze MIN_REUSABLE_SPAM_PROBABILITY hat.

## Nicht Teil dieses Arbeitspakets

- Ein-Klick-Workflow für Vorgangserstellung, Klassifikation und Abschluss.
- Suche oder Filter für große Vorgangslisten im Mail-Zuordnungsflow.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Spendenbescheinigungen, Adressdatenbank oder DFBnet-Integration.
- Allgemeine Dashboard-Usability-Überarbeitung.

## Akzeptanzkriterien

- Sehr kleine Spam-Werte werden konsistent behandelt und erzeugen keinen irreführenden Dauer-0-%-Eindruck.
- Werte oberhalb der Wiederverwendungsgrenze werden weiterhin aus dem Cache wiederverwendet.
- Fehler im Remote-Scoring fallen weiterhin kontrolliert auf fallback_spam_score() zurück, ohne normale erfolgreiche Bewertungen zu verschlechtern.
- Listen- und Detail-API liefern für dieselbe Mail im selben Zustand konsistente spamProbability-Werte.
- Neue oder angepasste Tests decken 0, 0.001, 0.0049, 0.005 und Cache-Verhalten ab.

## Hinweise für den Umsetzungs-Agenten

- Die relevante Logik ist bereits konzentriert in MailProcessingCache.get(), _score_messages(), _normalize_spam_result() und den lokalen/Remote-Scorern.
- Die README-Regel, dass Werte unter 0,5 % nicht als verlässlicher Cachetreffer gelten, soll beibehalten und sauber umgesetzt werden.
- Wenn das Problem hauptsächlich in der Anzeige liegt, trotzdem die Rohwerte und die API-Konsistenz mitprüfen, damit List- und Detailansicht nicht auseinanderlaufen.

## Manuelle Testhinweise

- Mail-Reiter mit mindestens einer legitimen Mail mit sehr niedrigem Spam-Score und einer klar verdächtigen Mail laden.
- Mehrfach neu laden und prüfen, ob sehr kleine Scores nicht fälschlich als stabiler immergleicher 0-%-Wert wirken.
- Eine Mail in Listen- und Detailansicht vergleichen und prüfen, ob spamProbability konsistent ist.
- Falls OpenAI nicht verfügbar ist, auch den Fallback-Pfad prüfen.

## Offene Fragen

- Ob das Nutzerproblem primär aus echter 0.0-Wahrscheinlichkeit, Rundung kleiner Werte auf 0 % oder einer Cache-/Fallback-Regression stammt, muss anhand der vorhandenen Tests bzw. Reproduktion verifiziert werden.
