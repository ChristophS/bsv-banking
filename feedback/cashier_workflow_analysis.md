# Analyse der Kassierer-Workflows im Dashboard

## Auftrag und Rahmen

Diese Analyse beschreibt den aktuellen Stand der täglichen Vereinsverwaltung beim Sichten, Klassifizieren, Zuordnen, Validieren und Abschließen. Grundlage sind die vorhandene Oberfläche, die serverseitigen Fachregeln, die Dashboard-Tests und der README-Kontext. Es wurden keine produktiven Daten und keine externen Dienste verwendet.

Vorgänge bleiben in allen Vorschlägen das zentrale fachliche Objekt. Beziehungen zwischen Transaktionen, Dokumenten, Mails, To-Dos und Terminen sollen weiterhin ausschließlich über vorhandene Vorgangsbeziehungen laufen. Direkte Ersatzbeziehungen werden nicht empfohlen.

Die Prioritäten bedeuten:

- **P0 – zuerst:** häufige tägliche Arbeit ist unnötig fehleranfällig oder eine angezeigte Arbeitsmenge lässt sich nicht gezielt abarbeiten.
- **P1 – danach:** ein häufiger Ablauf braucht vermeidbare Wechsel oder sein Zustand beziehungsweise nächster Schritt ist unklar.
- **P2 – später:** merkliche Verbesserung, aber kein wesentlicher Blocker im täglichen Kernablauf.

## Heutiger Arbeitsablauf

### 1. Sichten und priorisieren

Der Einstieg „Offene Arbeit“ zeigt Kennzahlen für nicht abgeschlossene Vorgänge, ungelesene Mails, nicht zugewiesene Transaktionen, offene To-Dos, nicht zugewiesene Dokumente sowie anstehende und nicht zugewiesene Termine. Zusätzlich gibt es kurze Vorschauen für offene Vorgänge, To-Dos und Termine.

Von dort wechseln Kassierer in getrennte Reiter:

- **Vorgänge:** Suche, optionales Ausblenden abgeschlossener Vorgänge, Status und Summen der zugeordneten Entitäten.
- **Transaktionen:** standardmäßig letzte drei Monate, Volltextsuche, Sortierung und optionales Ausblenden von Transaktionen, deren Vorgänge alle abgeschlossen sind.
- **Mails:** ungelesene Nachrichten, Suche, Spam-Bewertung, Detailansicht, Zusammenfassung und Vorgangszuordnung beziehungsweise geprüfter Vorgangsimport.
- **To-Dos:** offene/abgeschlossene Aufgaben, Priorität, Fälligkeit und Vorgangsbezug.
- **Termine:** geplante/abgeschlossene/abgesagte Termine und Vorgangsbezug.
- **Dokumente:** kein eigener Reiter; der Katalog und seine Zuordnung werden über Vorgänge, Vorschläge und Mail-Importe erreicht.

### 2. Klassifizieren

Transaktionen werden in ihrer Detailansicht oder innerhalb eines Vorgangs über Transaktionstyp, Oberkategorie, Unterkategorie und Sphäre klassifiziert; die fachliche Beschreibung ist ergänzend. Der Klassifikationsstatus wird nach Änderungen neu berechnet. Regeln können vollständig unklassifizierte Transaktionen automatisch bearbeiten, ohne manuelle Teilklassifikationen zu überschreiben. Splits besitzen dieselben Klassifikationsfelder und können einem bereits mit der Transaktion verknüpften Vorgang zugeordnet werden.

### 3. Zuordnen

Ein Vorgang kann aus einer Transaktion, Mail, einem To-Do, Dokument oder Termin heraus angelegt werden. Das Formular zeigt vorhandene und vorgeschlagene Entitäten getrennt nach Typ; Vorschläge werden sortiert und müssen bewusst bestätigt werden. Bestehende Vorgänge können in Transaktions- und Maildetails gesucht und zugeordnet werden. To-Dos und Termine können bei Anlage oder Bearbeitung mit mehreren Vorgängen verbunden werden. In Vorgangsdetails lassen sich alle fünf Entitätstypen gemeinsam pflegen.

### 4. Validieren

Die Oberfläche und der Server verhindern einen Abschluss, solange verknüpfte Transaktionen nicht vollständig klassifiziert sind. Für Vorgänge vom Typ „Rechnung“ werden zusätzlich mindestens eine Transaktion und mindestens ein Dokument verlangt. Die vorhandene Ausnahme für als Fehlbuchung klassifizierte „Sonstige“-Vorgänge bleibt bestehen. Im geöffneten Vorgang werden Abschlussmöglichkeit und Blocker angezeigt.

### 5. Abschließen und nachhalten

