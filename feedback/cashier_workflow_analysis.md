# Kassierer-Workflows und Reibungspunkte im Dashboard

## 1. Zweck und Abgrenzung

Diese Analyse beschreibt den beobachtbaren Stand des lokalen Dashboards aus
Sicht einer Person, die die laufende Vereinsverwaltung und Kasse bearbeitet.
Sie trennt Nutzerabläufe und fachliche Zustände von späteren technischen
Lösungen. Untersucht wurden die vorhandenen Dashboard-Ansichten, die lokalen
API-/Store-Abläufe und die zugehörigen Dashboard-Tests. Es wurden keine
produktiven Daten, externen Dienste oder Logins verwendet.

Für die Priorisierung wird eine einzelne Kassiererrolle mit wiederkehrender
täglicher Sichtung und mittleren Listenmengen angenommen. Konkrete Rollen- und
Mengenvorgaben fehlen. Befunde, deren Dringlichkeit von realen Mengen abhängt,
sind entsprechend gekennzeichnet.

Nicht Gegenstand sind UI-, API- oder Datenmodelländerungen. Insbesondere bleibt
der **Vorgang das zentrale fachliche Objekt**. Transaktionen, Dokumente, Mails,
To-Dos und Termine werden weiterhin über Vorgänge miteinander verbunden; die
Analyse empfiehlt keine direkten Ersatzbeziehungen.

## 2. Bewertungsmaßstab

| Priorität | Bedeutung | Kriterien |
|---|---|---|
| P0 | Blockierend | Datenverlust, unkontrollierbarer fachlicher Fehler oder Kernablauf nicht durchführbar |
| P1 | Hoch | häufiger Kernablauf führt in eine falsche Arbeitsmenge, verbirgt notwendige nächste Schritte oder erzeugt hohes Fehlbedienungsrisiko |
| P2 | Mittel | Ablauf ist möglich, benötigt aber wiederholte Suche, Kontextwechsel oder unnötige Einzelschritte |
| P3 | Niedrig | Orientierung oder Rückmeldung kann verbessert werden, ohne den Ablauf wesentlich zu behindern |

Zusätzlich wird die fachliche Wirkung als hoch, mittel oder niedrig bewertet.
Im untersuchten Stand wurde kein P0-Befund festgestellt.

## 3. Fachliches Grundbild

```text
Transaktion ─┐
Mail ────────┤
To-Do ───────┼── Vorgang (in Bearbeitung | abgeschlossen)
Dokument ────┤
Termin ──────┘
```

- Transaktionen haben zusätzlich den Klassifikationszustand
  `unklassifiziert`, `teilweise_klassifiziert` oder
  `vollstaendig_klassifiziert` sowie optionale Splits.
- To-Dos sind `offen` oder `abgeschlossen`.
- Termine sind `geplant`, `abgeschlossen` oder `abgesagt`.
- Dokumente besitzen unter anderem einen Verfügbarkeitszustand und können im
  Kontext eines Vorgangs optional einer dort verknüpften Transaktion
  zugeordnet werden. Das ist keine direkte Transaktion-Dokument-Beziehung.
- Ein Vorgang kann manuell oder regelbasiert abgeschlossen werden. Verknüpfte
  Transaktionen müssen grundsätzlich vollständig klassifiziert sein. Ein
  Rechnungsvorgang benötigt außerdem mindestens eine Transaktion und ein
  Dokument. Die vorhandene Fehlbuchungs-Ausnahme für eine leere Sphäre bleibt
  unberührt.

## 4. Strukturierte Workflow-Analyse

### W1: Vorgänge sichten, bearbeiten und abschließen

