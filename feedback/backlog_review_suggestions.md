# Review Backlog Suggestions

## 1. Split-Zuordnung auf „Nicht zugeordnet“ zurücksetzen und nach Reload prüfen

**Epic-ID:** epic-transaction-splits

**Epic-Titel:** Transaktionen in Teilbeträge und weitere Zuordnungsfälle aufteilen

**Epic-Ziel:** Transaktionen fachlich so aufteilen können, dass Teilbeträge getrennt klassifiziert und darauf aufbauende Rechnungs- und Vorgangszuordnungen unterstützt werden.

**Teilpaket:** Teil 5.1

**Priorität:** mittel

**Grund:** Der Review-Vorschlag betrifft direkt die eben umgesetzte Split-Vorgangszuordnung und sichert das fachlich wichtige Zurücksetzen auf keine Zuordnung samt Persistenz und Reload-Verhalten ab.

**Feedback:**

- Einen UI- oder HTTP-Regressionstest ergänzen, der eine vorhandene `vorgangs_id` auf „Nicht zugeordnet“ setzt, speichert und nach einem erneuten Laden die leere Auswahl bestätigt.