Vorgänge können manuell abgeschlossen und wieder geöffnet werden; manuell gesetzte Status werden von Automatikregeln nicht überschrieben. Abschlussregeln können geeignete Vorgänge nach der Klassifikation automatisch schließen. Das Abschließen eines Vorgangs markiert verknüpfte Mails als gelesen. To-Dos und Termine besitzen eigene, davon unabhängige Abschlusszustände.

## Priorisierte Reibungspunkte und abgegrenzte Verbesserungen

| Prio | Phase | Problemart | Beobachtung und Auswirkung | Abgegrenzter Verbesserungsvorschlag |
|---|---|---|---|---|
| **P0.1** | Sichten | fehlende Sichtbarkeit | Die Übersicht zählt unterschiedliche Arbeitsmengen, aber es gibt keine gemeinsame, nach Dringlichkeit sortierte Arbeitsliste. Kassierer müssen aus Kennzahlen und drei separaten Vorschauen selbst ableiten, womit sie beginnen. Überfällige To-Dos, unklassifizierte Transaktionen und nicht abschließbare Vorgänge konkurrieren ohne gemeinsame Priorität. | Eine vorgangsbasierte **Arbeitsliste** als Erweiterung der Übersicht definieren: wenige fachlich feste Gründe wie „überfällig“, „Klassifikation fehlt“, „Zuordnung fehlt“ und „abschlussbereit“. Jeder Eintrag führt in den bestehenden Vorgang beziehungsweise in den passenden Entitätskontext. Keine neue Fachentität und keine direkte Entitätsbeziehung einführen. |
| **P0.2** | Sichten/Zuordnen | fehlende Rückmeldung | Die Karte „Nicht zugewiesene Dokumente“ öffnet lediglich den Vorgangsreiter; dort wird kein Dokumentfilter gesetzt und nicht erkennbar erklärt, welche Dokumente die Kennzahl erzeugt haben. Die angezeigte Arbeitsmenge ist damit nicht gezielt abarbeitbar. | Einen fokussierten **Dokument-Zuordnungsmodus im Vorgangskontext** vorsehen: Karte setzt einen sichtbaren, zurücksetzbaren Filter oder öffnet eine bestehende Vorgangserstellung mit der Liste unzugeordneter Dokumente. Auswahl führt weiterhin zu `vorgang_belege`, nie zu einer direkten Transaktions-Dokument-Beziehung. |
| **P0.3** | Validieren/Abschließen | unklare Zustände | In der Vorgangsliste ist nur „in Bearbeitung“ oder „abgeschlossen“ sichtbar. Ob ein Vorgang sofort abgeschlossen werden kann und welcher konkrete Blocker besteht, erfahren Kassierer erst nach dem Öffnen. Das erzeugt wiederholtes Öffnen und Schließen vieler Vorgänge. | In der bestehenden Vorgangsliste einen **abgeleiteten Arbeitszustand** anzeigen, beispielsweise „abschlussbereit“, „Klassifikation fehlt“, „Transaktion fehlt“ oder „Dokument fehlt“. Die bestehenden Statuswerte bleiben unverändert; die Anzeige wird aus den vorhandenen Abschlussanforderungen abgeleitet. Ein Klick öffnet den Vorgang am relevanten Abschnitt. |
| **P1.1** | Klassifizieren | unnötige Schritte | Die Transaktionsliste zeigt Vorgangszuordnung, aber nicht den Klassifikationsstatus oder die fehlenden Pflichtfelder. Eine gezielte Runde „alle unvollständigen Buchungen bearbeiten“ erfordert das Öffnen einzelner Zeilen oder indirektes Arbeiten über Vorgänge. | Einen klaren **Klassifikationsfilter** und eine kompakte Statusanzeige in der Transaktionsliste ergänzen. In der Detailansicht fehlende Pflichtfelder zuerst anzeigen und nach erfolgreicher Klassifikation eine Aktion „Nächste unvollständige Transaktion“ anbieten. Klassifikation bleibt an der Transaktion beziehungsweise ihren Splits; der Vorgangsstatus wird wie bisher abgeleitet. |
| **P1.2** | Zuordnen | unnötige Schritte | Zuordnung ist je Entität unterschiedlich erreichbar: Mails und Transaktionen besitzen eine Suche im Detail, To-Dos und Termine ein Mehrfachauswahlfeld, Dokumente werden vor allem über Vorgangsformulare erreicht. Das ist fachlich korrekt, aber die nächste Handlung hängt stark vom Ausgangsreiter ab. | Einen einheitlichen **„Vorgang zuordnen oder erstellen“‑Ablauf** für die fünf Entitätstypen gestalten. Wiederverwenden: vorhandene Kandidatensuche, Vorschlagsgründe, bewusste Auswahl und Entitätsvorschau. Nur die Einstiegspunkte und Rückmeldungen vereinheitlichen; Persistenz bleibt bei den vorhandenen Vorgangs-Verknüpfungen. |
| **P1.3** | Zuordnen | unklare Zustände | Vorschläge enthalten Gründe, Scores und Klassifikationshinweise, doch die Bedeutung von „Vorschlag“, „Quelle“ und bereits bestätigter Auswahl ist nicht durchgängig erklärt. Hohe Scores werden mit gutem Grund nicht automatisch ausgewählt, können aber als vermeintlich sichere Zuordnung missverstanden werden. | Vorschläge visuell in **bestehend verknüpft**, **zur Prüfung vorgeschlagen** und **weitere Treffer** gruppieren. Eine kurze Erklärung festhalten: Vorschläge sind nie automatisch bestätigt. Vor dem Speichern eine kompakte Zusammenfassung der hinzukommenden und entfernten Beziehungen zeigen. |
| **P1.4** | Abschluss | unklare Zustände | Vorgangsabschluss, To-Do-Abschluss, Terminstatus und Mail-Lesestatus sind getrennte Zustände. Der Mail-Lesestatus ändert sich beim Vorgangsabschluss, offene To-Dos oder geplante Termine blockieren den Abschluss dagegen nicht. Ohne sichtbare Abschlusszusammenfassung kann „abgeschlossen“ fälschlich als Abschluss aller angrenzenden Arbeit verstanden werden. | Vor dem manuellen Abschluss eine **kompakte Abschlussprüfung** zeigen: erfüllte Pflichtbedingungen, noch offene To-Dos, geplante Termine und die Rückmeldung „verknüpfte Mails werden als gelesen markiert“. To-Dos und Termine bleiben unabhängig und werden nicht still mit abgeschlossen. Warnungen zu ihnen sind zunächst informativ, sofern keine neue Fachregel ausdrücklich beschlossen wird. |
| **P1.5** | Sichten/Nachhalten | fehlende Sichtbarkeit | Die Übersicht zählt unzugeordnete Transaktionen, Dokumente und Termine, aber nicht unzugeordnete To-Dos oder Mails. Gleichzeitig sind To-Dos und Mails wichtige Eingänge für Vorgänge. Dadurch bleibt offen, ob fehlender Vorgangsbezug dort bewusst oder unbearbeitet ist. | Fachlich klären und danach konsistente **Zuordnungskennzahlen** ergänzen. Nur Entitäten zählen, für die Zuordnung tatsächlich erwartet wird; bewusst eigenständige Einträge benötigen gegebenenfalls einen sichtbaren Zustand „kein Vorgang erforderlich“, statt dauerhaft als offen zu erscheinen. |
| **P2.1** | Sichten | unnötige Schritte | Filterzustände werden durch Übersichtskarten teilweise gesetzt, aber nur der besondere Terminfilter wird als eigener sichtbarer Filterhinweis dargestellt. Beim Wechsel zwischen Übersicht und Reitern ist deshalb nicht immer offensichtlich, warum nur ein Teilbestand sichtbar ist. | Für alle aus der Übersicht gesetzten Filter einen einheitlichen **Filterkontext mit Zurücksetzen** anzeigen, etwa „Aus Übersicht: nicht zugewiesen“. Trefferzahl und Leerzustand sollen den aktiven Filter benennen. |
| **P2.2** | Bearbeiten | fehlende Rückmeldung | Speichern wird in vielen Detailbereichen lokal bestätigt, anschließend werden Listen oder Dialoge neu geladen. Nach Zuordnung oder Klassifikation fehlt jedoch ein durchgängiger Hinweis, welche Arbeitsblockade dadurch gelöst wurde und ob der Vorgang nun abschlussbereit ist. | Nach relevanten Änderungen eine **fachliche Ergebnisrückmeldung** anzeigen: „zugeordnet“, „vollständig klassifiziert“, „Vorgang jetzt abschlussbereit“ oder verbleibender Blocker. Keine dauerhafte Aktivitäts- oder Auditarchitektur für dieses UI-Paket einführen. |

