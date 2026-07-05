# Nächstes Arbeitspaket

## Titel

Mail-Import um kontrollierten direkten Abschluss ergänzen

## Ziel

Im bestehenden Mail-zu-Vorgang-Import soll ein neuer Vorgang auf Wunsch direkt abgeschlossen werden können, aber nur über die vorhandenen Abschlussregeln und nur im bisherigen Mail-Import-Flow. Standardverhalten und bestehende Verknüpfungen bleiben unverändert.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/rules.py
- transaction_store/classification.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Importdialog um eine explizite Option 'direkt abschließen' und die Anbindung des Payloads ergänzen.
- banking_dashboard/static/index.html: falls der Mail-Importdialog statisch definiert ist, Checkbox/Option und kurzen Hinweis ergänzen.
- banking_dashboard/server.py: _mail_vorgang_import(...) so anpassen, dass der optionale Abschluss sauber validiert und verständlich zurückgemeldet wird.
- tests/test_dashboard.py: gezielte API-Tests für erfolgreichen und abgewiesenen Direktabschluss im Mail-Import ergänzen.

## Muss umgesetzt werden

- Im bestehenden Mail-Import-Flow eine explizite Option für 'direkt abschließen' unterstützen.
- Für den Abschluss ausschließlich die vorhandene Abschlussprüfung verwenden.
- Wenn die Voraussetzungen nicht erfüllt sind, darf der Vorgang nicht fälschlich als abgeschlossen gespeichert werden.
- Die Antwort des Mail-Imports soll erkennbar machen, ob der Vorgang am Ende abgeschlossen oder offen geblieben ist.
- Automatisierte Tests für mindestens einen erfolgreichen und einen abgewiesenen Fall ergänzen.

## Soll umgesetzt werden

- Die neue Option im UI standardmäßig ausgeschaltet lassen.
- Im UI kurz erklären, dass direkter Abschluss nur bei erfüllten Voraussetzungen funktioniert.

## Nicht Teil dieses Arbeitspakets

- Generischer Ein-Klick-Workflow für manuelle Vorgangserstellung außerhalb des Mail-Import-Flows.
- Inline-Klassifikation von Transaktionen direkt im Erstellungsdialog.
- Neue Datenmodellbeziehungen für Beleg-zu-Transaktion.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Größere Dashboard-Usability-Überarbeitung.

## Akzeptanzkriterien

- Der Client kann beim Mail-Import einen Abschlusswunsch mitsenden, ohne dass der Standard-Import bricht.
- Erfüllt der importierte Vorgang alle vorhandenen Abschlussvoraussetzungen, ist er nach dem Import abgeschlossen.
- Sind die Voraussetzungen nicht erfüllt, bleibt der Vorgang offen oder der Import liefert eine verständliche Validierungsrückmeldung; er wird nicht fälschlich abgeschlossen.
- Bestehende Verknüpfungen zu Mail, Dokumenten, To-Dos, Terminen und weiteren Links bleiben erhalten.
- Automatisierte Tests decken mindestens Erfolg und Misserfolg des direkten Abschlusses ab.

## Hinweise für den Umsetzungs-Agenten

- In _mail_vorgang_import(...) existiert bereits requested_completed; zuerst prüfen, ob das Frontend diesen Wert schon sendet.
- Der Vorgang wird aktuell bewusst zuerst mit completed=false angelegt und danach optional via update_vorgang_status(..., true) abgeschlossen. Dieses Muster beibehalten, weil Dokumente und weitere Links erst nach der Anlage vollständig vorliegen.
- Falls update_vorgang_status(...) bei nicht erfüllten Voraussetzungen einen ValueError wirft, sollte der Request nicht als generischer 500 enden, sondern fachlich verständlich antworten.
- Die bestehende Abschlusslogik in transaction_store/rules.py und transaction_store/classification.py wiederverwenden, nicht duplizieren.
- Rechnungsvorgänge dürfen nur direkt abgeschlossen werden, wenn die bestehenden Mindestanforderungen an Transaktion und Dokument erfüllt sind.

## Manuelle Testhinweise

- Im Dashboard den Mail-Reiter öffnen, einen Vorgang aus einer Mail importieren und die neue Option aktivieren.
- Fall 1: Vorgang ohne ausreichende Klassifikation oder ohne nötige Verknüpfungen importieren; er darf nicht fälschlich abgeschlossen werden.
- Fall 2: Rechnungsvorgang mit verknüpfter Transaktion und Dokument importieren; bei erfüllten Regeln soll er direkt abgeschlossen erscheinen.
- Den gleichen Import mit deaktivierter Option testen; das bisherige Verhalten muss erhalten bleiben.

## Offene Fragen

- Soll ein nicht erfüllbarer Abschlusswunsch den gesamten Import mit 400 abbrechen oder den Vorgang offen importieren und nur den Abschluss verweigern?
- Falls der UI-Flow bereits ein completed-Feld kennt: fehlt nur die Erklärung oder auch die tatsächliche Anbindung im Frontend?
