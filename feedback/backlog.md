# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere fachliche Erweiterung der bestehenden Vorgang-/Dokument-Zuordnung mit Datenmodell- und UI-Auswirkungen; nicht klein genug für das jetzt gewählte Refactoring-Paket.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Ueberlege wie man geschickt damit umgehen kann

## 2. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Eigenständiges größeres Modul mit Integrations- und Datenmodellfragen; derzeit nicht klein und risikoarm genug.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfaengern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es ueber DFBnet Verein laeuft.

## 3. Spezifischere Terminfilter für anstehende und nicht zugewiesene Termine prüfen

**Priorität:** niedrig

**Grund:** Eigenes UI-/Filter-Thema, aber ohne geladenen spezifischen Termin-Kontext derzeit weniger geeignet als das kleine Overview-Refactoring.

**Feedback:**

- Spezifischere Terminfilter für „anstehende Termine“ und „nicht zugewiesene Termine“ prüfen

## 4. Browser-Ressourcen im neuen Playwright-Test optional per try/finally schließen

**Priorität:** niedrig

**Grund:** Nicht-blockierender Test-Cleanup-Hinweis; kleiner, aber weniger nutzwirksam als das jetzt gewählte UI-Refactoring.

**Feedback:**

- Review-Hinweis: Browser-Ressourcen im neuen Playwright-Test optional per try/finally schließen

## 5. Bei künftig vorhandenem stabilem Belege-/Dokumenten-Selektor den Zielbereich noch spezifischer absichern

**Priorität:** niedrig

**Grund:** Abhängig von künftig stabilerer UI-Struktur; aktuell kein eigenständiges vorrangiges Arbeitspaket.

**Feedback:**

- Review-Hinweis: Bei künftig vorhandenem stabilem Belege-/Dokumenten-Selektor den Zielbereich noch spezifischer absichern
