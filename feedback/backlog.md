# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Vollständigen Bearbeitungsworkflow für Transaktions-Splitting im Dashboard ergänzen

**Priorität:** hoch

**Grund:** Bleibt als übergeordnetes Hauptthema bestehen; das nächste Arbeitspaket liefert nur die kleine technische Grundlage für Anzeige und Speicherung vorhandener Splits.

**Feedback:**

- ich benötige die Möglichkeit Transaktionen zu splitten. Da auf einer Rechnung oder innerhalb einer Transaktion Teilsummen zu Kategorie A und Teilsummen zu Kategorie B gehören können. Also ich brauche sowohl die Möglichkeit: Eine Transaktion - eien Rechnung - Teilsummen auf mehrere kategorien/Unterkategorien. Als auch die Möglichkeit Transaktion - mehrere Rechnungen und da vlt im Extremfall sogar innerhalb der Rechnungen verschiedene kateogrien/Unterkategorien

## 2. Mehrere Dokumente einer Mail unterschiedlichen Transaktionen innerhalb eines Vorgangs zuordnen

**Priorität:** mittel

**Grund:** Eigenständiger Mail- und Dokumentenworkflow außerhalb des kleinen Split-Grundlagenpakets.

**Feedback:**

- Ich habe jetzt eine Mail mit verschiedenen Dokumenten, die verschiedenen Transaktionen zugewiesen werden sollen. Das Ganze ist ein Vorgang. Überlege, wie man geschickt damit umgehen kann.

## 3. Spendenbescheinigungen mit Adressdatenbank und DFBnet-Verein-Integration konzipieren

**Priorität:** mittel

**Grund:** Eigenständiges neues Modul mit erheblichem Konzeptions- und Integrationsaufwand.

**Feedback:**

- Spendenbescheinigung: baue eine Adressdatenbank auf mit allen bisherigen Spendenempfängern. Dann auch eine automatische Erzeugung der Spendenbescheinigung. Das wird etwas kompliziert, da es über DFBnet Verein läuft.

## 4. Expliziten Migrationstest für Schema-Version 13 auf 14 ergänzen

**Priorität:** niedrig

**Grund:** Sinnvoll, aber nachrangig gegenüber der nutzbaren Split-Grundlage im Dashboard.

**Feedback:**

- Review-Hinweis zur Absicherung der Migration auf `transaction_splits`.

## 5. Prüfen, ob TransactionSplit created_at und updated_at enthalten soll

**Priorität:** niedrig

**Grund:** Modellkonsistenzfrage, die nach der ersten nutzbaren Split-Verwendung separat geklärt werden kann.

**Feedback:**

- Review-Hinweis zur Vollständigkeit des Datentyps gegenüber der Persistenz.