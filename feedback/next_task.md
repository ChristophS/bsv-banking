# Nächstes Arbeitspaket

## Titel

Mail-Dokumentzuordnung in der Vorgangsdetailansicht bedienbar machen

## Epic

**Epic-ID:** epic-mail-document-assignment

**Epic-Titel:** Mail-Dokumente über Vorgänge unterschiedlichen Transaktionsbezügen zuordnen

**Epic-Ziel:** Mehrere Dokumente einer Mail innerhalb eines zentralen Vorgangs nachvollziehbar unterschiedlichen zugeordneten Transaktionen zuordnen, ohne die vorgangsbasierte Architektur zu umgehen.

**Teilpaket:** Teil 3

## Ziel

In der bestehenden Vorgangsdetailansicht sollen zugeordnete Dokumente einer Mail nachvollziehbar jeweils einer bereits mit dem Vorgang verknüpften Transaktion zugeordnet oder wieder auf „keine spezifische Transaktion“ gesetzt werden können.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- Vorgangsdetail-Rendering und Event-Handler in banking_dashboard/static/app.js
- Bereich oder Template-Container für Vorgangsdetails in banking_dashboard/static/index.html
- Darstellung der Zuordnungselemente und Rückmeldungen in banking_dashboard/static/styles.css
- Bestehende API- und Dashboard-Tests in tests/test_dashboard.py

## Muss umgesetzt werden

- Im Vorgangsdetail für vorhandene Belege die bestehenden Daten aus GET /api/vorgaenge/<vorgangs_id>/mail-dokumentzuordnungen laden.
- Für jeden im Vorgang vorhandenen Beleg eine verständliche Zuordnungsanzeige bereitstellen.
- Als auswählbare Ziele ausschließlich die bereits über transaktion_vorgaenge mit diesem Vorgang verbundenen Transaktionen anbieten.
- Eine leere Auswahl als explizite Option für „keine spezifische Transaktion“ unterstützen.
- Änderungen gesammelt und explizit über PUT /api/vorgaenge/<vorgangs_id>/mail-dokumentzuordnungen mit dem Schema {"zuordnungen":[{"beleg_id":"...","transaktions_id":"...|null"}]} speichern.
- Nach erfolgreichem Speichern Vorgangsdetails und Zuordnungsanzeige konsistent aktualisieren sowie verständliche Fehler anzeigen.
- Automatisierte Tests für das Laden und Speichern der Zuordnung sowie für eine ungültige Zuordnung ergänzen, ohne Mail-, Browser- oder externe Dienste aufzurufen.

## Soll umgesetzt werden

- Belege mit Mailherkunft oder erkennbarer Mail-Anhangsreferenz in der UI nachvollziehbar kennzeichnen, sofern diese Information bereits in den geladenen Daten verfügbar ist.
- Bei Vorgängen ohne verknüpfte Transaktionen einen klaren Leerzustand anzeigen und keine ungültigen Auswahlwerte senden.
- Unveränderte Zuordnungen nicht unnötig als lokale Änderungen markieren.

## Nicht Teil dieses Arbeitspakets

- Keine neue direkte Beziehung zwischen Transaktionen und Belegen einführen.
- Keine Änderungen an Tabellen, Migrationen oder der bestehenden vorgangsbasierten Verknüpfungsarchitektur vornehmen.
- Keine automatische Zuordnung von Belegen zu Transaktionen entwickeln.
- Keine Änderungen an Microsoft Graph, Mailabruf, Mailimport oder produktiven externen Aktionen vornehmen.
- Keine komplexeren Rechnungs-, Teilrechnungs- oder Transaktions-Split-Flows umsetzen.

## Akzeptanzkriterien

- Ein Vorgang mit mehreren verknüpften Transaktionen und mehreren Belegen zeigt für jeden Beleg die aktuelle spezifische Transaktionszuordnung oder den unzugeordneten Zustand.
- Für einen Beleg kann genau eine der zum Vorgang gehörenden Transaktionen oder „keine spezifische Transaktion“ gewählt werden.
- Nach dem Speichern liefert ein erneutes Laden dieselben Zuordnungen und die UI stellt sie korrekt dar.
- Die UI bietet keine Transaktion an, die nicht mit dem aktuellen Vorgang verknüpft ist.
- API-Fehler werden sichtbar behandelt, ohne den lokal angezeigten bestätigten Stand als erfolgreich gespeichert auszugeben.
- Die bestehenden Dashboard-Tests bleiben grün; neue Tests verwenden ausschließlich lokale Testdaten und keine externen Dienste.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandenen Endpunkte und DashboardDataStore-Methoden mail_document_assignments und replace_mail_document_assignments verwenden; keine parallele API oder Persistenzlogik schaffen.
- Die fachliche Zuordnung bleibt vorgang_belege.vorgangsbezug_id, die auf den bestehenden transaktion_vorgaenge.bezugs_id verweist.
- Beim Speichern alle sichtbaren Belegzuordnungen als vollständige Liste senden, damit die vorhandene Replace-Semantik genutzt wird.
- Transaktionslabels sollten mindestens Datum, Zahlungsbeteiligten oder Verwendungszweck und Betrag enthalten, damit gleichartige Transaktionen unterscheidbar bleiben.
- Serveränderungen nur dann vornehmen, wenn ein klarer UI-seitiger Datenbedarf mit den bereits vorhandenen API-Antworten nicht abgedeckt werden kann.

## Manuelle Testhinweise

- Lokale Testdaten mit einem Vorgang, mindestens zwei verknüpften Transaktionen und mindestens zwei Belegen anlegen.
- Je Beleg unterschiedliche Transaktionen auswählen, speichern, Vorgang neu laden und die Persistenz prüfen.
- Eine Zuordnung wieder auf „keine spezifische Transaktion“ setzen, speichern und nach Neuladen prüfen.
- Einen Vorgang ohne verknüpfte Transaktionen öffnen und prüfen, dass kein unzulässiges Ziel auswählbar ist.
- Keine Mail-, Graph-, Banking- oder DFBnet-Aktion für den Test ausführen.

## Offene Fragen

- Keine Angaben
