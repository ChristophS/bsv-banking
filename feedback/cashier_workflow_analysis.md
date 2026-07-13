# Analyse der Kassierer-Workflows im Dashboard

## Zweck und Rahmen

Diese Analyse beschreibt den vorhandenen Arbeitsweg vom Eingang eines offenen Elements bis zum Abschluss eines Vorgangs. Grundlage sind die statischen Dashboard-Ansichten, ihre lokale API und die bestehenden Dashboard-Tests. Es wurden keine produktiven Daten, externen Dienste oder Logins verwendet.

Als primärer Nutzungskontext wird ein Kassierer mit grundlegender Kenntnis der Vereinsbuchhaltung angenommen, der regelmäßig, aber nicht ausschließlich mit dem Tool arbeitet. Deshalb müssen Priorität, Status und nächster Schritt ohne Kenntnis interner IDs oder technischer Verknüpfungstabellen verständlich sein. Die fachliche Reihenfolge mehrerer gleichzeitig offener Kategorien ist im Repository nicht verbindlich definiert; die unten vorgeschlagene Reihenfolge ist daher eine begründete Anforderung, keine Änderung bestehender Fachlogik.

## Bestehendes fachliches Modell

Der **Vorgang bleibt das zentrale fachliche Objekt**. Transaktionen, Mails, To-Dos, Dokumente/Belege und Termine werden über die vorhandenen Vorgangsverknüpfungen gebündelt. Eine direkte Beziehung zwischen zwei Nebenelementen darf diese Bündelung nicht ersetzen. Die vorhandene spezifische Zuordnung eines Dokuments zu einer Transaktion ist nur innerhalb eines bereits gemeinsam verknüpften Vorgangs zulässig.

Relevante Zustände:

- Vorgang: `offen`, `in_bearbeitung`, `abgeschlossen`; zusätzlich ist erkennbar, ob der Zustand manuell gesetzt oder automatisch ermittelt wurde.
- Transaktion: `unklassifiziert`, `unvollstaendig_klassifiziert`, `vollstaendig_klassifiziert`; vollständig sind mindestens Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre.
- To-Do: `offen` oder `abgeschlossen`, ergänzt um Priorität und Fälligkeit.
- Termin: `geplant`, `abgeschlossen` oder `abgesagt`; die Übersicht zählt nur geplante, anstehende Termine.
- Mail: insbesondere gelesen/ungelesen, Spam-Bewertung und Vorgangszuordnung.
- Dokument/Beleg: vorhanden/nicht vorhanden sowie einem Vorgang zugeordnet/nicht zugeordnet; bei Rechnungen ist mindestens ein Dokument eine Abschlussbedingung.

Architekturbelege: `banking_dashboard/server.py` (Übersicht in `overview_counts`, Abschlussprüfung in `_vorgang_completion_requirements_from_db`) und `banking_dashboard/static/app.js` (Vorgangsarbeitsraum in `renderVorgangWorkspace`).

## Arbeitsablaufmodell

### 1. Sichten und priorisieren

**Eingänge:** Die Startübersicht zählt nicht abgeschlossene Vorgänge, ungelesene Mails, nicht zugewiesene Transaktionen, offene To-Dos, nicht zugewiesene Dokumente, anstehende Termine und nicht zugewiesene anstehende Termine. Zusätzlich zeigt sie Vorschauen für offene Vorgänge, offene To-Dos und anstehende Termine.

**Vorhandener Ablauf:** Der Kassierer öffnet eine Kennzahl oder Vorschau, wechselt damit in eine Entitätsansicht und grenzt die Liste über Suche beziehungsweise vorhandene Filter ein. Offene Vorgänge werden in der Vorgangsliste vor abgeschlossenen priorisiert.

**Erwartetes Ergebnis:** Ein fachlich relevantes Element ist ausgewählt und entweder einem bestehenden Vorgang zugeordnet oder Ausgangspunkt für einen neuen Vorgang.