| Aspekt | Beobachteter Ablauf |
|---|---|
| Einstieg | Startübersicht über Karte/Vorschau „Nicht abgeschlossene Vorgänge“, Reiter `Vorgänge`, Link aus To-Do/Termin/Mail oder Öffnen aus einer Transaktion |
| Kernschritte | Liste suchen und optional abgeschlossene Einträge ausblenden; Vorgang öffnen; Metadaten und Verknüpfungen prüfen; Klassifikationen der Transaktionen bearbeiten; Dokument-Transaktions-Zuordnung im Vorgang prüfen; Status setzen |
| Zustände | `in_bearbeitung` oder `abgeschlossen`; Statusquelle manuell oder automatisch; zusätzlich `abschluss_moeglich` mit Blockerliste |
| Abschlussbedingung | Alle verknüpften Transaktionen vollständig klassifiziert; bei Typ Rechnung mindestens eine verknüpfte Transaktion und ein verknüpftes Dokument; danach manueller Abschluss oder passende Abschlussregel |
| Abbrüche/Fehler | Ungültige Verknüpfung, fehlende Pflichtbeziehung oder unvollständige Klassifikation verhindert Speichern/Abschluss; Löschen erfordert Bestätigung; fehlgeschlagene Requests bleiben im Dialog sichtbar |
| Reibung | Abschlussbereitschaft ist erst nach Öffnen sichtbar. Die Blockermeldung nennt bei unvollständiger Klassifikation weder betroffene Transaktionen noch konkrete fehlende Felder. In der Liste werden alle Nicht-Transaktions-Entitäten zu einer Zahl zusammengefasst. Sortierung und ein expliziter Bereitschaftsfilter fehlen. |

Eine Metadatenänderung an einem Vorgang markiert nach dem vorhandenen
Store-Ablauf verknüpfte Mails als gelesen. Dieser fachliche Seiteneffekt ist im
Bearbeitungsformular nicht angekündigt und kann den Mail-Sichtungsablauf
unerwartet abschließen.

### W2: Transaktionen sichten, klassifizieren und zuordnen

| Aspekt | Beobachteter Ablauf |
|---|---|
| Einstieg | Standardreiter `Transaktionen` mit Zeitraum der letzten drei Monate; Startkarte „Nicht zugewiesene Transaktionen“; Öffnen aus Vorgangsdetails |
| Kernschritte | Zeitraum/Suche/Sortierung setzen; Zeile öffnen; Bank- und Importdaten prüfen; fünf Klassifikationsfelder bearbeiten; bei Bedarf Splits ausgleichen; vorhandenen Vorgang zuordnen oder neuen Vorgang erstellen |
| Zustände | unklassifiziert, teilweise oder vollständig klassifiziert; Split-Summe leer, ausgeglichen oder unausgeglichen; keine, offene und/oder abgeschlossene Vorgangsverknüpfung |
| Abschlussbedingung | Fachlich passende Klassifikation gespeichert, Splits bei Nutzung betragsgleich und Zuordnung zu mindestens einem passenden Vorgang geprüft; der Vorgangsabschluss erfolgt weiterhin am Vorgang |
| Abbrüche/Fehler | Auto-Speichern kann fehlschlagen; ungültige Split-Beträge, falsche Summe oder unzulässiger Vorgangsbezug werden abgelehnt; Dialog kann ohne formellen Abschluss geschlossen werden |
| Reibung | Die Startkarte für nicht zugewiesene Transaktionen aktiviert lediglich „Transaktionen zu abgeschlossenen Vorgängen ausblenden“. Dadurch enthält die Zielliste auch Transaktionen mit offenen Vorgängen und entspricht nicht der gezählten Menge. Auto-Speichern erklärt nicht unmittelbar, dass eine unvollständige Klassifikation automatisch verknüpfte Vorgänge wieder öffnen kann. Zuordnung und Klassifikation liegen weit unten in einer umfangreichen Detailansicht. |

### W3: Dokumente/Belege prüfen und zuordnen

