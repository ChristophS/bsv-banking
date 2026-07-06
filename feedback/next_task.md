# Nächstes Arbeitspaket

## Titel

Transaktionsklassifikation im Mail-Vorgang-Import vor Direktabschluss bearbeitbar machen

## Ziel

Im bestehenden manuellen Mail-Vorgang-Import sollen verknuepfte Transaktionen vor dem finalen Import sichtbar und bearbeitbar sein, damit Klassifikationsdaten im selben Flow vervollstaendigt und anschliessend ueber den bestehenden Import- und Direktabschluss-Mechanismus verarbeitet werden koennen.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/server.py
- tests/test_dashboard.py
- transaction_store/database.py
- transaction_store/models.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: Mail-Import-Dialog um Anzeige/Bearbeitung der verknuepften transaction_ids und das Vorab-Speichern geaenderter Klassifikationen erweitern.
- banking_dashboard/static/index.html: Falls noetig UI-Container fuer Inline-Transaktionsklassifikation im Mail-Import ergaenzen.
- banking_dashboard/server.py: Nur gezielt an bestehenden Mail-Import- und Klassifikationsendpunkten ansetzen, damit Vorab-Speichern und anschliessender Import/Direktabschluss sauber zusammenspielen.
- tests/test_dashboard.py: Verhalten des Mail-Imports mit vorab klassifizierten Transaktionen und direct_completion absichern.

## Muss umgesetzt werden

- Im Mail-Vorgang-Import-Flow fuer bereits verlinkte Transaktionen die Klassifikationsfelder sichtbar machen: Transaktionstyp, Oberkategorie, Unterkategorie, Sphaere und optionale fachliche Beschreibung.
- Die Felder muessen vor dem eigentlichen POST /api/mail/<id>/vorgang-import bearbeitbar sein.
- Geaenderte Klassifikationsdaten muessen vor dem Import ueber die bestehende PATCH-API fuer Transaktionen gespeichert werden.
- Wenn der Nutzer Direktabschluss anfordert, darf der Import erst nach erfolgreicher Vorab-Speicherung starten und nur an echten Abschlussblockern scheitern.
- Fehler bei der Klassifikationsspeicherung muessen im UI sichtbar sein und den finalen Import/Direktabschluss verhindern.
- Vorhandene Vorschlags- und Auswahllogik fuer Klassifikationsoptionen im Frontend wiederverwenden.

## Soll umgesetzt werden

- Nach erfolgreicher Speicherung die betroffenen Transaktionsdaten im UI aktualisieren, damit der Vollstaendigkeitsstatus direkt sichtbar ist.
- Pflichtfelder je verknuepfter Transaktion im Import-Dialog so markieren, dass Direktabschluss-Blocker erkennbar werden.
- Die bestehende direct_completion-Rueckmeldung im Mail-Import-Ergebnis weiterhin klar anzeigen.

## Nicht Teil dieses Arbeitspakets

- Inline-Klassifikation fuer manuell neu erstellte Vorgänge ausserhalb des Mail-Import-Flows.
- Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen.
- Neue automatische Vorschlags- oder KI-Klassifikation fuer Transaktionen.
- Grundsaetzlicher Redesign des Mail- oder Vorgangsbereichs.

## Akzeptanzkriterien

- Wenn eine Mail im Import-Flow mit mindestens einer bestehenden transaction_id verknuepft wird, koennen deren Klassifikationsfelder vor dem Import im selben UI bearbeitet werden.
- Aenderungen an den Klassifikationsfeldern werden ueber die bestehende Transaktions-API gespeichert und sind danach in den Transaktionsdaten vorhanden.
- Ein Direktabschluss im Mail-Import klappt, wenn die verknuepften Transaktionen nach der Inline-Bearbeitung vollstaendig klassifiziert sind und keine weiteren bestehenden Abschlussblocker greifen.
- Schlaegt die Speicherung fehl oder fehlen Pflichtfelder, wird der Vorgang nicht stillschweigend abgeschlossen importiert; stattdessen erscheint eine nachvollziehbare Fehlermeldung oder Blockierung.
- Bestehende Importfunktionen fuer Dokumente, To-Dos, Termine und Verknuepfungen bleiben funktionsfaehig.

## Hinweise für den Umsetzungs-Agenten

- Bevorzugt die bestehende Sequenz: Transaktionsklassifikation speichern -> danach Mail-Vorgang-Import ausloesen, damit der Import-Endpunkt fachlich schlank bleibt.
- Die Rueckgabe von update_transaction_classification() enthaelt bereits transaction und vorgaenge; das kann fuer UI-Refresh und Validierung genutzt werden.
- Die Importlogik in _mail_vorgang_import() setzt completed zunaechst bewusst auf false und versucht danach update_vorgang_status(..., true); dieses Verhalten sollte erhalten bleiben.
- Achte darauf, dass verknuepfte Transaktionen global aktualisiert werden und nicht nur bezogen auf den neuen Vorgang.
- Falls app.js bereits Hilfsfunktionen fuer Klassifikationsoptionen oder abhängige Selects hat, diese fuer den Mail-Import wiederverwenden statt duplizieren.

## Manuelle Testhinweise

- Im Dashboard eine Mail oeffnen/importieren, die auf eine bestehende Transaktion verlinkt werden soll; im Import-Dialog Pflichtfelder der Transaktion ausfuellen und Direktabschluss aktivieren. Erwartung: Vorgang wird erstellt und abgeschlossen, falls sonst keine Blocker bestehen.
- Gleichen Test mit absichtlich fehlender Oberkategorie oder Sphaere durchspielen. Erwartung: Direktabschluss wird abgelehnt oder blockiert und die Ursache ist sichtbar.
- Testen, dass Dokumente, To-Dos und Termine aus demselben Mail-Import weiterhin normal importiert werden.
- Nach dem Import die betroffene Transaktion im Transaktions- oder Vorgangsdetail oeffnen und pruefen, dass die geaenderten Klassifikationswerte persistiert wurden.

## Offene Fragen

- Soll die Inline-Bearbeitung nur fuer bereits ueber links.transaction_ids verknuepfte Transaktionen gelten, oder auch fuer waehrend des Dialogs neu hinzugefuegte Transaktionslinks, falls das UI dies bereits unterstuetzt?
- Falls mehrere verknuepfte Transaktionen vorhanden sind: Reicht eine kompakte Editorliste, oder gibt es bereits ein bestehendes Detail-Widget in app.js, das dafuer wiederverwendet werden sollte?