### 2. Klassifizieren

**Eingang:** Eine ausgewählte Transaktion im Transaktionsdialog oder als verknüpfte Transaktion im Vorgangsarbeitsraum.

**Vorhandener Ablauf:** Der Kassierer ergänzt Transaktionstyp, Oberkategorie, Unterkategorie, Sphäre und optional die fachliche Beschreibung. Änderungen werden mit kurzer Verzögerung automatisch gespeichert. Alternativ können Klassifikationsregeln unklassifizierte Transaktionen bearbeiten. Splits besitzen dieselben fachlichen Klassifikationsfelder und müssen zusammen den Originalbetrag ergeben.

**Erwartetes Ergebnis:** Die Transaktion beziehungsweise alle Splits sind vollständig klassifiziert. Die Änderung kann automatisch verknüpfte Vorgangsstatus und Abschlussregeln neu bewerten.

### 3. Zuordnen und bündeln

**Eingänge:** Eine Transaktion, Mail, ein To-Do, Termin oder Dokument ohne Vorgang; alternativ ein bereits geöffneter Vorgang.

**Vorhandene Wege:**

- Transaktion: Detail öffnen, bestehenden Vorgang suchen und per Einzelauswahl zuordnen oder einen neuen Vorgang erstellen.
- Mail: im Maildetail vorhandenen Vorgang suchen/zuordnen; alternativ einen KI-Vorschlag prüfen und Vorgang, Dokumente, To-Dos, Termine sowie Transaktionen gemeinsam importieren.
- To-Do/Termin: im jeweiligen Formular einen oder mehrere Vorgänge auswählen oder aus dem Element einen neuen Vorgang erstellen.
- Dokument: über einen Vorgang verknüpfen; im Vorgangsarbeitsraum kann ein verknüpftes Dokument zusätzlich einer dort verknüpften Transaktion zugeordnet werden.
- Vorgang: im Vorgangsarbeitsraum über getrennte Vorschlagsbereiche Transaktionen, Mails, To-Dos, Dokumente und Termine hinzufügen oder entfernen.

**Erwartetes Ergebnis:** Alle fachlich zusammengehörigen Elemente sind über vorhandene Vorgangsverknüpfungen auffindbar. Originaldaten bleiben unverändert.

### 4. Prüfen und abschließen

**Eingang:** Ein offener oder in Bearbeitung befindlicher Vorgang.

**Vorhandener Ablauf:** Im Vorgangsarbeitsraum prüft der Kassierer Metadaten und alle zugeordneten Entitäten. Der Bereich „Bearbeitungsstatus“ zeigt, ob Abschluss möglich ist, und listet andernfalls textuelle Blocker. Allgemein müssen verknüpfte Transaktionen vollständig klassifiziert sein; typabhängige Anforderungen kommen hinzu, beispielsweise Transaktion und Dokument bei einem Rechnungsvorgang. Erst dann wird die Abschlussaktion aktiv. Ein abgeschlossener Vorgang kann wieder geöffnet werden. Eine später unvollständige Transaktion kann automatisch verknüpfte Vorgänge wieder öffnen; manuell gesetzte Zustände bleiben gemäß bestehender Logik gesondert behandelt.

**Erwartetes Ergebnis:** Der Vorgang ist nachvollziehbar abgeschlossen; die Originalelemente und Verknüpfungen bleiben erhalten. Zugeordnete Mails werden durch vorhandene Abschlussfolgen als gelesen markiert.

## Vergleich der Einstiege und Wechsel

