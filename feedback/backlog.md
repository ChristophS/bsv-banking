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

**Grund:** Weiterhin separater, nicht-blockierender Prüfpunkt; bewusst nicht mit dem kleinen Filterpaket vermischen.

**Feedback:**

- Vorhandener Backlog-Punkt: Zeitlogik für `beginnt_am` bei ISO-Zeitpunkten prüfen

## 4. Spezialfilter in der Terminansicht sichtbar machen

**Priorität:** niedrig

**Grund:** Nicht-blockierender UX-Hinweis aus dem Review; verbessert Nachvollziehbarkeit des aktiven Filters.

**Feedback:**

- Aktiven Spezialfilter in der Terminansicht sichtbar machen, z. B. als Hinweis-Badge „Nicht zugewiesene anstehende Termine“ mit Zurücksetzen-Aktion.

## 5. Spezialfilter bei normaler Termin-Navigation zurücksetzen testen

**Priorität:** niedrig

**Grund:** Zusätzlicher nicht-blockierender Frontend-Test aus dem Review; prüft das Zurücksetzen des Spezialfilters bei Standard-Navigation.

**Feedback:**

- Ergänzenden Frontend-Test hinzufügen, der prüft, dass der Spezialfilter nach normaler Termin-Tab-Navigation oder allgemeiner Termin-Route wieder deaktiviert ist.