| Aspekt | Beobachteter Ablauf |
|---|---|
| Einstieg | Startkarte „Nicht zugewiesene Dokumente“, Vorgang erstellen/bearbeiten, Vorgangsdetail, Mailanhang bzw. Mail-Import; kein eigener Dokument-Reiter |
| Kernschritte | Katalogeintrag oder Original öffnen; Dokument einem Vorgang zuordnen; im Vorgang optional die spezifische, bereits mit demselben Vorgang verknüpfte Transaktion auswählen |
| Zustände | Datei vorhanden/nicht vorhanden; keinem/einem/mehreren Vorgängen zugeordnet; im Vorgang ohne spezifische oder mit zulässiger spezifischer Transaktion gespeichert |
| Abschlussbedingung | Dokument ist dem fachlich passenden Vorgang zugeordnet; bei Bedarf ist innerhalb dieses Vorgangs die Transaktion präzisiert; Rechnungsvorgang kann danach seinen Dokumentblocker erfüllen |
| Abbrüche/Fehler | Fehlende Datei kann nicht als Original geöffnet werden; unbekannte IDs und eine Transaktion außerhalb des Vorgangskontexts werden abgelehnt |
| Reibung | Die Startkarte öffnet nur den ungefilterten Vorgangsreiter. Die dortige Suche berücksichtigt Dokumentfelder nicht, sodass die gezählten unzugeordneten Dokumente von dort nicht gezielt bearbeitbar sind. Der zweistufige fachlich richtige Weg „Dokument → Vorgang → Transaktion im Vorgang“ wird nicht als solcher erklärt. |

### W4: Mails sichten und in Vereinsarbeit überführen

| Aspekt | Beobachteter Ablauf |
|---|---|
| Einstieg | Startkarte „Ungelesene Mails“ oder Reiter `Mails`; Laden erfolgt über die externe Integration, lokal gespeicherte Übersichten werden vorab genutzt |
| Kernschritte | Liste durchsuchen; Mail/Verlauf öffnen; Inhalt und Anhänge prüfen; taggen, zusammenfassen oder antworten; vorhandenen Vorgang suchen und zuordnen oder aus Analyse/Review einen Vorgang mit ausgewählten Entitäten erzeugen; optional To-Do/Termin erzeugen; als gelesen markieren |
| Zustände | ungelesen/gelesen, BSV/Privat, Spam-Score, Einzelmail/Verlauf, mit/ohne Zusammenfassung, mit/ohne Vorgangsverknüpfung, zum Löschen markiert |
| Abschlussbedingung | Mail ist fachlich eingeordnet, relevante Entitäten sind über den Vorgang verbunden und die Mail ist bewusst als gelesen markiert; Antworten/Löschen sind separate Abschlüsse |
| Abbrüche/Fehler | Anmeldung/Netz/Graph oder optionale Zusammenfassung kann scheitern; Import-Review kann verworfen werden; Zuordnung kann entfernt werden; Senden und Löschen haben eigene Fehlerpfade |
| Reibung | In einer Liste konkurrieren Taggen, Zusammenfassen, Gelesen-Markieren und Löschen mit dem eigentlichen Zuordnen. Vorgangssuche, Vorgangserstellung und der umfangreiche Import-Review sind drei verschiedene Zuordnungswege. Zusätzlich kann eine spätere Vorgangsbearbeitung die Mail ohne sichtbaren Hinweis als gelesen markieren. |

### W5: To-Dos erfassen, zuordnen und abschließen

| Aspekt | Beobachteter Ablauf |
|---|---|
| Einstieg | Startkarte/Vorschau „Offene To-Dos“, Reiter `To-Dos`, Mail-Zusammenfassung oder Vorgangserstellung |
| Kernschritte | Suchen/abgeschlossene ausblenden; Titel, Beschreibung, Fälligkeit und Priorität erfassen; in Mehrfachauswahl Vorgänge zuordnen; speichern; per Checkbox abschließen oder wieder öffnen; bearbeiten/löschen |
| Zustände | offen/abgeschlossen; Priorität niedrig/normal/hoch; manuelle/automatische Quelle; mit/ohne Fälligkeit und Vorgangszuordnung |
| Abschlussbedingung | Aufgabe ist erledigt und als abgeschlossen markiert; fachlich notwendige Vorgangszuordnung wurde geprüft, ist technisch aber optional |
| Abbrüche/Fehler | Ungültige Pflichtfelder oder unbekannte Vorgänge verhindern atomar das Speichern; Bearbeitung kann abgebrochen, Löschen muss bestätigt werden |
| Reibung | Mehrfachauswahl und separate Vorgangslinks nutzen eine andere Interaktion als Mail- und Transaktionszuordnung. Es gibt Suche und Offenfilter, aber keine sichtbare Sortierwahl oder Gruppierung nach Überfälligkeit/Priorität. „Vorgang erstellen“ und „Bearbeiten“ stehen gleichrangig an jeder Karte, auch wenn bereits Verknüpfungen bestehen. |

