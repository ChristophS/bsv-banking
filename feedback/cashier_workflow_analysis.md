# Analyse der Kassierer-Workflows im Dashboard

## Zweck, Umfang und Annahmen

Diese Bestandsaufnahme beschreibt die vorhandenen Wege zum Sichten, Klassifizieren,
Zuordnen und Abschließen aus Sicht der allgemeinen Vereinsfinanzverwaltung. Grundlage
sind Dashboard, lokale API und Dashboard-Tests; externe Dienste und produktive Daten
wurden nicht verwendet.

Mangels festgelegter Rollen wird ein Kassierer mit Zugriff auf alle vorhandenen
Bereiche angenommen. Die bestehenden fachlichen Zustände bleiben verbindlich:
Vorgänge und To-Dos sind offen oder abgeschlossen, Termine geplant oder
abgeschlossen, Transaktionen unklassifiziert, teilweise oder vollständig
klassifiziert und Mails gelesen oder ungelesen. Vorgänge bleiben das zentrale Objekt;
die vorhandenen N:M-Verknüpfungen zu Transaktionen, Belegen, Mails, To-Dos und
Terminen sind zu erhalten.

## Systematische Bestandsaufnahme

### 1. Offene Arbeit sichten und priorisieren

**Vorhandener Weg:** Die Startübersicht zeigt Kennzahlen für offene Vorgänge,
ungelesene Mails, nicht zugewiesene Transaktionen, offene To-Dos, nicht zugewiesene
Dokumente sowie anstehende und nicht zugewiesene Termine. Drei Vorschaulisten zeigen
offene Vorgänge, To-Dos und anstehende Termine. Karten und Vorschauen wechseln in den
jeweiligen Bereich; Suche und Filter erfolgen erst dort.

**Reibungspunkte:**

- P1: „Nicht zugewiesene Transaktionen“ aktiviert den Filter „Transaktionen zu
  abgeschlossenen Vorgängen ausblenden“. Das bildet „ohne Vorgang“ nicht exakt ab und
  kann Transaktionen offener Vorgänge zeigen. Kennzahl und Zielliste können abweichen.
- P1: „Nicht zugewiesene Dokumente“ öffnet nur den Vorgangsbereich. Dort gibt es
  weder Dokumentliste noch sichtbaren Filter für unzugeordnete Belege.
- P2: Vorschauzeilen öffnen nur den Bereich, nicht das konkrete angezeigte Objekt.
- P2: Überfällige To-Dos, heutige Termine und blockierte Vorgänge haben keine
  gemeinsame Dringlichkeitslogik.
- P2: „Alles synchronisieren“ zeigt nicht dauerhaft, welche Quelle erfolgreich oder
  fehlerhaft war; Fehler erscheinen überwiegend als fünf Sekunden sichtbarer Toast.

**Positiv:** Offene Vorgänge werden vor abgeschlossenen sortiert; To-Do-Priorität,
Fälligkeit und Terminzeit sind sichtbar. Viele Mutationen aktualisieren die Übersicht.

### 2. Transaktionen sichten und klassifizieren

**Vorhandener Weg:** Transaktionen lassen sich durchsuchen, zeitlich filtern und nach
sichtbaren Spalten sortieren. Die Detailansicht enthält Rohdaten, Verknüpfungen,
Klassifikation und Splits. Klassifikation erfolgt manuell oder über Regeln, die
manuelle Werte nicht überschreiben. Splits müssen in Summe dem Betrag entsprechen
und können Vorgängen und Belegen zugeordnet werden.

**Reibungspunkte:**

- P1: Ein eindeutiger Listenfilter „unklassifiziert/teilweise klassifiziert“ fehlt,
  obwohl vollständige Klassifikation Abschlussvoraussetzung ist.
- P1: Ein exakter Filter „keinem Vorgang zugeordnet“ fehlt (siehe Übersicht).
- P2: Klassifikation, Splits, Zuordnung und Regelpflege teilen eine umfangreiche
  Detailarbeitsfläche. „Speichern und nächste offene Transaktion“ fehlt.
- P2: Die fachlichen Klassifikationszustände werden in der Gesamtübersicht nicht mit
  fehlenden Pflichtfeldern handlungsorientiert erklärt.
- P3: Seltene Regelpflege erhöht die visuelle Dichte des täglichen Workflows.

