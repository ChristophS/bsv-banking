# Nächstes Arbeitspaket

## Titel

Manuelles Schließen von Vorgängen im UI verständlicher machen

## Ziel

Der vorhandene manuelle Abschluss eines Vorgangs soll im Frontend klarer und leichter auffindbar werden, ohne Abschlussregeln oder andere Fachlogik zu ändern.

## Relevante Dateien

- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- banking_dashboard/static/styles.css
- banking_dashboard/server.py
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: vorhandene Vorgangs-Detailansicht und der aktuelle manuelle Abschluss-Button/Action-Handler so anpassen, dass der Abschluss klar als explizite Aktion sichtbar ist.
- banking_dashboard/static/index.html: Struktur des Vorgangs-Details oder der Aktionsleiste prüfen und eine besser auffindbare Platzierung für den manuellen Abschluss ergänzen.
- banking_dashboard/static/styles.css: minimale Layout-Anpassung für die deutlichere Platzierung des manuellen Abschluss-Buttons.
- banking_dashboard/server.py: nur falls nötig bestehende Status-API-Responses und Fehlermeldungen für manuelles Schließen prüfen, ohne die Abschlussregeln zu ändern.
- tests/test_dashboard.py: bestehende Tests für manuelles Schließen und Statuswechsel um eine UI-nahe bzw. API-seitige Absicherung ergänzen.

## Muss umgesetzt werden

- Den manuellen Abschluss-Button im Vorgangsbereich klarer positionieren oder als explizite Aktion hervorheben.
- Sicherstellen, dass der manuelle Abschluss weiterhin über die vorhandene Status-API funktioniert.
- Keine fachliche Logik für automatische Abschlussregeln ändern.

## Soll umgesetzt werden

- Eine kurze, verständliche Beschriftung für die manuelle Abschlussaktion verwenden.
- Falls bereits vorhandene Abschluss-Hinweise existieren, diese in der UI sichtbarer machen.

## Nicht Teil dieses Arbeitspakets

- Änderung der fachlichen Abschlussvoraussetzungen.
- Neuer kombinierter Flow zum Anlegen, Klassifizieren und direkten Abschließen von Vorgängen.
- Generelles UI-Redesign des Dashboards.
- Spendenbescheinigungen, Spam-Score, Mail-Verknüpfungspriorisierung oder komplexe Dokument-zu-Transaktion-Flows.

## Akzeptanzkriterien

- Ein Nutzer findet die Aktion zum manuellen Schließen eines Vorgangs ohne Suchen im UI.
- Das manuelle Schließen eines Vorgangs funktioniert weiterhin wie bisher über die vorhandene API.
- Automatische Abschlussregeln bleiben unverändert aktiv.
- Bestehende Tests zum Statuswechsel bestehen weiter.

## Hinweise für den Umsetzungs-Agenten

- Nur die Sichtbarkeit und Platzierung der vorhandenen manuellen Abschlussaktion verbessern, nicht die Statuslogik neu bauen.
- Falls der Button bisher in einer allgemeinen Aktionsgruppe untergeht, lieber die Anordnung und Beschriftung anpassen als neue Funktionen einzuführen.
- Die API-Antworten möglichst unverändert lassen, damit bestehende Clients nicht brechen.

## Manuelle Testhinweise

- Einen Vorgang im Dashboard öffnen und prüfen, ob die manuelle Abschlussaktion direkt erkennbar ist.
- Einen Vorgang manuell schließen und verifizieren, dass der Status korrekt auf abgeschlossen wechselt.
- Prüfen, dass ein über Abschlussregeln zu schließender Vorgang weiterhin unverändert behandelt wird.

## Offene Fragen

- Soll die Aktion als Button, Menüeintrag oder separate Sektion im Vorgangs-Detail erscheinen?
- Gibt es im bestehenden Layout bereits einen geeigneten Ort für eine prominentere Platzierung, ohne zusätzliche Navigation einzuführen?
