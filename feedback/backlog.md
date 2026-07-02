# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Generischen Ein-Klick-Workflow für manuelle Vorgangserstellung, Klassifikation und Abschluss ausbauen

**Priorität:** hoch

**Grund:** Umfasst einen breiteren manuellen Workflow mit zusätzlicher Klassifikation im selben Schritt und geht über den kleinen Mail-Import-Zuschnitt hinaus.

**Feedback:**

- Wenn ich einen Vorgang erstelle und es sind schon alle informationen da, dann will ich einen Vorgang direkt anlegen und erledigen koennen in einem Klick. Dazu gehoert auch, dass ich wenn eine Transaktion verknuepft ist bei dieser transaktion direkt die Parameter (Typ, Oberkategorie, unterkategorie, etc ) eintragen kann.

## 2. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Eigenes fachlich komplexes Thema mit mehreren Zuordnungsfällen; nicht Teil des kleinen Sofort-Abschluss-Pakets.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Ueberlege wie man geschickt damit umgehen kann

## 3. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Größeres, eigenständiges Modul mit zusätzlichem Datenmodell- und Integrationsbedarf.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfaengern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas komplizierter, da es ueber DFBnet Vrein laeuft. ...

## 4. Dashboard-Usability schrittweise verbessern ohne Funktionsverlust

**Priorität:** mittel

**Grund:** Querschnittsthema, das in mehrere konkrete UX-Pakete zerlegt werden sollte.

**Feedback:**

- Man merkt deutlich, dass das Tool gewachsen ist. Es ist stellenweise sehr unintuitiv oder unuebersichtlich. Vlt kannst du das verbessern ohne, dass Funktionalitaeten verloren gehen.

## 5. Persistierten Vorgang nach fehlgeschlagenem Mail-Sofortabschluss zusätzlich prüfen

**Priorität:** niedrig

**Grund:** Nicht-blockierende Review-Regression, die den Fehlerfall nach dem fehlgeschlagenen Sofort-Abschluss noch explizit absichert.

**Feedback:**

- Nach einem fehlgeschlagenen Sofort-Abschluss beim Mail-Import den persistierten Vorgang erneut laden und explizit prüfen, dass er nicht `abgeschlossen` ist.