# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Begründung

Die nachgeladenen Produktionsdateien bestätigen, dass die geforderte Statusableitung bereits zentral implementiert, nicht persistiert und in beiden Split-Antwortpfaden serialisiert ist. Der Diff ergänzt dazu einen passenden Regressionstest.

## Zusammenfassung

Akzeptiert: Der Branch sichert die bereits vorhandene zentrale Ableitung des Klassifikationsstatus für Split-Zeilen mit einem Regressionstest ab. Die Implementierung verwendet dieselben vier Pflichtfelder wie Transaktionen, berücksichtigt die optionale fachliche Beschreibung korrekt und liefert den abgeleiteten Status beim Speichern sowie Lesen von Splits.

# Review Report

## Ergebnis

**Accepted:** true

## Geprüfte Umsetzung

Der Compare enthält einen neuen Regressionstest in `tests/test_dashboard.py`. Die im Folge-Review nachgeladenen Produktionsdateien belegen, dass die fachliche Umsetzung bereits im vorhandenen Code enthalten ist:

- `classification_status(...)` in `transaction_store/classification.py` verwendet zentral die vier Pflichtfelder `transaction_type`, `top_category`, `sub_category` und `sphere`.
- Sind alle fünf Klassifikationsfelder leer, wird `unklassifiziert` geliefert.
- Sind alle vier Pflichtfelder befüllt, wird unabhängig von der fachlichen Beschreibung `vollstaendig_klassifiziert` geliefert.
- Teilweise Pflichtfeldbefüllung oder alleinige `professional_description` ergeben `unvollstaendig_klassifiziert`.
- `TransactionSplit` enthält keinen persistierten Statuswert.
- `_serialize_transaction_split(...)` leitet den Status unmittelbar aus dem gespeicherten `TransactionSplit` ab und liefert ihn kompatibel unter `klassifikationsstatus` sowie `classification_status`.
- Sowohl `transaction_splits(...)` für die Split-Leseantwort als auch `replace_transaction_splits(...)` über die anschließende Detailantwort verwenden diese Serialisierung.

## Testabdeckung

Der neue Test `test_split_responses_derive_each_classification_status` prüft für die Schreibantwort und eine nachfolgende Leseantwort:

1. vollständig leere Klassifikationsfelder: `unklassifiziert`
2. teilweise Pflichtfeldbefüllung: `unvollstaendig_klassifiziert`
3. ausschließlich fachliche Beschreibung: `unvollstaendig_klassifiziert`
4. alle vier Pflichtfelder: `vollstaendig_klassifiziert`

Zusätzlich prüft er, dass die Klassifikationsfelder und der Status der Ursprungstransaktion in der Schreibantwort unverändert bleiben. Die vorhandene Persistenzlogik ersetzt ausschließlich Split-Zeilen, behält die Betragsvalidierung bei und übernimmt weiterhin Split-ID, Reihenfolge sowie optionale `vorgangs_id`.

Laut Umsetzungsbericht wurde `tests/test_dashboard.py` mit **105 bestanden, 6 übersprungen** ausgeführt. Die übersprungenen browserabhängigen Tests sind plausibel dokumentiert und nicht blockierend.

## Fazit

Die Akzeptanzkriterien sind erfüllt. Es ist keine Schemaänderung und kein zusätzlicher persistierter Statuswert eingeführt worden; die Statuslogik bleibt zentral und konsistent zur Transaktionsklassifikation.
