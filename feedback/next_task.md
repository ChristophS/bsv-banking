# Nächstes Arbeitspaket

## Titel

Split-Zeilen über bestehende Vorgänge Rechnungsbelegen zuordnen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 4

## Ziel

Für eine Split-Zeile soll eine gültige Zuordnung zu einem bereits mit der Ursprungstransaktion verknüpften Vorgang speicher- und abrufbar sein. Rechnungen und Teilrechnungen bleiben dabei ausschließlich über die bestehende Vorgang-Beleg-Verknüpfung zugeordnet.

## Relevante Dateien

- transaction_store/database.py
- banking_dashboard/server.py
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- transaction_store.database.replace_transaction_splits und zugehörige Validierung
- transaction_store.database.list_transaction_splits und Vorgangsabfragen
- Split-bezogene API-Endpunkte in banking_dashboard/server.py
- Split-, Vorgangs- und API-Tests in tests/test_transactions.py und tests/test_dashboard.py

## Muss umgesetzt werden

- Beim Speichern von Split-Zeilen validieren, dass eine gesetzte vorgangs_id existiert und mit der Ursprungstransaktion über transaktion_vorgaenge verknüpft ist.
- Ungültige, fremde oder nicht vorhandene Vorgangs-IDs mit einer verständlichen Validierungsfehlermeldung ablehnen, ohne vorhandene Splits teilweise zu verändern.
- Für die Split-API die zulässigen, mit der Ursprungstransaktion verknüpften Vorgänge einschließlich ihrer bereits über vorgang_belege verknüpften Belege abrufbar machen.
- Die bestehende atomare Split-Speicherung und die Prüfung, dass die Split-Summe exakt dem Transaktionsbetrag entspricht, erhalten.
- Automatisierte Tests für erfolgreiche Zuordnung, unbekannten Vorgang, nicht zur Transaktion gehörenden Vorgang, Belegdarstellung über den Vorgang und unveränderten Datenbestand nach Fehlern ergänzen.

## Soll umgesetzt werden

- Die API-Antwort so strukturieren, dass eine spätere Split-Editor-Oberfläche die zulässigen Vorgänge und deren Rechnungsbelege ohne zusätzliche Architekturannahmen als Auswahl darstellen kann.
- Leere vorgangs_id weiterhin als bewusst nicht zugeordneten Split zulassen.

## Nicht Teil dieses Arbeitspakets

- Split-Editor oder sonstige neue Bedienoberfläche im Dashboard.
- Automatisches Erstellen neuer Vorgänge, Belege oder Rechnungen.
- Direkte Beziehungen zwischen Transaktionen und Belegen oder zwischen Split-Zeilen und Belegen.
- Mehrere Rechnungen automatisiert auf Split-Zeilen verteilen oder Teilrechnungsbeträge extrahieren.
- Änderungen an Klassifikations-, Abschluss- oder Split-Summenlogik außerhalb der für die Zuordnung nötigen Validierung.

## Akzeptanzkriterien

- Eine Split-Zeile kann auf einen bestehenden Vorgang der Ursprungstransaktion verweisen und wird nach erneutem Laden mit derselben vorgangs_id ausgegeben.
- Die für einen Split auswählbaren Vorgänge enthalten nur Vorgänge, die über transaktion_vorgaenge mit dessen Ursprungstransaktion verbunden sind.
- Rechnungsbelege werden bei der Auswahl ausschließlich aus vorgang_belege des jeweiligen Vorgangs abgeleitet.
- Eine fremde oder unbekannte vorgangs_id wird abgewiesen; weder Split-Zeilen noch bestehende Zuordnungen werden dabei unvollständig überschrieben.
- Alle bestehenden sowie die neuen Transaktions- und Dashboard-Tests laufen ohne Browser, externe Dienste oder produktive Daten.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandene transaction_splits.vorgangs_id und die Tabellen transaktion_vorgaenge sowie vorgang_belege verwenden; keine neue fachliche Verknüpfungstabelle einführen.
- Die fachliche Rechnung-zu-Transaktion-Beziehung bleibt indirekt: Split → Vorgang ← Beleg und Vorgang ← Transaktion.
- Die Validierung vor dem DELETE/INSERT-Zyklus von replace_transaction_splits ausführen oder vollständig innerhalb des bestehenden Savepoints absichern.

## Manuelle Testhinweise

- Mit einer Fixture-Datenbank eine Transaktion mit mindestens zwei verknüpften Vorgängen und je einem Rechnungsbeleg anlegen.
- Einen Split einem dieser Vorgänge zuordnen, die Splits neu laden und die korrekte Vorgangs- und Beleginformation prüfen.
- Danach einen Vorgang einer anderen Transaktion übermitteln und prüfen, dass eine Validierungsfehlermeldung erscheint und die zuvor gespeicherten Splits unverändert bleiben.

## Offene Fragen

- Keine Angaben
