# Backlog

Diese Punkte wurden nicht in das nächste Arbeitspaket aufgenommen und sollen später separat bearbeitet werden.

## 1. Mail-UI: Sehr kleine positive Spam-Scores verständlicher darstellen

**Priorität:** mittel

**Grund:** Reines Anzeige-Thema und nicht nötig, um die eigentliche Robustheit der Spam-Normalisierung und den Fallback zu beheben.

**Feedback:**

- Falls die UI positive Werte kleiner als 0,5 Prozent durch Rundung als 0 % anzeigt, eine reine Anzeigeverbesserung vornehmen, damit echte kleine Scores nicht wie ein technischer 0-Fehler wirken.

## 2. Spam-Score-Systemprompt für stabileres JSON-Schema präzisieren

**Priorität:** mittel

**Grund:** Kann die Robustheit verbessern, ist aber nicht zwingend notwendig für das kleine Kernpaket zur Fallback-Korrektur.

**Feedback:**

- Das OpenAI-Systemprompt in OpenAISpamScorer.score präzisieren, damit das Modell ein stabiles JSON-Schema liefert, z. B. probability als Zahl zwischen 0 und 1 sowie reasons als Liste kurzer Strings.
