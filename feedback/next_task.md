# Nächstes Arbeitspaket

## Titel

DFBnet-Vereinsdaten als getrennte Leseintegration für Spendenbescheinigungen prüfen

## Epic

**Epic-ID:** epic-donation-certificates

**Epic-Titel:** Spendenbescheinigungen mit Empfängeradressen und Vereinsdaten erstellen

**Epic-Ziel:** Spendenempfänger lokal verwalten und daraus nachvollziehbare Spendenbescheinigungen erzeugen; eine spätere DFBnet-Vereinsanbindung bleibt sicher und getrennt.

**Teilpaket:** Teil 3

## Ziel

Eine belastbare technische Entscheidungsgrundlage erstellen, ob und wie ausschließlich lesbare Vereinsdaten aus DFBnet künftig zur Unterstützung von Spendenbescheinigungen genutzt werden könnten, ohne die bestehende Vorgangsarchitektur oder produktive DFBnet-Aktionen zu verändern.

## Relevante Dateien

- banking_dashboard/player_premiums.py
- tests/test_player_premiums.py
- feedback/backlog.md

## Wahrscheinliche Änderungsstellen

- feedback/backlog.md
- README.md

## Muss umgesetzt werden

- Die bestehende DFBnet-Integration auf ihre wiederverwendbaren Sicherheitsgrenzen prüfen: separates Browserprofil, lokale Credentials, Fehlerbehandlung und keine schreibenden Aktionen.
- Dokumentieren, welche konkreten Vereinsdaten für Spendenbescheinigungen fachlich erforderlich wären und welche davon bereits lokal gepflegt werden sollten.
- Eine klare Abgrenzung festhalten, dass DFBnet weder Quelle für Spendenempfänger noch Ersatz für eine lokale, nachvollziehbare Bescheinigungsgrundlage ist.
- Einen Vorschlag für eine spätere, getrennte read-only Adapter-Schnittstelle beschreiben, ohne sie produktiv zu implementieren.
- Festhalten, dass eine spätere Umsetzung nur mit Fixtures oder Mocks getestet werden darf und keine produktiven DFBnet-Schreibaktionen enthalten darf.

## Soll umgesetzt werden

- Mögliche technische Risiken wie instabile Weboberflächen, nicht garantierte Verfügbarkeit von Vereinsstammdaten und fehlende fachliche Autorität der Datenquelle benennen.
- Entscheidungskriterien formulieren, unter denen eine spätere Implementierung sinnvoll ist oder verworfen werden soll.

## Nicht Teil dieses Arbeitspakets

- Keine DFBnet-Automatisierung ergänzen oder verändern.
- Keine echten DFBnet-Logins, Browserläufe oder produktiven Netzwerkanfragen durchführen.
- Keine Secrets, Zugangsdaten, Browserprofile oder Laufzeitdaten anfordern oder verwenden.
- Keine Spendenempfänger-, Adress-, Vorgangs- oder Belegtabellen umbauen.
- Keine automatische Erstellung oder Versendung von Spendenbescheinigungen implementieren.

## Akzeptanzkriterien

- Eine nachvollziehbare Dokumentation beschreibt Datenbedarf, Nutzen, Risiken und Grenzen einer optionalen DFBnet-Leseintegration.
- Die Dokumentation trennt lokale Stammdaten und Bescheinigungslogik eindeutig von optionalen externen Vereinsdaten.
- Die vorgeschlagene spätere Integration ist als read-only, isolierter Adapter ohne direkte neue Entitätsbeziehungen beschrieben.
- Für eine spätere Implementierung sind Mock-/Fixture-Tests und das Verbot produktiver Schreibaktionen ausdrücklich festgelegt.
- Es wird keine produktive externe Aktion ausgelöst und keine sensible Laufzeit- oder Credential-Datei verändert.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandene DFBnet-Logik in banking_dashboard/player_premiums.py ist nur als Referenz für Sicherheits- und Isolationsmuster zu bewerten, nicht als direkte fachliche Grundlage für Spendenbescheinigungen.
- Vorgänge bleiben das zentrale fachliche Objekt; eine spätere Dokumentzuordnung muss über die bestehenden Vorgangs- und Belegverknüpfungen erfolgen.
- Das Ergebnis dieses Teilpakets ist eine Entscheidungsvorlage, keine neue externe Integration.

## Manuelle Testhinweise

- Dokumentation gegen die bestehenden Architekturregeln prüfen: keine direkten Transaktion-Beleg-Beziehungen und keine neue fachliche Grundarchitektur.
- Prüfen, dass keine DFBnet-URL, kein Login und keine externe Aktion als manueller Test vorgeschrieben wird.
- Prüfen, dass die offenen Entscheidungsfragen für eine spätere Freigabe klar erkennbar sind.

## Offene Fragen

- Welche konkreten Vereinsdaten werden für die spätere Bescheinigungserstellung benötigt und wer ist ihre verbindliche lokale Quelle?
- Sind die gewünschten Vereinsdaten in DFBnet überhaupt vollständig, fachlich maßgeblich und stabil lesbar verfügbar?
- Soll eine spätere externe Datenübernahme ausschließlich als manuell bestätigter Import erfolgen?
