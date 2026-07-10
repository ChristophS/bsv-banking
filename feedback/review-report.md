# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Der geladene Kontext reicht zusammen mit dem GitHub-Diff für eine fachliche Entscheidung aus; die Branch-Lage ist sauber und die Split-Grundlage ist im aktuellen Stand technisch ausreichend umgesetzt.

## Zusammenfassung

Die Persistenz- und API-Grundlage für Transaktions-Splits ist umgesetzt: Datenmodell, Tabelle/Migration, Lade-/Ersetzungslogik, Summenvalidierung, API-Endpunkte und Tests sind vorhanden. Die im Diff sichtbare Nachbesserung zur Duplikatvalidierung ist fachlich sinnvoll; es verbleiben nur nicht-blockierende Verbesserungsmöglichkeiten.

# Review Report

## Ergebnis

**Accepted:** true

## Geprüfter Umfang

Geprüft wurden das Arbeitspaket „Transaktions-Splits als Persistenz- und API-Grundlage anlegen“, der GitHub-Compare-Diff sowie die nachgeladenen relevanten Dateien für Persistenz, Datenmodell, Klassifikationslogik, Server/API und Tests.

## Fachliche Bewertung

Die Umsetzung erfüllt die wesentlichen Anforderungen des Arbeitspakets:

- Es gibt ein Datenmodell `TransactionSplit` mit Transaktionsbezug, stabiler ID bzw. Reihenfolge, Cent-Betrag und den bestehenden Klassifikationsfeldern.
- Die Datenbank enthält eine gekapselte Split-Persistenz über `transaction_splits` inklusive Foreign Keys zu Transaktionen und optional zu Vorgängen.
- Splits einer Transaktion können geladen und vollständig ersetzt gespeichert werden.
- Beim Speichern wird die Summe der Split-Beträge gegen den Ursprungsbetrag der Transaktion validiert.
- Transaktionen ohne Splits bleiben über die Detail- und Listenflüsse weiterhin nutzbar; leere Split-Listen werden unterstützt.
- Die API unter `/api/transactions/{id}/splits` bietet Lesen und vollständiges Ersetzen der Split-Zeilen.
- Die bestehende Klassifikationslogik wird für Split-Zeilen wiederverwendet; Einzelstatus und aggregierter Split-Status werden bereitgestellt.
- Es gibt automatisierte Tests für Schema/Migration, Persistenz, Atomarität, Summenvalidierung, Klassifikationsstatus und API-Erfolgs-/Fehlerfälle.

Die im GitHub-Diff sichtbare Nachbesserung ergänzt eine sinnvolle Vorabvalidierung doppelter `split_id`s innerhalb eines Speicherpayloads und sichert diese mit Store- und API-Tests ab. Dadurch werden generische Datenbankfehler und Teilpersistenzrisiken vermieden.

## Technische Bewertung

Die Lösung bleibt innerhalb der bestehenden Transaktions-/Vorgangsarchitektur. Es werden keine externen Dienste, produktiven Daten oder geschützten Dateien berührt. Die Branch-Lage ist sauber (`ahead`, `behind_by=0`).

Die Verwendung von Cent-Beträgen und vollständigem Ersetzen der Split-Liste passt zum Arbeitspaket. Die Savepoint-Logik schützt bestehende Splits bei Validierungs- oder Insert-Fehlern vor partiellen Änderungen.

## Nicht-blockierende Hinweise

- Die API-Fehlerantworten sind aktuell im Kern `{ "error": "..." }`. Das ist für das Arbeitspaket ausreichend, könnte aber für eine spätere UI um strukturierte Fehlercodes und Feldinformationen ergänzt werden.
- Die Betrag-Validierung akzeptiert technisch Werte, die von `int(...)` konvertierbar sind. Für eine robuste API wäre es besser, JSON-Floats explizit abzulehnen und echte Ganzzahlen zu verlangen.
- Ungültige `vorgangs_id`-Referenzen in Split-Zeilen könnten vorab geprüft und als gezielte 400/404-Antwort statt als generischer Datenbankfehler behandelt werden.
- Der nachgeladene Kontext wirkt bei den im Diff ergänzten Duplikat-Prüfungen teilweise nicht vollständig auf dem gleichen Patch-Stand wie der GitHub-Diff. Da der GitHub-Diff maßgeblich für die geänderten Stellen ist und die übrige Split-Implementierung im Kontext nachvollziehbar ist, ist das hier nicht blockierend.

## Entscheidung

Keine blockierenden Probleme gefunden. Die Umsetzung kann akzeptiert werden.