| Bereich | Typischer Einstieg | Eingrenzung | Wechsel zum Vorgang | Status/Rückmeldung |
|---|---|---|---|---|
| Vorgänge | Übersichtskarte, Vorschau oder Tab | Suche, abgeschlossene ausblenden | direkter Arbeitsraum | Status, manuell/automatisch, Abschlussblocker, Speicherstatus |
| Transaktionen | Übersichtskarte oder Tab | Suche, Zeitraum, Sortierung, Vorgänge abgeschlossen ausblenden | Detail: bestehenden Vorgang zuordnen/öffnen oder neuen anlegen | Klassifikationsbadge und Autosave; Vorgangszelle zeigt nur Anzahl/Abschlussanteil |
| Mails | Übersichtskarte oder Tab | Suche; im Zuordnungsbereich abgeschlossene Vorgänge ausblenden | Maildetail: zuordnen/entfernen/öffnen oder Importprüfung | Lade-, Such- und Speicherstatus; komplexer Import hat eigenen Prüfablauf |
| To-Dos | Übersichtsvorschau/-karte oder Tab | Suche, abgeschlossene ausblenden | Vorgangslink öffnen, im Formular auswählen oder neuen Vorgang anlegen | offen/abgeschlossen, Priorität, Fälligkeit; Fehler überwiegend global |
| Termine | Übersichtsvorschau/-karte oder Tab | Suche, abgeschlossene ausblenden, Sonderfilter „nicht zugewiesen und anstehend“ | Vorgangslink öffnen, im Formular auswählen oder neuen Vorgang anlegen | geplant/abgeschlossen/abgesagt und Formularstatus |
| Dokumente | Übersichtskarte oder Vorgangsarbeitsraum | keine eigene sichtbare Arbeitsliste im Hauptdashboard | Karte wechselt lediglich zur ungefilterten Vorgangsliste; konkrete Zuordnung über Vorgang | vorhanden/nicht vorhanden erst im Kontext; keine direkte Restmenge im Ziel |

## Priorisierte Reibungspunkte

Priorität kombiniert Nutzerwirkung und Dringlichkeit: **P0** blockiert oder gefährdet den korrekten Abschluss, **P1** verursacht regelmäßig Mehrarbeit oder Fehlzuordnungen, **P2** erschwert Orientierung ohne den Kernablauf zu verhindern.