### W6: Termine erfassen, zuordnen und erledigen

| Aspekt | Beobachteter Ablauf |
|---|---|
| Einstieg | Startkarte/Vorschau „Anstehende Termine“, Karte „Nicht zugewiesene anstehende Termine“, Reiter `Termine`, Maildetail oder Vorgangserstellung |
| Kernschritte | Suchen/Statusfilter nutzen; Zeitraum, Ort und Status erfassen; Vorgänge per Mehrfachauswahl zuordnen; speichern; bearbeiten, Vorgang erzeugen oder löschen |
| Zustände | geplant/abgeschlossen/abgesagt; manuelle/automatische Quelle; zugeordnet/nicht zugeordnet; anstehend/vergangen |
| Abschlussbedingung | Termin ist abgeschlossen oder abgesagt und relevante Vorgangsbeziehungen sind geprüft |
| Abbrüche/Fehler | Ungültige Datumsfolge oder Vorgangs-ID verhindert Speichern; Bearbeitung kann abgebrochen, Löschen muss bestätigt werden |
| Reibung | Der Standardfilter „Abgeschlossene ausblenden“ zeigt nur geplante Termine und blendet damit auch abgesagte aus; seine Beschriftung beschreibt das nicht vollständig. Nur der Spezialweg aus der Startkarte zeigt den Zustand „nicht zugewiesen und anstehend“. Sortierung ist fest und nicht steuerbar. |

## 5. Doppelte oder widersprüchliche Bearbeitungsschritte

| Thema | Beobachtung | Folge |
|---|---|---|
| Vorgang zuordnen | Transaktion und Mail nutzen jeweils eigene Such-/Auswahldialoge; To-Do und Termin nutzen HTML-Mehrfachauswahl; Dokumente werden primär im Vorgangsformular gewählt | Gleiche fachliche Entscheidung hat unterschiedliche Bedien- und Rückmeldemuster |
| Vorgang erstellen | Möglich aus Transaktion, Mail, To-Do und Termin sowie global; Quellkontext wird teils vorgeschlagen, teils muss er erneut ausgewählt werden | Nutzer muss je Einstieg neu lernen, welche Beziehungen vorausgewählt sind |
| To-Do/Termin aus Vorgangsdialog | „Neu“-Aktionen schließen den Vorgangsdialog und wechseln den Reiter | Bereits erfasste, noch nicht gespeicherte Vorgangsdaten können verloren gehen |
| Abschluss | To-Do per Checkbox, Termin per Statusfeld, Vorgang per Statuseditor oder Regel, Mail per „Gelesen“ | Unterschiedliche Fachobjekte benötigen unterschiedliche Abschlüsse; problematisch ist vor allem die fehlende Erklärung ihrer gegenseitigen Seiteneffekte |
| Rückmeldung | Klassifikation speichert automatisch, Vorgang/Zuordnung/Formulare explizit, Listenaktionen teilweise sofort | Wechsel zwischen implizitem und explizitem Speichern erhöht Unsicherheit über den aktuellen Persistenzstand |

Die unterschiedlichen fachlichen Statusmodelle sollen nicht vereinheitlicht
werden. Vereinheitlicht werden sollte nur die Orientierung: Was wird geändert,
was wurde gespeichert und welche Wirkung hat dies auf den zentralen Vorgang?

## 6. Priorisierte Befunde

