# Nächstes Arbeitspaket

## Titel

Klassifikationsstatus für einzelne Split-Zeilen über die Split-API ableiten

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 3.1

## Ziel

Gespeicherte Split-Zeilen sollen ihren fachlichen Klassifikationsstatus nach denselben Pflichtfeldregeln wie Transaktionen konsistent zurückliefern, ohne die Klassifikation der Ursprungstransaktion oder bestehende Vorgangsverknüpfungen zu verändern.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/classification.py
- transaction_store/models.py
- banking_dashboard/server.py
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- TransactionSplit-Modell und die Serialisierung von Split-Zeilen
- zentrale Klassifikationsstatuslogik in transaction_store/classification.py
- bestehende API-Endpunkte zum Lesen und Speichern von Transaktions-Splits
- Unit- und API-Tests für Split-Antworten und Validierung

## Muss umgesetzt werden

- Für jede Split-Zeile einen abgeleiteten Klassifikationsstatus bereitstellen: unklassifiziert bei vollständig leeren Klassifikationsfeldern, vollständig_klassifiziert bei allen vier Pflichtfeldern und unvollstaendig_klassifiziert in allen übrigen Fällen.
- Dabei dieselben Pflichtfelder wie bei Transaktionen verwenden: Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre; die fachliche Beschreibung bleibt optional, verhindert bei alleiniger Befüllung aber den Status unklassifiziert.
- Den Status zentral ableiten und nicht als unabhängigen, manuell editierbaren Persistenzwert in transaction_splits speichern.
- Die bestehenden Split-Lese- und Schreibantworten so erweitern, dass Clients den abgeleiteten Status je gespeicherter Split-Zeile erhalten.
- Bestehende Betragsprüfung, Sortierung, Split-IDs und optionale vorgangs_id unverändert beibehalten.
- Tests für leere, teilweise und vollständig klassifizierte Splits sowie für eine ausschließlich gefüllte fachliche Beschreibung ergänzen.

## Soll umgesetzt werden

- Bestehende Klassifikationsstatus-Helfer wiederverwenden oder gezielt verallgemeinern, statt eine zweite abweichende Statuslogik einzuführen.
- API-Fehlerantworten und vorhandene Serialisierungsformate kompatibel halten.
- Testen, dass das Lesen und Speichern von Splits weder Klassifikationsfelder noch Status der Ursprungstransaktion verändert.

## Nicht Teil dieses Arbeitspakets

- Vorschlagslisten, Datalists oder abhängige Auswahlfelder im Split-Editor.
- Änderungen am sichtbaren Split-Editor oder zusätzliche UI-Flows.
- Automatische Klassifikationsregeln für Split-Zeilen.
- Automatisches Öffnen oder Abschließen von Vorgängen aufgrund von Split-Status.
- Zuordnungen mehrerer Rechnungen, Teilrechnungen oder Belege zu einzelnen Splits.
- Grundlegende Änderungen an Tabellen, bestehenden Transaktions-Vorgangs-Verknüpfungen oder der Vorgangsarchitektur.

## Akzeptanzkriterien

- Eine per API gelesene Split-Zeile enthält einen nachvollziehbar abgeleiteten Klassifikationsstatus.
- Ein Split ohne alle fünf Klassifikationsfelder ist unklassifiziert.
- Ein Split mit allen vier Pflichtfeldern ist vollständig_klassifiziert, unabhängig davon, ob eine fachliche Beschreibung gesetzt ist.
- Ein Split mit nur einem Teil der Pflichtfelder oder nur einer fachlichen Beschreibung ist unvollstaendig_klassifiziert.
- Der Status wird nach einem Speichern geänderter Split-Klassifikationsfelder sofort korrekt zurückgegeben.
- Die Summe der Split-Beträge muss weiterhin exakt dem Betrag der Ursprungstransaktion entsprechen.
- Die bestehenden Tests bleiben grün; neue Tests benötigen keine Bank-, Browser- oder produktiven Laufzeitdaten.

## Hinweise für den Umsetzungs-Agenten

- transaction_splits enthält bereits die fünf erforderlichen Klassifikationsfelder; hierfür ist keine neue fachliche Entität oder direkte Beleg-Transaktions-Beziehung nötig.
- Die Statusableitung muss vom gespeicherten Split-Inhalt ausgehen und darf keinen Status in der Ursprungstransaktion überschreiben.
- Vorgänge bleiben das zentrale Objekt: Die vorhandene optionale vorgangs_id eines Splits wird in diesem Paket nur erhalten, nicht fachlich neu ausgewertet.
- Die Umsetzung muss rein lokal und ohne externe Dienste erfolgen.

## Manuelle Testhinweise

- Eine vorhandene Transaktion mit mindestens zwei betragsgenau passenden Splits öffnen oder über die bestehende API anlegen.
- Einen Split leer lassen, einen nur teilweise klassifizieren und einen vollständig klassifizieren.
- Split-Liste erneut laden und die drei erwarteten Statuswerte prüfen.
- Eine fachliche Beschreibung bei einem ansonsten leeren Split setzen und prüfen, dass dieser nicht als unklassifiziert erscheint.
- Prüfen, dass Betrag, Reihenfolge und Ursprungstransaktion unverändert bleiben.

## Offene Fragen

- Soll ein späterer Vorgangsstatus aus Split-Klassifikationen nur ergänzend oder statt der derzeitigen transaktionsbasierten Vollständigkeitsprüfung abgeleitet werden? Dies bleibt für ein separates Folgepaket offen.
- Soll die API den Status ausschließlich unter dem bestehenden deutschen Feldnamen klassifikationsstatus oder zusätzlich unter einem Split-spezifischen technischen Namen liefern? An vorhandenen API-Konventionen ausrichten.