| ID | Prio | Ablauf | Entität | Beobachtung und Nutzerwirkung | Begründung |
|---|---|---|---|---|---|
| R1 | P0 | Prüfen/Abschließen | Vorgang, Transaktion, Dokument | Abschlussblocker sind Text in einer Liste, aber nicht mit dem betroffenen Element oder fehlenden Feld verknüpft. Der Kassierer muss im langen Arbeitsraum selbst suchen. | Verhindert den Abschluss und erhöht das Risiko, am falschen Element Änderungen vorzunehmen. |
| R2 | P0 | Klassifizieren/Abschließen | Transaktion, Vorgang | Der Klassifikationsstatus ist im Transaktionsdetail sichtbar, nicht jedoch als einheitlich priorisierbares Merkmal in Übersicht und Transaktionsliste. Die Karte „nicht zugewiesen“ erfasst unklassifizierte, bereits zugewiesene Transaktionen nicht. | Abschlussrelevante Arbeit kann in vorhandenen Vorgängen unbemerkt liegen bleiben. |
| R3 | P1 | Sichten | alle offenen Entitäten | Die sieben Übersichtskarten sind reine Kategorien mit Zählwerten. Es fehlen gemeinsame Dringlichkeit, Fälligkeit, Blockerbezug und ein erklärter nächster Schritt. Vorschauen existieren nur für drei Kategorien. | Der Kassierer muss mehrere Tabs prüfen und selbst entscheiden, was zuerst zu bearbeiten ist. |
| R4 | P1 | Sichten | Dokument | „Nicht zugewiesene Dokumente“ führt zur ungefilterten Vorgangsliste, nicht zu den gezählten Dokumenten oder einem aktiven Filter. | Die Kennzahl ist nicht direkt abarbeitbar; Kontext und Restmenge gehen beim Wechsel verloren. |
| R5 | P1 | Zuordnen | Transaktion, Mail, To-Do, Termin, Dokument | Such-, Auswahl- und Bestätigungsmuster unterscheiden sich: Radioauswahl im Transaktions-/Maildetail, Mehrfachauswahl im Formular, Checkbox-Vorschläge im Vorgang und dokumentbezogene Auswahl erst im Vorgang. | Wiederkehrende Arbeit erfordert Umlernen; Auswahl- und Fehlzuordnungsrisiko steigen. |
| R6 | P1 | Zuordnen | Vorgang und alle Nebenelemente | Kandidaten zeigen je nach Einstieg unterschiedliche Metadaten. Titel, Typ, Status, Datum, Betrag, Zuordnungsgrund und bereits verknüpfte Entitäten sind nicht überall vergleichbar. | Ähnliche Vorgänge sind schwer sicher zu unterscheiden, insbesondere ohne Kenntnis der ID. |
| R7 | P1 | Klassifizieren | Transaktion | Autosave meldet „Wird gespeichert/Gespeichert/fehlgeschlagen“, aber ein Wechsel oder Schließen während verzögertem beziehungsweise laufendem Speichern ist nicht als ungesicherter Zustand geführt. | Unklarheit, ob die letzte Eingabe bereits persistent und für den Abschluss wirksam ist. |
| R8 | P1 | Prüfen/Abschließen | Vorgang | Automatische Folgeeffekte – etwa Wiederöffnung durch unvollständige Klassifikation oder Mail als gelesen – sind fachlich getestet, werden im Arbeitsablauf aber nicht als Änderungshistorie beziehungsweise konkrete Ursache erklärt. | Unerwartete Statuswechsel wirken wie Fehler und erzeugen Nachprüfung. |
| R9 | P2 | Sichten | Transaktion | „Transaktionen zu abgeschlossenen Vorgängen ausblenden“ lässt unzugewiesene und teilweise mit offenen Vorgängen verknüpfte Transaktionen sichtbar; die Formulierung erklärt die Mehrfachverknüpfungssemantik nicht. | Filterergebnis kann als unzuverlässig missverstanden werden. |
| R10 | P2 | Zuordnen | To-Do, Termin | Die Formulare laden die vollständige Vorgangsauswahl; Suche und Begründung von Vorschlägen fehlen dort. | Mit wachsendem Bestand wird Auswahl langsam und fehleranfällig. |
| R11 | P2 | Prüfen | Vorgang | Der Arbeitsraum zeigt Status, Bearbeitung, Regeln, Spendenbescheinigung, Dokument-Transaktionszuordnung, Entitäten und komplette Transaktionsdetails in einem langen Dialog. | Der aktuelle Prüfschritt und die noch offene Arbeit verlieren visuelle Priorität. |
| R12 | P2 | Rückmeldung | mehrere Entitäten | Manche Fehler erscheinen nur über die globale Fehlermeldung, während andere direkt am Formular stehen. Nach einem Tabwechsel ist die Ursache nicht immer beim betroffenen Feld sichtbar. | Fehlerbehebung benötigt zusätzliche Suche; erfolgreiche und fehlgeschlagene Aktionen sind uneinheitlich bestätigt. |

## Abgegrenzte Folgeanforderungen

### Paket A: Übersicht als priorisierte Arbeitsliste

1. Eine gemeinsame, serverseitig begrenzte Arbeitsliste fasst ausschließlich Referenzen auf offene Vorgänge und offene/ungeklärte Nebenelemente zusammen; sie legt keine Ersatzverknüpfungen an.
2. Jede Zeile zeigt Entität, fachlichen Zustand, Dringlichkeitsgrund, relevante Fälligkeit/Datum, Vorgangsbezug und genau eine primäre nächste Aktion.
3. Die Standardsortierung ist nachvollziehbar: erst konkrete Abschlussblocker beziehungsweise überfällige Elemente, dann ungelesene/ungeklärte Eingänge, danach übrige offene Vorgänge; innerhalb einer Stufe älteste oder früheste Fälligkeit zuerst. Die endgültige Fachreihenfolge ist mit der Kassiererrolle abzustimmen.
4. Jede Übersichtskarte aktiviert im Ziel einen sichtbaren passenden Filter. Für Dokumente ist eine kleine, direkt bearbeitbare Liste oder ein dokumentbezogener Filter erforderlich; ein Wechsel zur ungefilterten Vorgangsliste genügt nicht.
5. Aktiver Filter, Trefferzahl und Rückweg zur Übersicht bleiben beim Bearbeiten erkennbar.

