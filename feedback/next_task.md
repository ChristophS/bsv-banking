# Nächstes Arbeitspaket

## Titel

Verknüpfte Vorgangs-Mails bei Zuordnung direkt als gelesen markieren

## Ziel

Beim Erstellen oder Aktualisieren eines Vorgangs sollen verknüpfte Mails sofort lokal als gelesen markiert werden. Die bestehende Markierung beim manuellen Vorgangsabschluss bleibt unverändert bestehen.

## Relevante Dateien

- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/server.py: in DashboardDataStore.create_vorgang(...) nach erfolgreicher Verknüpfung von mail_ids die zugehörigen Mails über _mark_vorgang_mails_read markieren.
- banking_dashboard/server.py: in DashboardDataStore.update_vorgang(...) nach dem Aktualisieren der Verknüpfungen und vor commit die betroffenen Mails als gelesen markieren.
- tests/test_dashboard.py: Create- und Update-Fälle für Vorgänge mit mail_ids ergänzen bzw. absichern.

## Muss umgesetzt werden

- Beim Anlegen eines Vorgangs mit mail_ids die verknüpften inbox_messages lokal auf is_read = 1 setzen.
- Beim Aktualisieren eines bestehenden Vorgangs und Verknüpfen weiterer Mails diese Mails lokal als gelesen markieren.
- Die bestehende Abschlusslogik für Vorgänge nicht verändern.
- Automatisierte Tests für mindestens einen Create- und einen Update-Fall ergänzen.

## Soll umgesetzt werden

- Die Markierung idempotent halten, sodass bereits gelesene Mails unverändert bleiben.
- Vorhandene zentrale Helper-Logik verwenden statt neue SQL-Sonderfälle einzubauen.

## Nicht Teil dieses Arbeitspakets

- Mails bereits bei bloßer Vorschau oder Kandidatenanzeige als gelesen markieren.
- Microsoft-Graph-seitiges Markieren als gelesen außerhalb der lokalen Datenbanklogik.
- Neue UI-Funktionen für Mail-Vorschau, Anhänge oder Empfängerauswahl.

## Akzeptanzkriterien

- Wird ein neuer Vorgang mit mail_ids angelegt, sind die zugehörigen inbox_messages danach lokal als gelesen markiert.
- Wird eine Mail nachträglich mit einem bestehenden Vorgang verknüpft, ist sie danach lokal als gelesen markiert.
- Das bisherige Verhalten beim Abschluss eines Vorgangs bleibt bestehen.
- Die betroffenen Dashboard-Tests laufen erfolgreich durch.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandene Funktion _mark_vorgang_mails_read(connection, vorgangs_ids) ist die zentrale Stelle für die lokale Read-Markierung und soll wiederverwendet werden.
- Da create_vorgang und update_vorgang bereits über die Linktabellen arbeiten, ist der Zeitpunkt nach dem Verknüpfen und vor dem Commit naheliegend.
- Für dieses Paket ist keine neue Architektur nötig; es reicht, den offenen Verknüpfungsfall sauber an die vorhandene Logik anzudocken.

## Manuelle Testhinweise

- Eine ungelesene Mail über den Vorgangs-Flow mit einem Vorgang verknüpfen und prüfen, dass sie anschließend als gelesen erscheint.
- Einen bestehenden Vorgang um eine Mail ergänzen und prüfen, dass die Mail danach als gelesen markiert ist.
- Anschließend einen Vorgang abschließen und prüfen, dass die bisherige Abschluss-Markierung weiter funktioniert.

## Offene Fragen

- Keine offenen Fragen für dieses kleine Paket.
