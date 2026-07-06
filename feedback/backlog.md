# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Größere fachliche Erweiterung der bestehenden Vorgang-/Dokument-Zuordnung und deutlich größer als das jetzt gewählte kleine Test-Arbeitspaket.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Ueberlege wie man geschickt damit umgehen kann

## 2. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Eigenständiges größeres Modul mit Datenmodell- und Integrationsfragen; nicht klein genug für den nächsten Schritt.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfaengern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es ueber DFBnet Verein laeuft.

## 3. Spezifischere Terminfilter für anstehende und nicht zugewiesene Termine prüfen

**Priorität:** niedrig

**Grund:** Eigenes UI-/Filter-Thema; bleibt außerhalb der gezielten Absicherung des aktuellen Overview-Klickpfads.

**Feedback:**

- Spezifischere Terminfilter für „anstehende Termine“ und „nicht zugewiesene Termine“ prüfen

## 4. Overview-Routing bei weiteren Kacheln über eine zentrale Mapping-Tabelle vereinfachen

**Priorität:** niedrig

**Grund:** Wartbarkeits-Refaktor statt unmittelbarer Fehlerbehebung; sollte separat nach der konkreten Absicherung des Klickpfads erfolgen.

**Feedback:**

- Review-Empfehlung zur Vereinfachung des Overview-Routings über eine zentrale Mapping-Tabelle

## 5. Browser-Ressourcen im neuen Playwright-Test optional per `try/finally` schließen

**Priorität:** niedrig

**Grund:** Nicht-blockierender Stabilitäts-/Cleanup-Hinweis aus dem Review.

## 6. Bei künftig vorhandenem stabilem Belege-/Dokumenten-Selektor den Zielbereich noch spezifischer absichern

**Priorität:** niedrig

**Grund:** Nicht-blockierender Hinweis zur künftigen Präzisierung der UI-Absicherung.