**Akzeptanz:** Alle sieben heutigen Kennzahlen sind ohne manuelles Nachsuchen abarbeitbar; vorhandene Zählsemantik bleibt erhalten und ist durch lokale Tests abgedeckt.

### Paket B: Einheitlicher Zuordnungsdialog

1. Ein wiederverwendbares UI-Muster bietet für Transaktion, Mail, To-Do, Termin und Dokument dieselben Schritte: suchen, Kandidaten vergleichen, auswählen, Änderung zusammenfassen, speichern, Ergebnis bestätigen.
2. Kandidaten zeigen mindestens Titel/Bezug, Typ, Status, relevantes Datum, passende Beträge sowie einen Vorschlagsgrund; technische IDs sind sekundär sichtbar.
3. Bestehende und abgeschlossene Vorgänge sind eindeutig markiert und filterbar. Bereits verknüpfte Elemente können geöffnet, aber nicht versehentlich doppelt zugeordnet werden.
4. Jede Speicherung nutzt ausschließlich die vorhandenen Vorgangs-Link-APIs beziehungsweise Store-Methoden. Dokument-Transaktionszuordnung bleibt auf Elemente desselben Vorgangs beschränkt.
5. Validierungsfehler erscheinen am Dialog und erhalten Suche und Auswahl; 4xx-Antworten dürfen keine Teilverknüpfung hinterlassen.

**Akzeptanz:** Das Interaktionsmuster ist über alle fünf Einstiege gleich, ohne Datenmodell oder Verknüpfungsarchitektur zu ändern; Atomarität wird mit isolierten Tests geprüft.

### Paket C: Handlungsorientierte Abschlussblocker

1. Die API liefert Blocker zusätzlich zum Text strukturiert mit Blockertyp, betroffener Entität/ID und – soweit vorhanden – fehlendem Klassifikationsfeld.
2. Der Vorgangsarbeitsraum gruppiert Blocker nach Transaktion, Dokument und sonstiger Anforderung und bietet eine Aktion „Problem bearbeiten“, die zum bestehenden Editor beziehungsweise Katalogeintrag springt.
3. Nach erfolgreicher Korrektur werden Abschlussfähigkeit und Blockerliste ohne Schließen des Vorgangs aktualisiert.
4. Automatische oder manuelle Statusherkunft und der konkrete Grund einer Wiederöffnung werden sichtbar, ohne die bestehende Validierungs- oder Statuslogik zu lockern.
5. Der Abschlussknopf bleibt deaktiviert, solange die bestehende Servervalidierung Blocker meldet; die UI darf den Server nicht als Wahrheitsquelle ersetzen.

**Akzeptanz:** Jeder bestehende Abschlussblocker ist aus dem Statusbereich in höchstens einer Aktion erreichbar; Tests sichern Rechnungs-, Klassifikations- und Wiederöffnungsfälle ab.

### Paket D: Konsistente Aktionsrückmeldungen

1. Formulare verwenden einheitliche Zustände für ungespeichert, wird gespeichert, gespeichert und fehlgeschlagen.
2. Ein Dialog darf bei laufendem oder fehlgeschlagenem Autosave nicht kommentarlos geschlossen werden; nach Fehler bleiben Eingabe und konkreter Feldbezug erhalten.
3. Aktionen mit fachlichen Folgeeffekten nennen diese knapp, zum Beispiel „klassifiziert; Vorgang kann jetzt abgeschlossen werden“ oder „Vorgang wegen unvollständiger Transaktion wieder geöffnet“.