**Fehlerbehandlung:** Serverseitige Validierungen schützen bestehende Splits und
Vorgangsstatus bei Fehlern. In der UI bleibt meist nur ein flüchtiger globaler Toast
statt dauerhafter Korrekturhilfe am Feld.

### 3. Entitäten einem Vorgang zuordnen

**Vorhandener Weg:** Vorgänge verknüpfen Transaktionen, Belege, Mails, To-Dos und
Termine. Transaktionen, Mails und To-Dos bieten außerdem Wege, einen Vorgang zu wählen
oder neu anzulegen. Vorschläge unterstützen einzelne Zuordnungen; Mehrfachlinks
werden im Vorgangsdetail zusammengeführt.

**Reibungspunkte:**

- P1: Der Einstieg ist je Entität unterschiedlich. Dokumente haben keine eigene
  Arbeitsliste; die übrigen Bereiche verwenden verschiedene Auswahlmuster.
- P1: Auswahlfelder laden häufig viele Vorgänge. Bei wachsendem Bestand leiden
  Auffindbarkeit, Payload-Größe und Renderzeit; serverseitige Suche ist vorzuziehen.
- P2: Nach einer Zuordnung ist nicht überall direkt sichtbar, welche
  Abschlussvoraussetzung als Nächstes fehlt.
- P2: Vorschläge werden zu Recht nicht automatisch ausgewählt, aber Nutzen und
  Begründung sind nicht überall gleich verständlich dargestellt.

**Positiv:** Unbekannte Ziele werden abgelehnt, Zuordnungen sind idempotent und
fehlerhafte Requests hinterlassen laut Tests keine partiellen Fachobjekte. Diese
Sicherheit darf durch UI-Vereinfachungen nicht geschwächt werden.

### 4. Vorgänge prüfen und abschließen

**Vorhandener Weg:** Die Liste zeigt Typ, Status und Bezug und kann abgeschlossene
Vorgänge ausblenden. Im Detail stehen alle verknüpften Entitäten. Abschluss verlangt
vollständig klassifizierte Transaktionen; Rechnungen benötigen zusätzlich mindestens
eine Transaktion und einen Beleg. Fehlbuchungs-Ausnahme, manuelle Statushoheit und
automatische Abschlussregeln werden berücksichtigt.

**Reibungspunkte:**

- P1: „Offen und abschließbar“ sowie „offen und blockiert“ sind nicht in der Liste
  sichtbar oder filterbar; jeder Vorgang muss geöffnet werden.
- P1: Abschlussblocker bieten keine direkten Aktionen wie „fehlende Klassifikation
  öffnen“ oder „Beleg zuordnen“.
- P2: Automatischer und manueller Status (`status_manuell`) werden nicht durchgehend
  als Herkunft des Zustands erklärt.
- P2: Eine später unvollständige Klassifikation öffnet automatisch abgeschlossene
  Vorgänge korrekt wieder, doch die Oberfläche erklärt diese Ursache nicht.

### 5. Belege bearbeiten

**Vorhandener Weg:** Lokale Belege werden katalogisiert, in Vorgangs- oder
Transaktionsdetails angezeigt, im Original geöffnet und mit Vorgängen verknüpft. Für
Mailanhänge existiert zusätzlich eine Dokumentzuordnung im Vorgangskontext.

**Reibungspunkte:**

- P1: Trotz Übersichtszähler fehlt eine Warteschlange, um nicht zugewiesene Belege
  nacheinander zu prüfen und zuzuordnen.
- P2: „Beleg“ und „Dokument“ werden uneinheitlich verwendet; Mailanhang,
  katalogisierte Datei und Beleg sind für Nutzer schwer abzugrenzen.
- P2: Original öffnen, Kontext prüfen und zuweisen verteilt sich auf mehrere Details.

### 6. Mails bearbeiten

**Vorhandener Weg:** Die Mailansicht zeigt ungelesene Mails und Verläufe, Inhalte und
Anhänge, Zusammenfassung, Spam-Bewertung, Antwort, Gelesen-Markierung, To-Do- und
Termin-Erstellung sowie Vorgangssuche/-import. Beim Import können Transaktionen
klassifiziert und Entitäten verknüpft werden.

**Reibungspunkte:**

- P1: Der Maildetailbereich bündelt sehr viele Entscheidungen; die Reihenfolge
  „prüfen, zuordnen, Folgeaufgaben übernehmen, gelesen setzen“ ist nicht als
  Fortschritt erkennbar.