| ID | Prio | Wirkung | Befund | Orientierung/Rückmeldung statt Validierungsabbau |
|---|---:|---:|---|---|
| U-01 | P1 | hoch | Startkarten für nicht zugewiesene Transaktionen und Dokumente führen nicht in die jeweils gezählte, direkt bearbeitbare Menge | Kartennavigation muss denselben Filterkontext wie die Kennzahl sichtbar übergeben; keine Validierung betroffen |
| A-01 | P1 | hoch | Abschlussbereitschaft und konkrete Blocker sind in der Vorgangsliste unsichtbar; die Blockermeldung führt nicht zur betroffenen Transaktion/Feldgruppe | Vorhandene Abschlusslogik auswerten und handlungsorientiert darstellen; Regeln bleiben unverändert |
| Z-01 | P1 | hoch | Zuordnung zum Vorgang ist je Entität unterschiedlich und bietet uneinheitliche Kandidateninformationen, Suche und Bestätigung | Gemeinsames Interaktions- und Rückmeldemuster auf bestehenden Link-Endpunkten; Beziehungen bleiben unverändert |
| Z-02 | P1 | mittel | Neues To-Do/Termin aus einem ungespeicherten Vorgang schließt den Dialog und riskiert Eingabeverlust | Warnung, Zwischenerhalt oder klarer Rückweg; keine neue Persistenzarchitektur erforderlich |
| R-01 | P1 | mittel | Klassifikationsänderungen können Vorgänge wieder öffnen; Vorgangsbearbeitung kann verknüpfte Mails als gelesen markieren. Beide Wirkungen sind am Auslöser kaum sichtbar | Vor Aktion/als Erfolgsmeldung Wirkung anzeigen; bestehende fachliche Automatik nicht umgehen |
| L-01 | P2 | hoch bei großen Mengen | Vorgangsliste zeigt keine Abschlussbereitschaft, keine getrennten Entitätszahlen als Arbeitsindikatoren und keine steuerbare Sortierung | Zusätzliche vorhandene/ableitbare Anzeige- und Sortieroptionen, zunächst ohne neue Datenstruktur |
| L-02 | P2 | mittel | To-Do- und Terminlisten haben keine steuerbare Reihenfolge nach Fälligkeit, Priorität oder Aktualität | Lokal oder serverseitig stabile Sortierung anbieten; Mengen vor Entscheidung messen |
| T-01 | P2 | mittel | Terminfilter heißt „Abgeschlossene ausblenden“, zeigt aber ausschließlich geplante und verbirgt auch abgesagte Termine | Filter fachlich korrekt benennen oder Statuswahl anbieten; Statusvalidierung bleibt bestehen |
| M-01 | P2 | mittel | Mail-Liste bündelt viele gleichrangige Aktionen; die primäre Entscheidung „bearbeiten/zuordnen/erledigen“ ist nicht geführt | Aktionen nach Sichtungsphase ordnen und eindeutige Abschlussrückmeldung geben |
| D-01 | P2 | mittel | Der korrekte zweistufige Dokumentweg über den Vorgang ist nicht erklärt; unzugeordnete Dokumente sind schwer auffindbar | Kontextanzeige und gefilterter Einstieg, ausdrücklich ohne direkte Transaktion-Dokument-Beziehung |
| F-01 | P3 | niedrig | Filterzustände werden zwischen Übersichtsrouten teils gesetzt oder zurückgesetzt, aber nicht überall als aktiver Kontext erklärt | Aktive Filter als sichtbare Chips/Hinweise mit Zurücksetzen darstellen |

## 7. Abgegrenzte Folgepakete

### FP-1: Übersichtskarten mit identischem Arbeitskontext öffnen

- **Ziel:** Kartenwert, Zielmenge und sichtbarer Filter stimmen überein.
- **Umfang:** Semantik für `unassigned_transactions` und
  `unassigned_documents` ergänzen; aktive Startseitenfilter sichtbar machen;
  Routen für bereits passende Karten beibehalten.
- **Nicht enthalten:** neue Kennzahlen, neue Beziehungen, Dokumentverwaltung
  außerhalb der Vorgänge.
- **Akzeptanz:** Nach Klick entspricht die sichtbare Ergebniszahl der Karte;
  Filter ist benannt und rücksetzbar; Browser-/API-Tests decken beide Karten ab.
- **Wahrscheinliche Stellen:** `banking_dashboard/static/app.js`,
  `banking_dashboard/static/index.html`, `banking_dashboard/server.py`,
  `tests/test_dashboard.py`.
- **Leistung/Funktion:** Bestehende Zählabfragen nicht vervielfachen; Filter
  indexfreundlich halten. Alle bisherigen Karten und Reiter bleiben erhalten.

### FP-2: Einheitliches Zuordnungsmuster zum zentralen Vorgang

