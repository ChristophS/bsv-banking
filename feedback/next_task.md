# Nächstes Arbeitspaket

## Titel

Vorgangs- und Beleg-API-Flows auf konsistente Eingabevalidierung und Fehlerantworten prüfen

## Epic

**Epic-ID:** epic-system-consistency

**Epic-Titel:** Systematische Qualitäts- und Konsistenzprüfung des Vereins-Finanztools

**Epic-Ziel:** Die bestehenden Funktionen, Datenflüsse und Schnittstellen des Vereins-Finanztools schrittweise auf konsistentes Verhalten, Datenintegrität und sichere lokale Testbarkeit prüfen und nachbessern.

**Teilpaket:** Teil 2.4

## Ziel

Die bestehenden lokalen API-Flows für Vorgänge und Belege sollen bei Erstellen, Ändern, Löschen und Verknüpfen einheitlich validieren, korrekte HTTP-Statuscodes liefern und verständliche Fehlerantworten zurückgeben, ohne die bestehende Vorgangs- und Verknüpfungsarchitektur umzubauen.

## Relevante Dateien

- Keine Angaben

## Wahrscheinliche Änderungsstellen

- Keine Angaben

## Muss umgesetzt werden

- Die bestehenden API-Flows für Vorgänge und Belege bei Erstellen, Ändern, Löschen und Verknüpfen fachlich prüfen.
- Erforderliche und erlaubte Eingabefelder sowie ungültige Eingaben konsistent behandeln.
- Erfolgs- und Fehlerfälle mit nachvollziehbaren und einheitlichen HTTP-Statuscodes abbilden.
- Fehlerantworten so gestalten oder korrigieren, dass Clients die Ursache verständlich erkennen können.
- Bestehende Vorgangs-, Beleg- und Verknüpfungsstrukturen weiterverwenden.

## Soll umgesetzt werden

- Passende lokale Tests für erfolgreiche, ungültige und nicht gefundene Vorgänge beziehungsweise Belege ergänzen oder korrigieren.
- Sicherstellen, dass fehlgeschlagene Änderungen keine unvollständigen Folgeänderungen oder unerwarteten Verknüpfungen hinterlassen.

## Nicht Teil dieses Arbeitspakets

- API-Flows für Transaktionen, To-Dos oder Termine; diese bleiben separaten Teilpaketen vorbehalten.
- Einführung einer direkten Ersatzbeziehung außerhalb der bestehenden Vorgangsarchitektur.
- Grundlegender Neuaufbau bestehender Tabellen, Services oder Verknüpfungen.
- Echte externe Banking-, Mail-, Microsoft-Graph- oder DFBnet-Aktionen.

## Akzeptanzkriterien

- Gültige Vorgangs- und Belegoperationen liefern konsistente Erfolgsstatuscodes und erwartbare Antwortdaten.
- Fehlende Pflichtfelder, unzulässige Werte und ungültige Verknüpfungen werden ohne unerwartete Persistenzänderung abgelehnt.
- Nicht vorhandene Vorgänge oder Belege führen zu einem konsistenten Fehlerstatus statt zu einem internen Fehler oder einer stillen Ignorierung.
- Fehlerantworten enthalten eine verständliche fachliche Meldung und folgen einem einheitlichen Format, soweit im bestehenden API-Kontext vorgesehen.
- Lösch- und Verknüpfungsoperationen respektieren die bestehenden fachlichen Integritätsregeln.
- Die relevanten lokalen Tests decken mindestens Erfolgsfall, Validierungsfehler, nicht gefundenes Objekt und Verknüpfungsfehler ab und bestehen.

## Hinweise für den Umsetzungs-Agenten

- Zuerst den vorhandenen API-Vertrag und die aktuellen Services prüfen; nur notwendige Korrekturen vornehmen.
- Technische Detailentscheidungen zu konkreten Dateien und Statuscodes anhand des bestehenden Repository-Codes treffen.
- Externe Systeme weder aufrufen noch für Tests voraussetzen.

## Manuelle Testhinweise

- Einen gültigen Vorgang und Beleg anlegen, ändern, verknüpfen und löschen.
- Jeweils eine Anfrage mit fehlendem Pflichtfeld, ungültiger ID und ungültiger Verknüpfung ausführen.
- Prüfen, dass abgelehnte Anfragen keine teilweise gespeicherten Änderungen hinterlassen.

## Offene Fragen

- Welches Fehlerantwortformat ist im bestehenden lokalen API-Vertrag bereits verbindlich und soll für die betroffenen Flows übernommen werden?
