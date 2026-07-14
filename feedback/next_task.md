# Nächstes Arbeitspaket

## Titel

Klassifikations- und Abschlussblocker verständlich und handlungsorientiert darstellen

## Epic

**Epic-ID:** epic-cashier-usability

**Epic-Titel:** Kassiererfreundliche Arbeitsabläufe im Dashboard verbessern

**Epic-Ziel:** Die tägliche Vereinsverwaltung im Dashboard mit klaren Prioritäten, verständlichen Zuständen und reibungsarmen Zuordnungsabläufen unterstützen, ohne Funktionsumfang oder Leistung zu verschlechtern.

**Teilpaket:** Teil 4

## Ziel

Kassierer sollen bei nicht abschließbaren Vorgängen klar erkennen, welche Klassifikationsfelder oder Belege fehlen und welche nächsten Schritte erforderlich sind, ohne bestehende Validierungen zu umgehen.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Nicht abschließbare Vorgänge müssen einen verständlichen, handlungsorientierten Hinweis zum jeweiligen Abschlussblocker anzeigen.
- Fehlende oder unvollständige Klassifikationsfelder müssen eindeutig benannt werden.
- Fehlende erforderliche Belege oder andere bereits bestehende Abschlussvoraussetzungen müssen verständlich ausgewiesen werden, sofern sie den Abschluss verhindern.
- Die Darstellung muss den bestehenden fachlichen Abschlussprüfungen folgen und darf deren Validierung nicht umgehen oder abschwächen.

## Soll umgesetzt werden

- Hinweise sollen zwischen behobenen und weiterhin offenen Abschlussblockern unterscheidbar sein.
- Die Darstellung soll sich in die bestehenden Vorgangs- und Dashboard-Strukturen einfügen.

## Nicht Teil dieses Arbeitspakets

- Neue Abschlussregeln oder neue Pflichtfelder einführen.
- Vorgangs-, Beleg-, Transaktions- oder Verknüpfungsstrukturen umbauen.
- Automatische Klassifikation oder automatische Belegerzeugung.
- Performance-Optimierungen oder eine umfassende Überarbeitung anderer Dashboard-Listen.

## Akzeptanzkriterien

- Für einen Vorgang mit fehlenden Klassifikationsangaben wird sichtbar angezeigt, welche Angaben fehlen.
- Für einen Vorgang mit fehlendem erforderlichem Beleg wird sichtbar angezeigt, dass der Beleg fehlt.
- Bei mehreren Blockern werden alle relevanten offenen Blocker verständlich dargestellt.
- Ein Vorgang kann weiterhin nur dann abgeschlossen werden, wenn die bestehenden fachlichen Abschlussprüfungen erfüllt sind.
- Für die neue Darstellung existieren automatisierte Tests für mindestens fehlende Klassifikation, fehlenden Beleg und einen blockfreien beziehungsweise abschließbaren Vorgang.
- Bestehende Funktionen und Tests für Vorgänge und Abschlussprüfungen bleiben erhalten.

## Hinweise für den Umsetzungs-Agenten

- Bestehende Status- und Abschlussprüfungen sowie die vorhandenen Vorgangsstrukturen wiederverwenden.
- Keine direkte Ersatzbeziehung zwischen Transaktionen, Belegen oder anderen Entitäten einführen.
- Technische Detailentscheidungen zur konkreten UI- oder Service-Schicht können bei der Repository-Analyse getroffen werden.

## Manuelle Testhinweise

- Einen Vorgang mit unvollständiger Klassifikation öffnen und prüfen, ob die fehlenden Felder verständlich genannt werden.
- Einen Vorgang mit fehlendem erforderlichem Beleg öffnen und prüfen, ob der Abschlussblocker und die erforderliche Aktion erkennbar sind.
- Einen Vorgang mit mehreren Blockern sowie einen vollständig vorbereiteten Vorgang prüfen.

## Offene Fragen

- Welche bestehenden Abschlussprüfungen liefern bereits strukturierte Gründe und welche müssen lediglich für die Darstellung aufbereitet werden?
- An welcher bestehenden Dashboard-Ansicht werden Vorgangsstatus und Abschlussaktionen aktuell angezeigt?
