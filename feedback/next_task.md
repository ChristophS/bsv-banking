# Nächstes Arbeitspaket

## Titel

Dashboard-Oberfläche für manuelle Saldo-Korrekturen ergänzen

## Epic

**Epic-ID:** epic-balance-correction

**Epic-Titel:** Manuelle Behandlung abweichender Kontostandsanker

**Epic-Ziel:** Abweichungen zwischen exportierten Bank-Salden und importierten Umsatz-Saldoketten kontrolliert, nachvollziehbar und ohne Veränderung von Originaldaten behandeln.

**Teilpaket:** Teil 2

## Ziel

Kassierer können vorhandene manuelle Saldo-Korrekturen lokal nachvollziehen und nach bewusster Eingabe eine neue Korrektur mit Konto, Stichtag, Centbetrag und Begründung anlegen.

## Relevante Dateien

- banking_dashboard/static/index.html
- banking_dashboard/static/app.js
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py
- transaction_store/database.py

## Wahrscheinliche Änderungsstellen

- Dashboard-Bereich für Kontostände oder Transaktionen in banking_dashboard/static/index.html
- Frontend-Lade-, Formular-, Validierungs- und Fehlerrückmeldelogik in banking_dashboard/static/app.js
- Darstellung von Korrekturhistorie, Warnhinweisen und Formularzuständen in banking_dashboard/static/styles.css
- Bestehende Endpunkte GET/POST /api/balance-corrections und gegebenenfalls eine ausschließlich lesende Kontoliste im banking_dashboard/server.py
- API- und Dashboard-Tests für Saldo-Korrekturen in tests/test_dashboard.py

## Muss umgesetzt werden

- Eine klar abgegrenzte lokale Dashboard-Ansicht für vorhandene manuelle Saldo-Korrekturen bereitstellen.
- Je Korrektur mindestens Konto, Anbieter beziehungsweise Kontobezeichnung soweit verfügbar, Stichtag, Betrag, Begründung, Erstellzeitpunkt und den Hinweis auf die manuelle Prüfung anzeigen.
- Ein Formular für neue Korrekturen bereitstellen, das account_id, balance_minor, balance_as_of und reason an den bestehenden POST-Endpunkt sendet.
- Für Beträge die bereits vorhandene Cent-basierte API-Semantik verwenden und vor dem Absenden nachvollziehbar validieren.
- Vor dem Speichern deutlich machen, dass eine Korrektur nur nach manueller Prüfung eines Kontoauszugs oder Bankstands angelegt werden darf und keine Originaltransaktionen verändert.
- Erfolgs- und Fehlerzustände im Dashboard sichtbar darstellen und die Liste nach erfolgreichem Speichern aktualisieren.
- Bestehende Korrekturen nur anzeigen und neue anlegen; keine Widerrufs-, Lösch- oder Ersetzungsfunktion vorziehen.
- Automatisierte Tests für den lokalen API- und UI-nahen Flow ergänzen, ohne Datenbanken, Bankzugriffe oder andere externe Dienste produktiv zu verwenden.

## Soll umgesetzt werden

- Die Korrekturansicht bei fehlenden Einträgen mit einem verständlichen Leerzustand versehen.
- Die Kontenauswahl anhand bereits lokal bekannter Konten verständlich beschriften, ohne neue Kontostammdaten zu erzeugen.
- Serverseitige Fehlerantworten des bestehenden Endpunkts im Frontend unverändert verständlich weitergeben.
- Die Darstellung so platzieren, dass sie im bestehenden Kontostands- oder Transaktionsworkflow auffindbar bleibt.

## Nicht Teil dieses Arbeitspakets

- Widerruf, Löschung oder Ersatz bestehender manueller Saldo-Korrekturen.
- Eine getrennte fachliche Bestätigung nach dem Anlegen einer Korrektur.
- Änderungen an Import-, Saldenketten- oder Archivierungslogik.
- Automatische Korrekturen, Bankabgleiche oder externe Banking-Aktionen.
- Umbau der Vorgangs-, Transaktions-, Beleg- oder Verknüpfungsarchitektur.

## Akzeptanzkriterien

- Das Dashboard lädt vorhandene Korrekturen über GET /api/balance-corrections und zeigt deren wesentliche Werte nachvollziehbar an.
- Ein Nutzer kann eine neue Korrektur mit gültigem Konto, ganzzahligem Centbetrag, ISO-Stichtag und nicht leerer Begründung über das Dashboard anlegen.
- Nach erfolgreichem POST /api/balance-corrections erscheint die neu angelegte Korrektur ohne manuellen Seitenreload in der Ansicht.
- Ungültige oder unvollständige Eingaben werden vor dem Absenden oder anhand der API-Antwort klar angezeigt; es wird keine scheinbar erfolgreiche Korrektur dargestellt.
- Die Oberfläche weist sichtbar darauf hin, dass die Korrektur eine bewusste lokale, manuell geprüfte Maßnahme ist und Originaldaten nicht verändert.
- Bestehende Korrekturen können in diesem Paket nicht gelöscht, überschrieben, widerrufen oder automatisch bestätigt werden.
- Die ergänzten Tests laufen ohne echte Bankzugriffe, Credentials, Browserprofile oder produktive Laufzeitdaten.

## Hinweise für den Umsetzungs-Agenten

- Die vorhandenen Funktionen DashboardDataStore.list_balance_corrections und DashboardDataStore.create_balance_correction sowie die Endpunkte GET/POST /api/balance-corrections wiederverwenden.
- Keine direkte fachliche Beziehung zwischen Korrektur und Belegen, Mails oder Transaktionen einführen; die Korrektur bleibt ein lokaler Saldoanker gemäß bestehender Persistenzlogik.
- Für den Formulardatentransfer ausschließlich JSON mit den bestehenden Pflichtfeldern verwenden.
- Betragsdarstellung und Eingabe eindeutig dokumentieren: API-Werte sind Cent als Integer; eine eventuell nutzerfreundliche Euro-Eingabe muss vor dem Request verlustfrei in Cent umgerechnet und gegen Dezimalfehler abgesichert werden.
- Die bestehende Sicherheits- und Fehlerbehandlungsstruktur des lokalen Dashboards beibehalten.

## Manuelle Testhinweise

- Mit einer ausschließlich temporären Testdatenbank das Dashboard starten und den Leerzustand der Korrekturansicht prüfen.
- Eine gültige lokale Korrektur für ein vorhandenes Testkonto anlegen und prüfen, dass Betrag, Stichtag, Begründung und Prüfhinweis korrekt erscheinen.
- Ungültige Fälle prüfen: fehlendes Konto, nicht ganzzahliger Centwert beziehungsweise ungültige Betragseingabe, ungültiges Datum und leere Begründung.
- Prüfen, dass kein Browser für Banking, kein externer Dienst und keine produktiven Daten benötigt werden.
- Prüfen, dass vorhandene Korrekturen in diesem Paket weder gelöscht noch verändert werden können.

## Offene Fragen

- Soll die Bedienoberfläche Beträge ausschließlich als Cent anzeigen oder Euro mit klarer, verlustfreier Umrechnung in Cent anbieten?
- Soll die Kontoliste für die Auswahl über einen kleinen neuen lesenden API-Endpunkt bereitgestellt werden oder reicht die im bestehenden Kontostands-Payload vorhandene Kontoliste aus?
