# Nächstes Arbeitspaket

## Titel

Explizite Fehlererkennung für fehlende externe Mailobjekte ergänzen

## Epic

**Epic-ID:** epic-mail-synchronisation

**Epic-Titel:** Mailübersicht robust mit dem externen Mailbestand synchronisieren

**Epic-Ziel:** Mailstatus und Mailübersicht sollen mit erwartbaren externen Änderungen und temporären Mailbox-Fehlern robust umgehen.

**Teilpaket:** Teil 1.1

## Ziel

Die Mail-Synchronisation soll das erwartbare Fehlen eines externen Mailobjekts eindeutig von anderen Lookup- und temporären Mailbox-Fehlern unterscheiden können.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Eine explizite Exception-Klasse oder einen strukturierten Fehlercode für ein fehlendes externes Mailobjekt einführen oder die vorhandene entsprechende Struktur verwenden.
- Die Mail-Synchronisationslogik so anpassen, dass dieser Fall gezielt erkannt und fachlich behandelt werden kann.
- Andere Lookup-, Authentifizierungs- und temporäre Mailbox-Fehler weiterhin unterscheidbar behandeln.
- Die bestehende vorgangsbasierte Struktur und vorhandene Mail-Verknüpfungen unverändert weiterverwenden.

## Soll umgesetzt werden

- Die Fehlerstruktur so gestalten, dass sie unabhängig von instabilen Fehlermeldungstexten auswertbar ist.
- Tests für das fehlende externe Mailobjekt sowie mindestens einen davon abgrenzbaren Fehlerfall ergänzen.

## Nicht Teil dieses Arbeitspakets

- Die sichtbare Entfernung eines stale Mail-Eintrags aus der Mailübersicht; dies bleibt Teil 1.2.
- Ein echter Zugriff auf externe Maildienste.
- Neue Mail-, Vorgangs- oder Verknüpfungsmodelle.
- Unabhängige Spenden-, Adress- oder DFBnet-Funktionen.

## Akzeptanzkriterien

- Ein fehlendes externes Mailobjekt wird über eine explizite Exception oder einen strukturierten Fehlercode erkannt und nicht über den Vergleich eines Fehlermeldungstextes.
- Die Synchronisationslogik kann den Fall fehlendes externes Mailobjekt separat von generischen Lookup- oder temporären Mailbox-Fehlern behandeln.
- Bestehende Fehlerfälle behalten ihr bisheriges fachliches Verhalten, sofern sie nicht eindeutig ein fehlendes externes Mailobjekt darstellen.
- Automatisierte Tests belegen die eindeutige Erkennung des fehlenden externen Mailobjekts und die Abgrenzung zu mindestens einem anderen Fehlerfall.
- Alle Tests laufen ohne echte externe Mailaktionen und verwenden Mocks, Fakes oder Fixtures.

## Hinweise für den Umsetzungs-Agenten

- Zunächst vorhandene Mail-Integrations- und Teststrukturen nutzen; konkrete Änderungsstellen kann der Coding-Agent anhand des Repositorys bestimmen.
- Die Fehlerklassifikation sollte möglichst auf stabilen Typen oder Codes des verwendeten Mail-Clients basieren und eine notwendige Übersetzung in eine domänenspezifische Struktur kapseln.
- Keine Secrets, Tokens oder produktiven Maildaten für Tests oder Implementierung anfordern.

## Manuelle Testhinweise

- Nicht erforderlich; die fachliche Abgrenzung soll automatisiert mit Mocks oder Fakes geprüft werden.

## Offene Fragen

- Welche konkrete externe Mailbibliothek und welche bereits vorhandenen Fehlerstrukturen im Repository verwendet werden, ist durch den Coding-Agenten zu prüfen.