- P1: Gelesen-Markierung hat beim Vorgangsabschluss fachliche Seiteneffekte, die vor
  der Aktion nicht transparent sind.
- P2: Nach Fehler einer späteren externen Aktualisierung bleibt nicht dauerhaft
  sichtbar, ob die Liste vollständig oder nur lokal ist.
- P2: Ein Vorgangsimport kann erfolgreich sein, während direkter Abschluss abgewiesen
  wird. Die Meldung führt nicht unmittelbar zur passenden Korrekturaktion.

### 7. To-Dos bearbeiten

**Vorhandener Weg:** To-Dos können gesucht, nach Abschluss gefiltert, priorisiert,
terminiert, bearbeitet, gelöscht, per Checkbox abgeschlossen und mehreren Vorgängen
zugeordnet werden. Aus einem To-Do kann ein Vorgang entstehen; Überfälligkeit wird
markiert.

**Reibungspunkte:**

- P2: Sortierung/Filter nach Überfälligkeit, Fälligkeit und Priorität fehlen.
- P2: Die große Vorgangs-Mehrfachauswahl skaliert schlecht und unterscheidet offene
  nicht klar von abgeschlossenen Zielen.
- P2: Schneller To-Do-Abschluss zeigt nicht, ob daraus offene Vorgangsfolgen bleiben.
- P3: „To-Do + Vorgang“ erzeugt zusätzliche Dialog- und Fokuswechsel.

### 8. Termine bearbeiten

**Vorhandener Weg:** Termine können gesucht, nach Abschluss gefiltert, erstellt,
bearbeitet, gelöscht und mehreren Vorgängen zugeordnet werden. Status ist geplant
oder abgeschlossen. Die Übersicht öffnet gezielt nicht zugewiesene anstehende Termine.

**Reibungspunkte:**

- P2: Der Sonderfilter „Nicht zugewiesene anstehende Termine“ ist nur nach Navigation
  aus der Übersicht sichtbar, nicht regulär auswählbar.
- P2: Vergangene, noch geplante Termine bilden keine bezeichnete Überfällig-Liste.
- P2: Die vollständige Vorgangs-Mehrfachauswahl skaliert schlecht.
- P3: Termin- und Vorgangsabschluss sind getrennt, ohne Hinweis auf verbleibende
  Vorgangsarbeit.

## Priorisierte Verbesserungsbereiche

| Priorität | Fachliches Problem | Verbesserung | Einordnung |
| --- | --- | --- | --- |
| P1 | Übersicht und Ziellisten stimmen nicht überein | Exakte Filter für „ohne Vorgang“, „unklassifiziert/teilweise“ und nicht zugewiesene Belege | kurzfristige kleine UI-Pakete |
| P1 | Abschlussarbeit ist erst im Detail erkennbar | Vorgangsliste um „abschließbar/blockiert“, Blocker und Sprungaktionen ergänzen | eigenes UI/API-Paket |
| P1 | Dokumente besitzen keine Warteschlange | Belegliste mit Vorschau, Vorgangssuche und nächstem Eintrag | eigenes UI-Paket |
| P1 | Große, unterschiedliche Zuordnungen bremsen | Einheitliche suchbasierte Vorgangsauswahl, offene zuerst | Komponenten-Paket |
| P2 | Dringlichkeit ist verteilt | Arbeitslisten nach Überfälligkeit, Termin und Priorität strukturieren | später, bereichsübergreifend |
| P2 | Fehler und Teilerfolge sind flüchtig | Inline-Fehler, Retry und klarer lokaler/externer Ladestatus | Feedback-Paket |
| P2 | Wiederholte Navigation | „Speichern und nächster Eintrag“ sowie direkte Vorschau-Navigation | kleine UI-Pakete |
| P3 | Regelpflege erhöht Dichte | Regelverwaltung visuell vom Tagesworkflow trennen | späteres UI-Paket |

P1 bedeutet: tägliche Arbeit ist nicht eindeutig auffindbar oder wird unterbrochen.
P2 bedeutet: Arbeit ist möglich, braucht aber unnötige Navigation oder Interpretation.
P3 ist eine Optimierung ohne unmittelbare fachliche Blockade.

## Abgegrenzte Folgepakete

### UI-1 (klein, zuerst): Exakter Filter für nicht zugewiesene Transaktionen

**Problem:** Übersichtskarte und Zielzustand stimmen fachlich nicht überein.

**Umfang:**