**Akzeptanz:** Browser-Tests prüfen mindestens Klassifikations-Autosave, Zuordnung und Abschluss jeweils für Erfolg und Fehler.

## Leistungs-, Funktions- und Sicherheitsrisiken

| Risiko | Auswirkung | Begrenzung für Folgepakete |
|---|---|---|
| Gemeinsame Arbeitsliste führt zu teuren Joins oder N+1-Abfragen | Langsames Dashboard bei Vereinsdaten | Aggregierte, indizierbare Abfrage; feste Vorschau-/Seitengröße; Details erst beim Öffnen laden; Query-Anzahl und Antwortgröße testen. |
| Live-Suche sendet zu viele Requests | Last und springende Treffer | Eingaben entprellen, vorherige Requests abbrechen, serverseitig begrenzen und paginieren. Das vorhandene Abort-Muster der Transaktionssuche wiederverwenden. |
| Vereinheitlichung verändert Linksemantik | Umgehung des Vorgangs oder falsche Mehrfachzuordnung | Nur UI-Muster teilen; bestehende APIs, Store-Validierung und Linktabellen unverändert nutzen. |
| Clientseitige Blocker weichen von Serverregeln ab | Unzulässiger Abschluss oder falsche Sperre | Blocker ausschließlich serverseitig ableiten; Client rendert und navigiert nur. |
| Automatisches Nachladen überschreibt ungespeicherte Eingaben | Datenverlust und Fehlklassifikation | Dirty-/Saving-Zustand explizit führen; Aktualisierung auf betroffene Teilbereiche begrenzen. |
| Umfangreiche Statushistorie vergrößert Datenmodell | Unnötige Persistenz- und Migrationsarbeit | Zunächst vorhandene Antwortdaten und unmittelbare Aktionsresultate erklären; Historisierung separat fachlich entscheiden. |
| Vorschlagsgründe werden als Gewissheit interpretiert | Fehlzuordnung | Vorschläge klar als Vorschläge kennzeichnen, nie vorauswählen, explizite Bestätigung verlangen. |
| Externe Mail- oder KI-Aktionen in Tests | Secrets, instabile Tests, echte Seiteneffekte | Ausschließlich vorhandene Fakes/Mocks und temporäre lokale Datenbanken verwenden. |

## Nachweis gegen die Akzeptanzkriterien

- Das Arbeitsablaufmodell deckt Sichten, Klassifizieren, Zuordnen und Abschließen ab.
- Jeder Reibungspunkt benennt Ablauf und fachliche Entität und ist nach Nutzerwirkung/Dringlichkeit priorisiert.
- Die Anforderungen A bis C bilden eigenständige kleine Folgepakete für Übersicht, Zuordnungsdialoge und Abschlussblocker; D kapselt die querschnittliche Rückmeldung.
- Vorgänge bleiben zentral; direkte Ersatzbeziehungen, Änderungen an Originaldaten und produktive externe Aktionen werden ausdrücklich ausgeschlossen.
- Typische Einstiege und Wechsel sowie unklare Zustände, fehlende Rückmeldungen, Zusatzschritte und Leistungsrisiken sind gesondert dokumentiert.

## Offene fachliche Entscheidungen vor Folgeumsetzung

1. Primäre Kassiererrolle und Erfahrungsniveau mit einem tatsächlichen Nutzer bestätigen.
2. Reihenfolge der Dringlichkeitsstufen und Umgang mit mehreren gleichzeitigen Kategorien fachlich freigeben.
3. Festlegen, ob manuell abgeschlossene Vorgänge bei neuen Blockern nur gewarnt oder wie automatisch abgeschlossene Vorgänge wieder geöffnet werden sollen; die bestehende Logik darf bis dahin nicht verändert werden.
4. Verbindliche Bedeutung der vorhandenen Filter, besonders bei mehrfach verknüpften Transaktionen, in der UI-Terminologie bestätigen.