## Abgrenzung sinnvoller Folgearbeitspakete

Die nachfolgenden Pakete sind so geschnitten, dass sie einzeln umgesetzt und getestet werden können:

1. **Arbeitsgründe und Navigation schärfen (P0.2, P0.3):** Abgeleitete Arbeitszustände definieren, Dokument-Karte in einen echten Zuordnungskontext routen und Filterkontext sichtbar machen. Das ist der kleinste Schritt mit direkter Wirkung.
2. **Klassifikationsrunde beschleunigen (P1.1):** Status/fehlende Felder in der Transaktionsliste, Filter und „nächste unvollständige“ Navigation. Keine Regel- oder Datenmodelländerung.
3. **Vorgangsbasierte Arbeitsliste (P0.1):** Erst nach stabiler Definition der Arbeitsgründe eine priorisierte Liste auf der Übersicht ergänzen. Die Liste referenziert bestehende Vorgänge und Entitäten.
4. **Zuordnungsdialog vereinheitlichen (P1.2, P1.3):** Gemeinsame UI-Komponenten und klare Vorschlagsgruppen für Transaktion, Mail, To-Do, Dokument und Termin; vorhandene Endpunkte und Verknüpfungen wiederverwenden.
5. **Abschlussprüfung und Ergebnisrückmeldung (P1.4, P2.2):** Bestehende Abschlussblocker plus informative Hinweise zu offenen angrenzenden Einträgen anzeigen; Seiteneffekte transparent machen.
6. **Zuordnungspolitik für Mail und To-Do klären (P1.5):** Erst fachlich entscheiden, wann ein Vorgangsbezug erwartet wird; danach Kennzahlen oder einen bewussten Ausnahmezustand umsetzen.
7. **Filterkonsistenz und Feinschliff (P2.1):** Einheitliche Filterchips, Leerzustände und Zurücksetzen über alle Arbeitsreiter.

