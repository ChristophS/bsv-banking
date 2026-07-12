# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Änderungen erfüllen die zentralen Anforderungen des Arbeitspakets. Vorgangs- und Beleg-Verknüpfungen validieren Eingaben konsistenter, unterscheiden Validierungsfehler von unbekannten Fachobjekten und verwenden das bestehende JSON-Fehlerformat mit HTTP 400 beziehungsweise 404. Die Änderungen bleiben innerhalb der vorhandenen Architektur; der GitHub-Compare ist vollständig und der gemeldete Testlauf erfolgreich.

# Review

## Entscheidung

**Akzeptiert.**

## Geprüfte Anforderungen

- Die Vorgangs-Payload validiert Textfelder wie `title`, `description` und `vorgangstyp` jetzt explizit und wandelt fremde Datentypen nicht mehr stillschweigend in Text um.
- Verknüpfungslisten für Vorgänge akzeptieren nur Text-IDs und lehnen Zahlen, `null` und andere Datentypen mit HTTP 400 ab.
- Die Beleg-Verknüpfungs-API verlangt eine nichtleere Zeichenkette als `vorgangs_id`.
- Das Verknüpfen und Aufheben einer Beleg-Verknüpfung prüft sowohl Beleg als auch Vorgang. Unbekannte Fachobjekte führen zu HTTP 404.
- Das bestehende Fehlerformat `{"error": "..."}` und die vorhandene HTTP-Konvention für Validierungs- und Lookup-Fehler werden beibehalten.
- Die Änderungen verwenden weiterhin die bestehenden Tabellen, Store-Methoden und N:M-Verknüpfungen.

## Persistenz und Integrität

Die Validierungen erfolgen vor den relevanten Schreiboperationen. Bei ungültigen oder unbekannten Verknüpfungen werden keine neuen Zuordnungen angelegt. Die ergänzten Tests prüfen außerdem, dass abgelehnte Erstellungs- und Verknüpfungsanfragen keine teilweise persistierten Daten hinterlassen.

## Tests

Die ergänzten HTTP-Regressionstests decken ungültige Vorgangseingaben, unbekannte Vorgänge bei Änderung und Löschung sowie ungültige und unbekannte Beleg-Verknüpfungen ab. Laut Implementierungsbericht bestehen 129 Tests; sechs optionale Browser-Tests sind übersprungen. Das ist für dieses lokale API-Arbeitspaket plausibel, da keine externen Dienste benötigt werden.

## Scope und Branch-Zustand

Es wurden nur der API-Store, die zugehörigen Tests und der Implementierungsbericht geändert. Es gibt keine Änderungen am Datenmodell, an externen Integrationen oder an UI-Komponenten. Der Branch ist laut Compare einen Commit vor `main`, nicht hinter `main`, und weist keine fehlenden oder zusätzlichen Compare-Dateien auf.

## Nicht blockierende Hinweise

Für eine noch vollständigere Vertragsabdeckung wären explizite Tests der erfolgreichen Erstellungs-, Änderungs- und Löschoperationen sowie der ungültigen Beleg-ID bei der POST-Verknüpfung sinnvoll. Diese Ergänzungen sind jedoch kein Blocker, da die bestehenden Tests und die geprüfte Implementierung die zentralen Akzeptanzkriterien abdecken.