- **Ziel:** Transaktion, Mail, To-Do, Dokument und Termin zeigen Kandidat,
  Status, vorhandene Beziehung, Bestätigung und Ergebnis nach demselben Muster.
- **Umfang:** vorhandene Komponenten und Link-Endpunkte inventarisieren und
  schrittweise angleichen; bestehende Vorschläge bleiben ungeprüft und müssen
  bewusst bestätigt werden; ungespeicherte Eingaben beim Kontextwechsel
  schützen.
- **Nicht enthalten:** direkte Ersatzbeziehungen, neue N:M-Tabellen,
  automatische Zuordnung allein anhand eines Scores.
- **Akzeptanz:** Jede Zuordnung nennt Zielvorgang und Wirkung vor dem Speichern,
  ist abbrechbar, bestätigt Erfolg/Fehler und erhält den Ausgangskontext.
- **Wahrscheinliche Stellen:** zunächst `banking_dashboard/static/app.js`,
  `banking_dashboard/static/index.html`, `tests/test_dashboard.py`; API nur bei
  nachgewiesener Lücke.
- **Leistung/Funktion:** Kandidaten weiterhin bedarfsgesteuert laden und Suche
  abbrechbar halten; bestehende Einzel- und Mehrfachzuordnungen bleiben möglich.

### FP-3: Handlungsorientierte Abschlussblocker

- **Ziel:** Vor dem Abschluss ist sichtbar, welches Objekt und welcher Schritt
  fehlt.
- **Umfang:** vorhandene Abschlussanforderungen in Liste und Detail anzeigen;
  unvollständige Transaktions-IDs/Bezeichnungen und fehlende Felder verlinken;
  Direktabschluss beim Erstellen vor Absenden verständlich prüfen oder den
  Serverfehler feldnah darstellen.
- **Nicht enthalten:** Lockerung der Klassifikations-, Rechnungs- oder
  Fehlbuchungsregeln und keine neue Abschlussregelengine.
- **Akzeptanz:** Kassierer kann von jedem Blocker direkt zur notwendigen
  Bearbeitung gelangen; ein nicht möglicher Abschluss bleibt gesperrt; Tests
  belegen unveränderte Validierung.
- **Wahrscheinliche Stellen:** `banking_dashboard/server.py`,
  `banking_dashboard/static/app.js`, `tests/test_dashboard.py`.
- **Leistung/Funktion:** Blocker für Listen gebündelt ermitteln, kein
  Detailrequest pro Zeile. Manuelle und automatische Statusführung erhalten.

### FP-4: Konsistente Listenbedienung und Arbeitsreihenfolge

- **Ziel:** Offene, überfällige und bald fällige Arbeit kann ohne wiederholte
  Volltextsuche geordnet werden.
- **Umfang:** pro Liste fachlich passende Sortierung und klar benannte
  Statusfilter; aktive Filter sichtbar; bei Vorgängen getrennte, kompakte
  Entitätsindikatoren oder Abschlussbereitschaft.
- **Nicht enthalten:** neue Dashboard-Grundstruktur oder Entfernung vorhandener
  Such-/Zeitraumfunktionen.
- **Akzeptanz:** Sortierung ist stabil, zugänglich und zurücksetzbar; Terminfilter
  behandelt `abgesagt` eindeutig; bestehende Standardansichten bleiben
  erreichbar.
- **Wahrscheinliche Stellen:** `banking_dashboard/static/index.html`,
  `banking_dashboard/static/app.js`, optional Listenparameter in
  `banking_dashboard/server.py`, `tests/test_dashboard.py`.
- **Leistung/Funktion:** Bei kleinen Mengen darf lokal sortiert werden; vor
  serverseitiger Erweiterung typische Mengen messen. Keine unlimitierte
  zusätzliche Detailbeladung.

### FP-5: Sichtbare Seiteneffekte und Speicherstatus

- **Ziel:** Automatisches Speichern, Wiederöffnen von Vorgängen und
  Gelesen-Markieren von Mails sind am Auslöser nachvollziehbar.