## Auswirkungen und Randbedingungen

### Bestehende Funktionen

- Manuelle und automatische Klassifikation, Splits und Abschlussregeln dürfen nicht in ihrer Reihenfolge oder Schutzwirkung verändert werden.
- Manuell gesetzte Vorgangsstatus dürfen weiterhin nicht von Automatik überschrieben werden.
- Die besonderen Abschlussregeln für Rechnungen und Fehlbuchungen müssen aus derselben serverseitigen Fachlogik gespeist werden; UI-Texte dürfen keine abweichende zweite Regelquelle bilden.
- Bewusstes Bestätigen von Vorschlägen bleibt erhalten. Ein Score allein darf keine Beziehung anlegen.
- Separate Zustände von Vorgang, To-Do und Termin bleiben bestehen, solange keine neue fachliche Regel beschlossen und separat umgesetzt wird.
- Das Markieren verknüpfter Mails als gelesen beim Vorgangsabschluss muss vor der Aktion sichtbar werden und funktional erhalten bleiben.

### Leistung

- Listen dürfen nicht pro Zeile zusätzliche Einzelabfragen auslösen. Arbeitszustände und Zähler sollten in vorhandenen Listen-/Übersichtsabfragen aggregiert oder in einer begrenzten Arbeitslistenabfrage geliefert werden.
- Eine Arbeitsliste braucht eine feste Obergrenze beziehungsweise serverseitige Begrenzung; vollständige Mailtexte, Anhänge, Rohdaten und Dokumentinhalte gehören nicht in die Übersicht.
- Bestehende verzögerte Mail- und Anhangsladung bleibt erhalten. Usability-Verbesserungen dürfen keine externe Analyse oder Volltextladung beim bloßen Öffnen der Übersicht auslösen.
- Suchen und Filter sollen weiterhin serverseitige, indexierbare Kriterien verwenden. Eine neue globale Suche über sämtliche Detailinhalte ist nicht Teil der vorgeschlagenen kleinen Pakete.

## Offene fachliche Fragen

Vor P1.4 und P1.5 sollten Kassierer beziehungsweise Vereinsverwaltung verbindlich beantworten:

1. Müssen offene To-Dos oder geplante Termine einen Vorgangsabschluss blockieren, nur warnen oder je Eintrag als bewusst offen bestätigt werden?
2. Welche Mails und To-Dos benötigen zwingend einen Vorgangsbezug, und welche dürfen dauerhaft eigenständig bleiben?
3. Welche Reihenfolge gilt im Alltag tatsächlich: überfällige Aufgaben, neue Mails, unklassifizierte Transaktionen, fehlende Dokumente oder abschlussbereite Vorgänge?
4. Soll „nicht zugewiesene Transaktion“ ausschließlich „ohne jeden Vorgang“ bedeuten oder auch „nur einem automatisch erzeugten Standardvorgang zugeordnet“ erfassen?
5. Wer darf einen automatisch ermittelten Status manuell überschreiben, und soll die Oberfläche den Grund dafür erfassen?

## Prüfbarkeit der vorgeschlagenen nächsten Handlungen

Für jeden priorisierten Zustand ist eine konkrete nächste Handlung ableitbar:

- **Klassifikation fehlt:** betroffene Transaktion mit den fehlenden Feldern öffnen.
- **Transaktion fehlt:** vorhandene Transaktion suchen/zuordnen oder Vorgang offen lassen.
- **Dokument fehlt:** Dokumentkatalog im Vorgangskontext öffnen und über `vorgang_belege` zuordnen.
- **Zuordnung fehlt:** bestehenden Vorgang auswählen oder neuen Vorgang aus der Entität erstellen.
- **Abschlussbereit:** Abschlussprüfung öffnen und bewusst abschließen.
- **Offenes To-Do/geplanter Termin:** angrenzenden Eintrag öffnen; nicht still zusammen mit dem Vorgang abschließen.

