# Implementation Report

## Branchname

agent2/codex-20260706-103831

## Geaenderte Dateien

- feedback/implementation_report.md

## Umgesetzte Punkte

- Der vorhandene Backlog-Punkt "Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen" wurde repo-konkret analysiert.
- Die bestehende Vorgangszentrierung bleibt fachliche Leitplanke: Mail zu Vorgang ueber `inbox_vorgaenge`, Transaktion zu Vorgang ueber `transaktion_vorgaenge`, Beleg zu Vorgang ueber `vorgang_belege`.
- Es wurde kein neues Datenmodell und keine direkte Beleg-Transaktions-Verknuepfung vorgeschlagen oder eingefuehrt.
- Die betroffenen bestehenden Einstiegspunkte wurden benannt:
  - `banking_dashboard/server.py`: `DashboardDataStore.create_vorgang()`, `DashboardDataStore.update_vorgang()`, `DashboardDataStore.vorgang_detail()`, `_mails_for_vorgang()`, `_belege_for_vorgang()`, `link_beleg_vorgang()`, `unlink_beleg_vorgang()`, `_mail_vorgang_import()`, `GET/PATCH /api/vorgaenge/{vorgangs_id}`, `POST/DELETE /api/belege/{beleg_id}/vorgaenge`, `GET/POST /api/mail/{entry_id}/vorgaenge`, `POST /api/mail/{entry_id}/vorgang-import`.
  - `banking_dashboard/static/app.js`: Mail-Tab und Mail-Detailaktionen, `renderVorgangCreateForm()`, `createVorgangMetadataEditor()`, `appendVorgangEntitySections()`, `renderVorgangWorkspace()`, `renderBelegEntityPreview()`, `renderTransactionContent()`.
  - `banking_dashboard/static/index.html`: bestehende Tabs `Mails`, `Vorgaenge`, `Transaktionen` und der gemeinsame Detaildialog als UI-Rahmen.
  - `transaction_store/database.py`: Tabellen `vorgaenge`, `transaktion_vorgaenge`, `belege`, `vorgang_belege`; eine direkte aktuelle Tabelle fuer Beleg zu Transaktion existiert nicht als Zielmodell.
- Groessere Teilaspekte wie automatische Aufteilung, Massenzuordnung, komplexe UX und KI/OCR bleiben im Backlog und wurden nicht umgesetzt.

## Praezisiertes Folgebriefing

Titel: Sichtbarkeit von Mailanhaengen im gemeinsamen Vorgang vorbereiten

Ziel: Fuer den Kernfall "eine Mail mit mehreren Anhaengen gehoert zu einem gemeinsamen Vorgang, der mehrere Transaktionen und mehrere Belege enthaelt" soll die bestehende Vorgangsdetailansicht so vorbereitet werden, dass Review und spaetere Umsetzung klar sehen, welche Mails, Transaktionen und Dokumente in demselben Vorgang gemeinsam betrachtet werden. Die Verknuepfung bleibt ausschliesslich vorgangszentriert.

Kleinstes erstes Folgepaket:

- In der Vorgangsdetailansicht die bereits geladenen Listen `vorgang.mails`, `vorgang.transaktionen` und `vorgang.belege` enger zusammen sichtbar machen.
- Den bestehenden Abschnitt "Zugeordnete Entitaeten" in `appendVorgangEntitySections()` als Einstieg nutzen und dort besonders Mails mit `attachment_count` sowie Dokumente aus demselben Vorgang besser unterscheidbar anzeigen.
- Keine neue Persistenz einfuehren. Speichern und Laden bleiben ueber `PATCH /api/vorgaenge/{vorgangs_id}` mit `mail_ids`, `transaction_ids` und `beleg_ids` sowie ueber die bestehenden Link-Endpunkte.
- Optional als kleinste API-Ergaenzung, falls die UI dafuer Detaildaten braucht: `vorgang_detail()` kann die vorhandenen Mailfelder aus `_mails_for_vorgang()` erweitern, zum Beispiel um eindeutig vorhandene Anhangsmetadaten aus der bestehenden Mail-Schicht. Das darf nur erfolgen, wenn diese Daten bereits lokal verfuegbar sind und keine externe Mail-Abfrage ausloesen.

Nicht Teil des Folgepakets:

- Keine automatische fachliche Zuordnung einzelner Anhaenge zu einzelnen Transaktionen.
- Keine neue Tabelle wie `transaktion_belege` oder direkte Beleg-Transaktions-Relation.
- Keine Massenzuordnung ueber mehrere Vorgaenge.
- Keine neue Import-Engine und keine OCR-/KI-Aufteilung.
- Keine externe Mail-, Banking- oder Login-Aktion.

Akzeptanz fuer das Folgepaket:

- Eine Mail mit mehreren Anhaengen bleibt in einem gemeinsamen Vorgang sichtbar.
- Mehrere Transaktionen und mehrere Belege desselben Vorgangs sind im Vorgangsdetail gemeinsam und unterscheidbar dargestellt.
- Die bestehenden Tabellen `inbox_vorgaenge`, `transaktion_vorgaenge` und `vorgang_belege` bleiben die einzigen fachlichen Verknuepfungen fuer diesen Fall.
- Der bestehende Mail-Import ueber `_mail_vorgang_import()` kann weiterhin Dokumente in denselben Vorgang importieren.

## Nicht umgesetzte Punkte

- `feedback/next_task.md` und `feedback/backlog.md` wurden gemaess Prompt-Vorgabe nicht geaendert.
- Es wurde keine Anwendungscode-Aenderung vorgenommen, weil das Arbeitspaket ein praezisiertes Folgebriefing verlangt und die gesperrten Planungsdateien nicht bearbeitet werden duerfen.
- Es wurden keine neuen Tests ergaenzt, da keine Laufzeitlogik geaendert wurde.

## Ausgefuehrte Tests

- `"C:\Users\chsue\AppData\Local\Programs\Python\Python312\python.exe" -m pytest tests/test_dashboard.py`

## Testergebnis

- `tests/test_dashboard.py`: 77 passed, 4 skipped

## Bekannte Einschraenkungen

- Die Praezisierung liegt aus Sicherheits- und Prompt-Gruenden im Implementation Report, nicht in `feedback/next_task.md` oder `feedback/backlog.md`.
- Die lokale Anzeige kann nur Daten verwenden, die bereits in der lokalen Datenbank oder isolierten Mail-Testschicht vorhanden sind. Externe Dienste wurden nicht verwendet.

## Hinweise fuer den Review-Agenten

- Pruefpunkt: Das vorgeschlagene Folgepaket fuehrt bewusst keine direkte Beleg-Transaktions-Verknuepfung ein.
- Pruefpunkt: Der Kernfall ist eine Mail mit mehreren Anhaengen, mehreren Belegen und mehreren Transaktionen in genau einem gemeinsamen Vorgang.
- Pruefpunkt: Die naechste echte Umsetzung sollte im bestehenden Vorgangsdetail starten, weil dort `vorgang.mails`, `vorgang.transaktionen` und `vorgang.belege` bereits zusammen geladen werden.
