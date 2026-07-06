# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere fachliche Erweiterung über Mail-Import, Dokumenthandling, Vorgangsdetail-UI und bestehende Verknüpfungslogik; nicht als kleines, kontrollierbares Arbeitspaket abgrenzbar.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 2. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Eigenständiges größeres Modul mit zusätzlichem Datenmodell- und Integrationsbedarf; nicht Teil des kleinen nächsten Arbeitspakets.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.

## 3. Zeitlogik für `beginnt_am` bei ISO-Zeitpunkten prüfen

**Priorität:** niedrig

**Grund:** Nicht-blockierender Hinweis aus dem Review; die aktuelle Logik nutzt weiterhin nur den Datumsteil und unterscheidet innerhalb des Tages nicht per Uhrzeit.

## 4. Exakten Terminlisten-Filter für nicht zugewiesene Termine prüfen

**Priorität:** niedrig

**Grund:** Nicht-blockierender Hinweis aus dem Review; der Kartenklick führt weiterhin in die allgemeine Terminansicht mit bestehendem Filter statt in eine explizit auf unzugewiesene Termine eingeschränkte Ansicht.
