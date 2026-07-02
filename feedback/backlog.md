# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Ein-Klick-Workflow für Vorgangserstellung, Klassifikation und Abschluss

**Priorität:** hoch

**Grund:** Größerer Workflow über Vorgänge, Transaktionen und UI; nicht Teil dieses kleinen Fehlerbehebungspakets.

**Feedback:**

- Wenn ich einen Vorgang erstelle und es sind schon alle informationen da, dann will ich einen Vorgang direkt anlegen und erledigen koennen in einem Klick. Dazu gehoert auch, dass ich wenn eine Transaktion verknuepft ist bei dieser transaktion direkt die Parameter (Typ, Oberkategorie, unterkategorie, etc ) eintragen kann.

## 2. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Komplexes Fach- und UX-Thema, da Belege laut bestehender Architektur an Vorgänge und nicht direkt an Transaktionen hängen.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Ueberlege wie man geschickt damit umgehen kann

## 3. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Eigenes größeres Modul mit neuem Datenmodell- und Integrationsbedarf, nicht klein genug für das nächste Paket.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfaengern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas komplizierter, da es ueber DFBnet Vrein laeuft. ...

## 4. Dashboard-Usability schrittweise verbessern ohne Funktionsverlust

**Priorität:** mittel

**Grund:** Querschnittsthema; sollte später in kleinere konkrete UI-Pakete zerlegt werden.

**Feedback:**

- Man merkt deutlich, dass das Tool gewachsen ist. Es ist stellenweise sehr unintuitiv oder unuebersichtlich. Vlt kannst du das verbessern ohne, dass Funktionalitaeten verloren gehen.

## 5. Mail-Vorgangsfluss bei großem Datenbestand durch Suche oder Filter verbessern

**Priorität:** niedrig

**Grund:** Nützliche UX-Verbesserung, aber nicht so dringend wie die Spam-Score-Fehlerkorrektur.

**Feedback:**

- Optional Auswahl vorhandener Vorgänge bei größerem Datenbestand durch Suche, Filter oder `/api/vorgaenge/link-candidates` verbessern.
