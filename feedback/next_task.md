# Nächstes Arbeitspaket

## Titel

Vorgangsstatus aus klassifizierten Split-Zeilen ableiten

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.3

## Ziel

Die bestehende vorgangsbasierte Statusableitung so ergänzen, dass klassifizierte Split-Zeilen bei der automatischen Abschlussprüfung berücksichtigt werden, ohne manuell gesetzte Vorgangsstatus zu überschreiben.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/classification.py
- banking_dashboard/server.py
- banking_dashboard/static/app.js
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- transaction_store/database.py: Split-Speicherung sowie Trigger und Invariante für Vorgangsstatus
- transaction_store/classification.py: gemeinsame Prüfung auf vollständige Klassifikation, falls dafür eine wiederverwendbare Hilfsfunktion sinnvoll ist
- banking_dashboard/server.py: Rückgabe des aus Splits abgeleiteten Status in bestehenden Detail- oder Split-Antworten
- banking_dashboard/static/app.js: Aktualisierung der bestehenden Statusanzeige nach dem Speichern von Split-Zeilen, soweit die API dies bereits unterstützt
- tests/test_transactions.py: Datenbank- und Statusfälle für vollständig, unvollständig und manuell gesetzte Vorgänge
- tests/test_dashboard.py: API-Regressionstest für sichtbare Statusaktualisierung, sofern der Status über Dashboard-Endpunkte geliefert wird

## Muss umgesetzt werden

- Die fachliche Regel für automatisch abgeleitete Vorgangsstatus anhand der vorhandenen Split-Struktur präzise implementieren: Ein nicht manuell gesetzter Vorgang darf nur automatisch abgeschlossen sein, wenn alle für ihn relevanten Transaktions- und Split-Klassifikationen vollständig sind und die bestehende Abschlusslogik dies zulässt.
- Bei unvollständiger Split-Klassifikation muss ein automatisch abgeleiteter abgeschlossener Vorgang wieder auf "in_bearbeitung" gesetzt werden.
- Beim Ersetzen, Hinzufügen, Entfernen oder Bearbeiten von Split-Zeilen muss die Statusableitung innerhalb derselben Datenbankänderung erneut geprüft werden.
- Manuell gesetzte Vorgangsstatus dürfen durch die automatische Split-Statusableitung weder überschrieben noch zurückgesetzt werden.
- Die vorhandenen Tabellen `vorgaenge`, `transaktion_vorgaenge`, `transaction_splits` und die bestehende vorgangsbasierte Abschlusslogik verwenden; keine direkte Beleg-Transaktions-Beziehung einführen.
- Unit-Tests mit temporärer SQLite-Datenbank ergänzen; keine Browser-, Banking- oder sonstigen externen Zugriffe ausführen.

## Soll umgesetzt werden

- Die Klassifikationsvollständigkeit von Transaktionen und Splits über eine konsistente, gut testbare Hilfslogik bewerten, statt ähnliche SQL-Bedingungen an mehreren Stellen auseinanderlaufen zu lassen.
- Sicherstellen, dass ein Vorgang ohne Splits sein bisheriges Statusverhalten unverändert beibehält.
- Sofern bestehende API-Antworten Split- und Vorgangsdaten zusammen ausliefern, den neu abgeleiteten Status nach einer Split-Speicherung unmittelbar zurückgeben.

## Nicht Teil dieses Arbeitspakets

- Neue Split-Editor-Oberflächen oder ein breiter UI-Umbau.
- Rechnungs-, Teilrechnungs- oder Belegzuordnungen für Split-Zeilen.
- Neue Vorgangstypen oder eine grundlegende Änderung der bestehenden Abschlussregelverwaltung.
- Automatische produktive Aktionen gegen Banking-, Mail-, DFBnet- oder andere externe Dienste.
- Änderungen an der fachlichen Klassifikation der ursprünglichen Transaktion außerhalb der für die Statusableitung notwendigen Integration.

## Akzeptanzkriterien

- Ein automatisch verwalteter Vorgang mit relevanten unvollständig klassifizierten Split-Zeilen hat den Status `in_bearbeitung`.
- Ein zuvor automatisch abgeschlossener Vorgang wird bei einer nachträglich unvollständig gemachten Split-Zeile auf `in_bearbeitung` zurückgesetzt.
- Ein manuell auf `abgeschlossen` oder `in_bearbeitung` gesetzter Vorgang behält seinen manuellen Status trotz Änderungen an Split-Zeilen.
- Das Ersetzen von Splits ist weiterhin atomar: Bei ungültiger Split-Summe oder sonstigem Fehler bleiben weder Splits noch Vorgangsstatus teilweise geändert zurück.
- Vorgänge ohne Splits verhalten sich in den vorhandenen Tests weiterhin wie vor der Änderung.
- Die ergänzten Unit-Tests laufen ohne Netzwerk, Browser, Credentials oder produktive Daten.

## Hinweise für den Umsetzungs-Agenten

- Die aktuelle Statusinvariante in `transaction_store/database.py` prüft verknüpfte Transaktionen. Die Erweiterung muss Split-Zeilen ergänzen, ohne die vorhandene N:M-Zuordnung Transaktion–Vorgang zu umgehen.
- Da `transaction_splits.vorgangs_id` optional ist, muss die Umsetzung eindeutig festlegen, welche Split-Zeilen für welchen Vorgang relevant sind. Dabei sind nur bestehende Vorgangsreferenzen und die Zuordnung der Ursprungstransaktion zu verwenden.
- Statusänderungen sollen nur für nicht manuelle Vorgänge erfolgen (`status_manuell = 0`) und die vorhandenen Statuswerte `in_bearbeitung` sowie `abgeschlossen` beibehalten werden.
- Falls SQLite-Trigger für Split-Änderungen ergänzt werden, müssen diese für INSERT, UPDATE und DELETE konsistent wirken und mit `replace_transaction_splits` kompatibel sein.

## Manuelle Testhinweise

- Lokale Testdatenbank mit einer Transaktion, einem Vorgang und zugeordneten Split-Zeilen anlegen.
- Einen automatisch verwalteten Vorgang bei vollständigen Klassifikationen prüfen und anschließend ein Pflichtfeld eines Splits leeren; der Status muss auf `in_bearbeitung` wechseln.
- Den Vorgangsstatus manuell setzen, danach Split-Daten ändern und bestätigen, dass der manuelle Status unverändert bleibt.
- Eine ungültige Split-Summe speichern versuchen und prüfen, dass weder Split-Liste noch Vorgangsstatus verändert wurden.

## Offene Fragen

- Die genaue Semantik für Split-Zeilen ohne `vorgangs_id` sollte anhand des bestehenden Split-UI/API-Verhaltens bestätigt werden: Sollen sie den automatisch erzeugten Vorgang ihrer Ursprungstransaktion beeinflussen oder nur bei expliziter Vorgangszuordnung?
- Es ist zu klären, ob die vorhandene Abschlussregelverwaltung bereits Split-Klassifikationen auswertet oder ob diese Erweiterung bewusst auf die reine Vollständigkeitsinvariante begrenzt bleibt.
