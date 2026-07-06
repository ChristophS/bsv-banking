# Nächstes Arbeitspaket

## Titel

Transaktionsklassifikation im Mail-Vorgang-Import vor Direktabschluss ergänzen

## Ziel

Im bestehenden Mail-zu-Vorgang-Import sollen verknüpfte Transaktionen vor einem optionalen Direktabschluss klassifiziert werden können, damit der Vorgang auf Basis der aktualisierten Transaktionsdaten direkt abgeschlossen werden kann, wenn alle Regeln erfüllt sind.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Import-Dialog für Mail->Vorgang so erweitern, dass pro verknüpfter Transaktion Klassifikationsfelder erfasst und mitsamt Import gesendet werden können.
- banking_dashboard/static/index.html: falls nötig kleine Formular-Erweiterung für transaktionsbezogene Eingabefelder im bestehenden Importdialog.
- banking_dashboard/server.py: _mail_vorgang_import um optionales Lesen und Anwenden von Transaktionsklassifikationen vor dem optionalen update_vorgang_status(..., True) ergänzen.
- tests/test_dashboard.py: Tests für Mail-Vorgang-Import mit Transaktionsklassifikation und Direktabschluss ergänzen.

## Muss umgesetzt werden

- Im Import-Payload ein optionales Feld für Transaktionsklassifikationen unterstützen, z. B. je transaction_id mit transaktionstyp, oberkategorie, unterkategorie, sphaere und optional fachliche_beschreibung.
- Die Klassifikationen serverseitig vor dem optionalen Direktabschluss anwenden, damit update_vorgang_status(..., True) auf den aktualisierten Daten basiert.
- Für jede übermittelte Transaktion die bestehende Methode update_transaction_classification(...) oder äquivalente vorhandene Logik verwenden.
- Im Frontend die bereits verknüpften Transaktionen im Importdialog so darstellen, dass ihre Klassifikationsfelder bearbeitbar sind.
- Wenn Direktabschluss angefordert wird, muss die Antwort klar enthalten, ob der Abschluss gelungen ist oder wegen bestehender Blocker offen blieb.

## Soll umgesetzt werden

- Vorhandene Transaktionswerte als Vorbelegung anzeigen, damit nur fehlende Angaben ergänzt werden müssen.
- Nur tatsächlich bearbeitete Transaktionen mitsenden.
- Fehler für ungültige Klassifikationsdaten im bestehenden Importdialog sichtbar machen.

## Nicht Teil dieses Arbeitspakets

- Allgemeine Inline-Klassifikation in allen manuellen Vorgang-Erstellflows außerhalb des bestehenden Mail-Vorgang-Imports
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen
- Konzeption oder Umsetzung von Spendenbescheinigungen, Adressdatenbank oder DFBnet-Integration
- Allgemeine Dashboard-Usability-Überarbeitung

## Akzeptanzkriterien

- Beim Mail-Vorgang-Import können für verknüpfte Transaktionen Klassifikationsfelder im Import-Flow mitgegeben werden.
- Die Klassifikation wird vor dem Direktabschluss gespeichert und ist anschließend in den Transaktions- bzw. Vorgangsdetails sichtbar.
- Wenn Direktabschluss angefordert wird und danach alle Abschlussvoraussetzungen erfüllt sind, wird der neu angelegte Vorgang direkt als abgeschlossen zurückgegeben.
- Sind die Voraussetzungen trotz Import weiterhin nicht erfüllt, bleibt der Vorgang offen und die bestehende Blocker-Meldung wird geliefert.
- Bestehende Importpfade ohne Transaktionsklassifikation funktionieren unverändert weiter.

## Hinweise für den Umsetzungs-Agenten

- Der kleinste konkrete Einstieg ist der bestehende Mail-Endpunkt _mail_vorgang_import, weil dort Direktabschluss bereits existiert.
- Im Handler wird der Vorgang aktuell mit completed=False erstellt und erst danach optional per update_vorgang_status abgeschlossen; genau dazwischen sollten die Klassifikationen angewendet werden.
- update_transaction_classification(...) löst bereits apply_completion_rules(...) aus; diese bestehende Synchronisation soll genutzt werden.
- Falls mehrere Transaktionen verknüpft sind, erst alle Klassifikationen anwenden und dann einmal den Direktabschluss versuchen.
- Das Paket soll den bestehenden Flow erweitern, keinen neuen separaten API-Endpunkt dafür schaffen.

## Manuelle Testhinweise

- Mail mit verknüpfter, noch unvollständig klassifizierter Transaktion im Dashboard öffnen und Vorgang-Import starten.
- Im Importdialog fehlende Klassifikationsfelder ausfüllen und Direktabschluss aktivieren.
- Prüfen, dass der importierte Vorgang sofort abgeschlossen ist, wenn keine weiteren Blocker bestehen.
- Gegenprobe: eine Pflichtangabe leer lassen und prüfen, dass der Vorgang offen bleibt und eine nachvollziehbare Abschlussmeldung zurückkommt.
- Nach dem Import in Vorgangsdetails und Transaktionsdetails kontrollieren, dass die eingegebenen Klassifikationen gespeichert wurden.

## Offene Fragen

- Soll das UI in diesem Paket nur fehlende Klassifikationsfelder bearbeiten lassen oder alle vorhandenen Felder vollständig editierbar machen? Empfehlung: alle fünf bestehenden Felder editierbar, aber ohne neue Komfortlogik.
- Falls mehrere Transaktionen verknüpft sind: sollen sie standardmäßig eingeklappt angezeigt werden? Das ist eher eine UI-Detailentscheidung.
