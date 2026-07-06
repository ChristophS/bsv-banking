# Nächstes Arbeitspaket

## Titel

Abschlussstatus und Mail-Lesestatus nach manueller oder regelbasierter Vorgangsabwicklung sofort nachziehen

## Ziel

Sicherstellen, dass abgeschlossene Vorgänge nach manueller Statusänderung oder nach Klassifikation mit greifender Abschlussregel sofort konsistent wirken: betroffene Transaktionen verschwinden bei aktivem Filter für abgeschlossene Vorgänge zuverlässig und verknüpfte Mails werden als gelesen markiert.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_dashboard.py
- transaction_store/database.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: in DashboardDataStore.update_vorgang_status() nach erfolgreicher manueller Statusänderung abhängige Folgeaktionen ausführen.
- banking_dashboard/server.py: in DashboardDataStore.update_transaction_classification() nach apply_completion_rules(...) zusätzlich die tatsächlich betroffenen bzw. abgeschlossenen Vorgänge und deren Mails nachziehen.
- banking_dashboard/server.py: kleine Hilfsfunktion(en) im DashboardDataStore für das Markieren verknüpfter Mails als gelesen und ggf. zum Ermitteln der von einer Transaktion betroffenen Vorgänge.
- banking_dashboard/static/app.js: nach erfolgreicher PATCH-Antwort die Transaktionsliste mit aktuellem Filter neu laden, falls die UI den Status nicht ohnehin serverseitig neu abfragt.
- tests/test_dashboard.py: Dashboard-/API-Tests für manuellen Abschluss, Abschluss nach Klassifikation und Mail-is_read-Nachzug ergänzen.

## Muss umgesetzt werden

- Beim manuellen Abschließen eines Vorgangs über update_vorgang_status() alle über inbox_vorgaenge verknüpften, nicht gelöschten Mails in inbox_messages auf gelesen setzen.
- Beim Klassifizieren einer Transaktion über update_transaction_classification() nach apply_completion_rules(...) sicherstellen, dass dadurch neu abgeschlossene Vorgänge ebenfalls ihre verknüpften Mails als gelesen markieren.
- Sicherstellen, dass der Transaktionsfilter hide_completed_vorgaenge nach diesen Änderungen ohne zusätzlichen erneuten Speichervorgang sofort korrekt greift; falls das Problem im Frontend-Refresh liegt, nach erfolgreicher PATCH-Antwort die Transaktionsliste unter Beibehaltung des aktuellen Filters neu laden.
- Nur tatsächlich abgeschlossene Vorgänge/Mails nachziehen; beim Wiederöffnen keine automatische Rücksetzung auf ungelesen vornehmen.

## Soll umgesetzt werden

- Falls sinnvoll, den Nachziehschritt in eine kleine interne Hilfsfunktion kapseln, damit manueller und regelbasierter Abschluss denselben Pfad nutzen.
- Falls Tests es nahelegen, den Nachziehschritt auch beim Anlegen eines bereits abgeschlossenen Vorgangs konsistent anwenden, ohne den Paketumfang unnötig zu vergrößern.

## Nicht Teil dieses Arbeitspakets

- Originaldokument statt Katalogeintrag aus dem Dokument-Flow öffnen.
- Transaktionen splitten und Teilbeträge mehreren Kategorien oder Rechnungen zuordnen.
- Eine bestehende Transaktion einem vorhandenen Vorgang zuordnen und passende Vorgänge vorschlagen.
- Mehrere Anhänge einer Mail in der Vorgangsanlage sichtbar machen.
- Allgemeine Dashboard- oder UX-Themen außerhalb des Abschluss- und Lesestatus-Refreshs.

## Akzeptanzkriterien

- Wenn ein Vorgang manuell auf abgeschlossen gesetzt wird und mit mindestens einer Transaktion verknüpft ist, erscheint diese Transaktion bei aktivem Filter 'Transaktionen zu abgeschlossenen Vorgängen ausblenden' nicht mehr, sofern sie keinem weiteren offenen Vorgang zugeordnet ist.
- Wenn eine Transaktion so klassifiziert wird, dass eine aktive Abschlussregel greift, wirkt der Abschluss unmittelbar nach dem Speichern; ein separates erneutes Speichern der Abschlussregel ist nicht nötig.
- Beim manuellen oder regelbasierten Abschluss eines Vorgangs werden alle über inbox_vorgaenge verknüpften, nicht gelöschten Mails in inbox_messages auf gelesen gesetzt.
- Beim Wiederöffnen eines Vorgangs bleiben bereits auf gelesen gesetzte Mails gelesen.
- Bestehende Semantik des Filters bleibt erhalten: Transaktionen mit mindestens einem offenen Vorgang bleiben sichtbar, auch wenn zusätzlich ein abgeschlossener Vorgang verknüpft ist.

## Hinweise für den Umsetzungs-Agenten

- Das gemeldete Filterproblem passt eher zu fehlendem Status- oder Listen-Refresh als zu einer falschen SQL-Filterbedingung; die Filter-Query in list_transactions() nur ändern, wenn ein Test einen echten Backendfehler zeigt.
- Für den Mail-Nachzug kann eine direkte SQL-Aktualisierung von inbox_messages.is_read genutzt werden, eingeschränkt auf inbox_vorgaenge des betroffenen Vorgangs und deleted_at IS NULL.
- Da update_transaction_classification() aktuell nur die betroffene Transaktion kennt, ist es sinnvoll, vor oder nach apply_completion_rules(...) die zugehörigen Vorgänge bzw. deren Statusänderungen zu ermitteln und nur für neu abgeschlossene Vorgänge den Mail-Nachzug auszuführen.
- Die PATCH-Endpunkte liefern bereits aktualisierte Payloads zurück; falls die UI die Liste nicht neu lädt, sollte app.js nach erfolgreicher Klassifikations- oder Statusänderung die aktuelle Transaktionsliste mit aktivem hide_completed_vorgaenge-Filter erneut abrufen.

## Manuelle Testhinweise

- Transaktion öffnen, zugehörigen Vorgang manuell abschließen, dann in der Transaktionsliste den Filter 'Transaktionen zu abgeschlossenen Vorgängen ausblenden' aktivieren: die Transaktion darf nicht mehr sichtbar sein, solange kein weiterer offener Vorgang verknüpft ist.
- Eine ungelesene Mail mit einem Vorgang verknüpfen, Vorgang abschließen, danach im Mail-Bereich oder direkt in der DB/API prüfen, dass is_read=true ist.
- Eine Transaktion so klassifizieren, dass eine vorhandene Abschlussregel greift; direkt nach dem Speichern prüfen, dass derselbe Filtereffekt ohne erneutes Öffnen oder Speichern der Abschlussregel eintritt.
- Gegenprobe: Vorgang wieder öffnen; Mail bleibt gelesen und die Transaktion erscheint mit aktivem Filter wieder, falls nun ein offener Vorgang existiert.

## Offene Fragen

- Soll das automatische Setzen von Mails auf gelesen nur bei abgeschlossenen Vorgängen gelten oder auch schon bei jeder bloßen Verknüpfung? Dieses Paket beschränkt sich bewusst auf Abschlussfälle.
- Falls das UI-Problem reproduzierbar ist: Tritt die falsche Sicht nur in der aktuellen Browseransicht auf oder liefert auch GET /api/transactions?hide_completed_vorgaenge=true noch falsche Daten? Das sollte bei der Umsetzung kurz verifiziert werden.