- Bestehende Transaktions-API um booleschen Filter erweitern, der ausschließlich
  Transaktionen ohne Eintrag in `transaktion_vorgaenge` liefert.
- Toolbar-Option „Keinem Vorgang zugeordnet“ ergänzen; ein durch die Übersicht
  aktivierter Filter bleibt sichtbar.
- Übersichtskarte aktiviert exakt diesen Filter. Zeitraum, Suche, Sortierung und der
  bestehende Abschlussfilter bleiben kombinierbar.
- Keine Änderung an Vorgängen, Tabellen oder Verknüpfungen.

**Akzeptanzkriterien:**

1. Ergebniszahl nach Kartenklick entspricht bei unverändertem Datenstand der Karte.
2. Transaktionen mit mindestens einem Vorgang fehlen; solche ohne Vorgang erscheinen
   unabhängig von Klassifikation oder Vorgangsstatus.
3. Der aktive Filter ist sichtbar und ohne Seitenwechsel rücksetzbar.
4. API- und Browser-/DOM-Test decken Aktivierung, Kombination mit Suche und Reset ab.
5. Standardsicht und Antwortzeit bleiben erhalten; serverseitiges `NOT EXISTS`
   überträgt keine zusätzliche Kandidatenliste.

### UI-2 (klein): Direkte Vorschau-Navigation

Vorschauzeilen öffnen das konkrete Objekt. Ist es nach Aktualisierung nicht mehr da,
bleibt die Liste offen und zeigt eine persistente Meldung. Kein Datenmodellwechsel.

### UI-3 (klein): Klassifikations-Warteschlange

Ein serverseitiger Filter liefert unklassifizierte oder teilweise klassifizierte
Transaktionen. Liste und Detail nennen fehlende Pflichtfelder; nach Speichern kann der
nächste Treffer geöffnet werden. Bestehende Klassifikationslogik bleibt maßgeblich.

### UI-4 (eigenständig): Abschlussbereitschaft in der Vorgangsliste

Vorhandene Abschlussanforderungen werden als „abschließbar“ oder „blockiert“ angezeigt
und gefiltert; Aktionen führen zur fehlenden Klassifikation oder Belegzuordnung. API,
SQL und Antwortzeit sind mit größeren synthetischen Fixtures zu prüfen.

### UI-5 (eigenständig): Beleg-Zuordnungswarteschlange

Eine Liste unzugewiesener Belege bietet Originalvorschau, suchbasierte
Vorgangsauswahl, Speichern und „nächster Beleg“. Bestehende Entitäten und Links bleiben.

### UI-6 (eigenständig): Einheitliche suchbasierte Vorgangsauswahl

To-Dos, Termine, Mails, Belege und Transaktionen verwenden verzögerte serverseitige
Suche, offene Vorgänge zuerst und explizite Bestätigung. Mehrfachzuordnungen und
API-Validierung bleiben erhalten.

### UI-7 (später): Persistentes Arbeitsfeedback

Mutationserfolg, Validierungsfehler, Teilerfolg und lokaler/externer Ladestatus bleiben
am Objekt sichtbar. Es entstehen keine externen Aktionen; Tests verwenden Fakes.

## Datenmenge, Antwortzeit und Funktionsschutz

- Neue Warteschlangen sollen serverseitig gefiltert und paginierbar sein; vollständige
  Vorgangs-, Transaktions- oder Mailbestände sollen nicht zusätzlich geladen werden.
- `NOT EXISTS` ist fachlich passend; bei großen Fixtures sind Query-Plan und Indizes
  der Verknüpfungsschlüssel vor neuen dauerhaften Aggregaten zu prüfen.
- Direkte Vorschau-Navigation benötigt keine zusätzlichen Übersichtsdaten, weil die
  gelieferten Einträge bereits IDs enthalten.
- Abschlussbereitschaft darf nicht in JavaScript neu berechnet werden. Die vorhandene
  serverseitige Logik einschließlich Rechnung und Fehlbuchung bleibt alleinige Quelle.
- Atomare Fehlerpfade, manuelle Statushoheit, idempotente Zuordnung und bestehende
  N:M-Verknüpfungen müssen unverändert bleiben.

## Nicht Gegenstand dieser Analyse-Umsetzung

Es wurden keine UI, API, Persistenz, externen Integrationen oder fachlichen Zustände
geändert. Die Folgepakete sind unabhängig prüfbar; Vorgänge werden nicht durch eine
neue Arbeits- oder Inbox-Entität ersetzt.
