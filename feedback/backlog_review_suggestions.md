# Review Backlog Suggestions

## 1. HTTP-Test für erfolgreiche Termin-Löschung ergänzen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.6

**Priorität:** mittel

**Grund:** Die erfolgreiche DELETE-Route der Termin-API soll zusätzlich per HTTP-Test abgesichert werden, damit auch der reguläre Löschpfad explizit geprüft ist.

**Feedback:**

- Erfolgreichen HTTP-Löschpfad für Termine zusätzlich absichern

## 2. Zusätzliche Testfälle für Grenzwerte bei Datum/Zeit und gemischte Zeitzonen ergänzen

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.7

**Priorität:** mittel

**Grund:** Die terminbezogene Validierung soll an den Randfällen von Datum, Uhrzeit und Zeitzonen noch robuster abgesichert werden.

**Feedback:**

- Grenzwerte bei Datum/Zeit und gemischte Zeitzonen für die Termin-API testen

## 3. Erlaubte Terminstatuswerte und Datumssemantik als zentrale Konstante oder API-Dokumentation festhalten

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.8

**Priorität:** niedrig

**Grund:** Die fachlich erlaubten Terminstatuswerte und die Datumssemantik sollen zentral nachvollziehbar dokumentiert oder als gemeinsame Konstante gepflegt werden.

**Feedback:**

- Erlaubte Terminstatuswerte und Datumssemantik zentral festhalten
- Konsistente fachliche Referenz für Terminvalidierung schaffen