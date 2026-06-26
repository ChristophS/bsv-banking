# Nächstes Arbeitspaket

## Titel

Spamerkennung und Verlauf-Markierung im Mail-Reiter stabilisieren

## Ziel

Die Spam-Bewertung soll wieder plausible Werte liefern und das Markieren einer Mail als gelesen muss auf den gesamten Conversation-Verlauf wirken, ohne die bestehende Graph- und lokalen Cache-Mechanismen umzubauen.

## Relevante Dateien

- banking_dashboard/mail_integration.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_mail_integration.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/mail_integration.py für Spam-Score-Berechnung, Cache-Trefferlogik und Conversation-Zuordnung.
- banking_dashboard/server.py für API-Endpunkte, die Gelesen-Markieren und Spam-Werte an die Oberfläche liefern.
- banking_dashboard/static/app.js für UI-Aktionen im Mail-Reiter und die Darstellung des Gelesen-Status pro Verlauf.
- tests/test_mail_integration.py für Scoring-/Cache-Fälle und Conversation-Handling.
- tests/test_dashboard.py für API- und UI-nahe Regressionen zu Gelesen-Markieren und Verlaufsauswirkungen.

## Muss umgesetzt werden

- Prüfen, warum die Spam-Scores derzeit bei 0% landen, und die wahrscheinliche Ursache in Heuristik, Cache oder API-Übergabe beheben.
- Sicherstellen, dass 'als gelesen markieren' beim ausgewählten Mailverlauf alle Nachrichten mit derselben conversationId als gelesen markiert.
- Dabei die bestehende Verlaufserkennung und die vorhandenen Graph-Operationen wiederverwenden, statt eine neue Statuslogik einzuführen.

## Soll umgesetzt werden

- Falls die Oberfläche nur Einzelmails markiert, die Batch-Aktion sichtbar auf den gesamten Verlauf erweitern oder klar an den Verlauf knüpfen.
- Die betroffenen Zustände im UI nach dem Markieren direkt aktualisieren, damit der Verlauf nicht inkonsistent angezeigt wird.

## Nicht Teil dieses Arbeitspakets

- Die Spam-Schwelle oder das manuelle Löschen von Spam ändern.
- Neue Mail-Automatisierungen wie Vorgangserstellung, Tagging-Redesign oder neue Filter einführen.
- Andere Feedbackpunkte wie Deckelliste, manuelle Gegenposition, Transaktionsfilter, Umbuchung oder Dokumentspeicherung in dieses Paket ziehen.

## Akzeptanzkriterien

- Mindestens ein realistisch simuliertes Mail-Beispiel liefert wieder einen plausiblen Spam-Score ungleich 0%, sofern die bisherigen Regeln oder Heuristiken dafür einen Treffer erzeugen sollten.
- Eine Mail wird im Dashboard als gelesen markiert und danach sind alle Nachrichten desselben conversation-Verlaufs im lokalen Zustand und in der UI als gelesen sichtbar.
- Bestehende Einzelmail-Fälle ohne conversationId oder mit nur einer Nachricht bleiben funktionsfähig.

## Hinweise für den Umsetzungs-Agenten

- Vor Änderungen zuerst die bestehende Conversation- und Inbox-ID-Logik in mail_integration.py und server.py prüfen, damit die Änderung auf die vorhandenen Datenstrukturen passt.
- Bei der Score-Reparatur zuerst prüfen, ob ein Fallback immer 0 zurückliefert oder ob das Ergebnis unterwegs auf 0 abgeschnitten wird.
- Die UI-Änderung sollte minimal bleiben und nur die vorhandene Liste- und Detailansicht für Gelesen-Status und Verlauf nutzen.

## Manuelle Testhinweise

- Im Mail-Reiter mehrere Nachrichten mit derselben conversationId laden, eine davon als gelesen markieren und prüfen, dass der gesamte Verlauf umspringt.
- Mehrere Mails mit unterschiedlicher Betreff-, Absender- und Vorschau-Struktur laden und prüfen, dass der Spam-Score nicht pauschal 0% ist, wenn die Heuristik eigentlich anschlagen sollte.

## Offene Fragen

- Ist der 0%-Spamwert ein echter Berechnungsfehler oder wird nur ein vorhandener sehr kleiner Cachewert auf 0 gerundet?
- Soll 'gelesen markieren' künftig ausdrücklich im Kontext des Verlaufs-Buttons passieren oder reicht ein implizites Ausweiten der bestehenden Aktion?
