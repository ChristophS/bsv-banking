# Nächstes Arbeitspaket

## Titel

Transaktions-Splits als Persistenz- und API-Grundlage anlegen

## Epic

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 1

## Ziel

Die bestehende Transaktions- und Vorgangsarchitektur um eine kleine, kontrollierte Split-Grundlage erweitern, sodass für eine einzelne Transaktion mehrere Teilbeträge mit eigener Klassifikation gespeichert, geladen und serverseitig validiert werden können.

## Relevante Dateien

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/classification.py
- banking_dashboard/server.py
- tests/test_transactions.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- transaction_store/database.py
- transaction_store/models.py
- transaction_store/classification.py
- banking_dashboard/server.py
- tests/test_transactions.py
- tests/test_dashboard.py

## Muss umgesetzt werden

- Bestehende Datenbankstruktur um Split-Persistenz für Transaktionen erweitern, ohne direkte neue Grundarchitektur außerhalb der vorhandenen Vorgangs-/Transaktionsstrukturen einzuführen.
- Ein kleines Datenmodell für Split-Zeilen definieren, das mindestens Transaktionsbezug, Reihenfolge, Betrag und die vorhandenen Klassifikationsfelder abbildet.
- Serverseitige Lade- und Speicherlogik für Splits einer einzelnen Transaktion implementieren.
- Validieren, dass die Summe aller Split-Beträge exakt dem Betrag der Ursprungstransaktion entspricht.
- Eine schlanke API für Lesen und Speichern der Split-Zeilen einer Transaktion bereitstellen.
- Den abgeleiteten Klassifikationsstatus für Split-Zeilen mit der bestehenden Klassifikationslogik kompatibel machen oder eine klar begrenzte Wiederverwendung derselben Regeln sicherstellen.
- Automatisierte Tests für Persistenz, Summenvalidierung und API-Verhalten ergänzen.

## Soll umgesetzt werden

- Split-Zeilen mit stabiler interner ID oder stabiler Reihenfolge speichern, damit spätere UI-Bearbeitung robust anschließen kann.
- Fehlerantworten der API so gestalten, dass eine spätere UI Summenfehler und Pflichtfeldprobleme gezielt anzeigen kann.
- Die Datenzugriffe so kapseln, dass spätere Erweiterungen für Rechnungs- oder Vorgangszuordnungen anschlussfähig bleiben.

## Nicht Teil dieses Arbeitspakets

- Kein Split-Editor oder sonstige Split-UI im Dashboard.
- Keine Zuordnung von Splits zu mehreren Rechnungen oder Teilrechnungen.
- Keine neuen komplexen Vorgangsverknüpfungen pro Split.
- Keine Migration bestehender Mail-, Beleg- oder Dokumentenflüsse.
- Keine automatische Abschlusslogik oder Statuslogik für komplexe Split-Folgefälle.

## Akzeptanzkriterien

- Für eine bestehende Transaktion können mehrere Split-Zeilen gespeichert und wieder geladen werden.
- Jede Split-Zeile enthält Betrag und Klassifikationsfelder in einer Form, die mit der bestehenden Fachlogik vereinbar ist.
- Der Speichervorgang wird abgelehnt, wenn die Split-Summe nicht exakt dem Transaktionsbetrag entspricht.
- Eine Transaktion ohne Splits bleibt fachlich und technisch unverändert nutzbar.
- Die neue API ist durch Tests für Erfolgs- und Fehlerfälle abgedeckt.
- Bestehende Tests für Transaktionen und Dashboard-Verhalten bleiben grün oder werden gezielt angepasst.

## Hinweise für den Umsetzungs-Agenten

- Vorgänge bleiben das zentrale fachliche Objekt; keine direkte neue Beleg- oder Rechnungsbeziehung an Splits vorbei einführen.
- Bestehende Tabellen und Services nur ergänzen, nicht grundlegend umbauen.
- Falls bereits Klassifikations-Helfer für Transaktionen existieren, diese für Split-Zeilen wiederverwenden statt parallele Logik zu erfinden.
- Die API zunächst auf einen einzelnen klaren Flow beschränken: Splits einer Transaktion lesen und vollständig ersetzen/speichern.
- Bei Geldbeträgen möglichst dieselbe interne Cent-Logik wie bei Transaktionen verwenden, um Rundungsprobleme zu vermeiden.

## Manuelle Testhinweise

- Per API eine Transaktion mit zwei Split-Zeilen anlegen, deren Summe dem Ursprungsbetrag entspricht, und die Daten erneut abrufen.
- Per API einen Speicherversuch mit falscher Split-Summe auslösen und prüfen, dass eine verständliche Fehlermeldung zurückkommt.
- Prüfen, dass eine Transaktion ohne Splits weiterhin normal in bestehenden Detailansichten und Datenabfragen erscheint.

## Offene Fragen

- Sollen Split-Zeilen bereits im ersten Schritt einen eigenen abgeleiteten Klassifikationsstatus persistent speichern oder reicht eine serverseitige Berechnung beim Laden?
- Soll das Speichern als vollständiges Ersetzen aller Splits einer Transaktion umgesetzt werden oder als feinere Einzeloperationen?
- Braucht Teil 1 bereits eine explizite Kennzeichnung, ob die Ursprungstransaktion durch Splits fachlich die führende Klassifikation verliert?
