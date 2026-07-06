# Nächstes Arbeitspaket

## Titel

Browser-Test für Klick auf die Overview-Kachel „Nicht zugewiesene Dokumente“ ergänzen

## Ziel

Die bestehende Overview-Navigation im Dashboard mit einem gezielten UI-Test absichern, damit ein Klick auf die echte Kachel `unassigned_documents` weiterhin zuverlässig in den Dokumente-Bereich führt.

## Relevante Dateien

- tests/test_dashboard.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/server.py

## Wahrscheinliche Änderungsstellen

- tests/test_dashboard.py: gezielten Test ergänzen, der die Overview-Antwort mit der Kachel `unassigned_documents` nutzt und den Klickpfad bis zur erwarteten Ansicht bzw. zum erwarteten Frontend-Zustand absichert.
- banking_dashboard/static/app.js: nur falls der Test eine kleine schwer testbare Stelle offenlegt, z. B. wenn bestehende Routing-Logik ohne klar erkennbare Hook/Zuordnung arbeitet.
- banking_dashboard/static/index.html: nur falls stabile Selektoren oder bestehende DOM-Anker für die Kachel fehlen und minimal ergänzt werden müssen.

## Muss umgesetzt werden

- Einen automatisierten Test ergänzen, der explizit den Klick auf die Overview-Kachel `unassigned_documents` abdeckt statt nur allgemeine Routing-Helfer indirekt zu prüfen.
- Im Test verifizieren, dass dieser Klick in den Dokumente-/Belege-Bereich führt und nicht fälschlich in einen anderen Tab oder ohne Effekt bleibt.
- Falls nötig den Test so aufbauen, dass er gegen die echte Kachel-/Mapping-Konfiguration prüft, nicht nur gegen eine manuell aufgerufene Navigationsfunktion mit hartcodiertem Ziel.

## Soll umgesetzt werden

- Falls im Frontend noch kein stabiler Selektor/Identifier für diese Kachel existiert, minimalen testfreundlichen Anker ergänzen.
- Benennungen im Test an die tatsächlichen UI-Begriffe angleichen (`Nicht zugewiesene Dokumente`, `documents`, `belege`), damit klar bleibt, welcher Pfad abgesichert wird.

## Nicht Teil dieses Arbeitspakets

- Zentrale Vereinheitlichung aller Overview-Routen über eine neue Mapping-Tabelle.
- Fachliche Erweiterung der Dokumentzuordnung innerhalb von Vorgängen.
- Änderungen an Terminfiltern, Spendenbescheinigungen oder Mail-/Dokument-Importlogik.

## Akzeptanzkriterien

- Es existiert ein automatisierter Test, der den Klick auf die echte Overview-Kachel `unassigned_documents` abdeckt.
- Der Test schlägt fehl, wenn die Kachel nicht mehr in den Dokumente-/Belege-Bereich navigiert.
- Alle bestehenden Tests bleiben grün.
- Es werden keine fachlichen Verhaltensänderungen an Datenmodell, API oder Belegverknüpfung eingeführt.

## Hinweise für den Umsetzungs-Agenten

- In `server.py` ist die Karte bereits klar definiert; der Test sollte sich auf diese existierende Semantik stützen: `key = "unassigned_documents"`, `entity = "documents"`.
- Da die Backlog-Notiz explizit von einem Browser-Test für den Klick auf `unassigned_documents` spricht, sollte die Absicherung möglichst nah am gerenderten Frontend erfolgen und nicht nur eine Hilfsfunktion unit-testen, falls bereits Frontend-Interaktionstests in `tests/test_dashboard.py` vorhanden sind.
- Wenn das Frontend intern Begriffe wie `documents` für den Tab nutzt, aber die API `belege` liefert, im Test auf die tatsächliche sichtbare UI-Navigation zielen statt auf interne Namensdiskussionen.

## Manuelle Testhinweise

- Dashboard starten und Overview laden.
- Auf die Kachel „Nicht zugewiesene Dokumente“ klicken.
- Prüfen, dass die Dokumente-/Belege-Ansicht aktiv wird und die URL bzw. der sichtbare Bereich konsistent dazu wechselt.
- Kurz prüfen, dass andere Overview-Kacheln unverändert funktionieren.

## Offene Fragen

- Falls `tests/test_dashboard.py` derzeit keine echte Frontend-Klicksimulation enthält: soll der Test als HTML/JS-Inhaltstest innerhalb der bestehenden Testmittel umgesetzt werden oder gibt es bereits ein leichtgewichtiges DOM-/Browser-Testmuster in dieser Datei, das wiederverwendet werden kann?