- **Umfang:** Warn-/Erfolgstexte und betroffene Objektanzahl; einheitliche
  Zustände „ungespeichert“, „wird gespeichert“, „gespeichert“, „fehlgeschlagen“;
  fachliche Prüfung, ob reines Bearbeiten eines Vorgangs weiterhin Mails als
  gelesen markieren soll.
- **Nicht enthalten:** Abschalten bestehender Validierung oder stilles Ändern
  der Statusregeln.
- **Akzeptanz:** Nach jeder Änderung ist Persistenzstand und Statuswirkung
  sichtbar; Fehler lassen Eingaben korrigierbar; Tests sichern die beabsichtigte
  Mail- und Vorgangswirkung.
- **Wahrscheinliche Stellen:** `banking_dashboard/static/app.js`,
  `banking_dashboard/server.py`, `tests/test_dashboard.py`.
- **Leistung/Funktion:** Rückmeldungen nutzen vorhandene Responses; keine
  zusätzlichen Komplettladungen pro Tastendruck.

## 8. Empfohlene Reihenfolge

1. FP-1, weil falscher Zielkontext tägliche Priorisierung unmittelbar
   untergräbt und klein abgrenzbar ist.
2. FP-3, weil Abschlussblocker den Kern des zentralen Vorgangs betreffen.
3. FP-2, beginnend mit Transaktion und Mail; anschließend To-Do, Termin und
   Dokument im selben Muster.
4. FP-4 nach Erhebung typischer Listenmengen.
5. FP-5 parallel zu den jeweils berührten Abläufen oder als kleiner eigener
   Branch für die geklärte Mail-Status-Semantik.

## 9. Auswirkungen auf Leistung und Funktionsumfang

- Die Analyse fordert keinen Funktionsabbau. Suche, Filter, Vorschläge,
  manuelle Bearbeitung, Regeln, Splits und alle Entitätstypen bleiben erhalten.
- Übersichts- und Listenverbesserungen dürfen keine Detailabfrage pro Zeile
  einführen. Benötigte Zustände sollten in vorhandenen Listenabfragen gebündelt
  oder aus bereits gelieferten Feldern abgeleitet werden.
- Kandidatensuchen sollen weiter verzögert bzw. abbrechbar und nicht beim
  initialen Laden vollständig materialisiert werden.
- Vorschläge bleiben Orientierungshilfen. Ein Score ersetzt keine bewusste
  Bestätigung und keine vorhandene Validierung.
- Externe Mail- und Synchronisationsaufrufe dürfen durch reine Navigation nicht
  zusätzlich ausgelöst werden. Lokale Leer- und Fehlerzustände müssen erhalten
  bleiben.
- Vor FP-4 sind reale oder synthetische, nicht sensible Mengengerüste zu messen:
  Anzahl Vorgänge, Transaktionen je Zeitraum, Dokumente und Kandidaten je
  Zuordnungsdialog.

## 10. Nachvollzug typischer lokaler Fälle

Die Abläufe wurden anhand vorhandener isolierter Testfälle gedanklich
nachvollzogen:

1. Unvollständig klassifizierte Transaktion in einem offenen Vorgang:
   Abschluss bleibt blockiert; der nächste konkrete Feldschritt ist derzeit
   nicht direkt erreichbar.
2. Rechnung mit klassifizierter Transaktion, aber ohne Dokument:
   Dokumentblocker greift; der korrekte Weg bleibt die Zuordnung über den
   Vorgang.
3. Unzugeordnetes Dokument aus der Startkarte:
   Karte öffnet den Vorgangsreiter, liefert aber keinen Dokumentfilter oder
   bearbeitbaren Dokumentkontext.
4. Mail mit To-Do und Termin:
   mehrere Erzeugungs-/Zuordnungswege sind möglich; der Nutzer muss den
   Zusammenhang selbst über den Vorgang sichern.
5. Nicht zugewiesener anstehender Termin:
   Spezialfilter aus der Startkarte funktioniert, ist aber nicht als regulärer
   Listenfilter verfügbar.

Jeder priorisierte Befund ist damit einem Folgepaket zugeordnet. Befunde ohne
eigene technische Folgearbeit (unterschiedliche fachliche Statusmodelle) sind
bewusst als beizubehaltende Domänensemantik dokumentiert.
