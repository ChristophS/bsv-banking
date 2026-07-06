# Nächstes Arbeitspaket

## Titel

Dashboard-Kachel „Nicht zugewiesene Dokumente“ auf den Belege-Bereich routen

## Ziel

Die Übersichts-Kachel für nicht zugewiesene Dokumente soll beim Klick den bestehenden Belege-/Dokumente-Bereich öffnen statt fälschlich in einen anderen Bereich wie Termine zu navigieren.

## Relevante Dateien

- banking_dashboard/server.py
- banking_dashboard/static/app.js
- banking_dashboard/static/index.html
- tests/test_dashboard.py

## Wahrscheinliche Änderungsstellen

- banking_dashboard/static/app.js: das Mapping für Overview-Karten bzw. den Klick-Handler so anpassen, dass `entity: documents` oder `key: unassigned_documents` den Belege-Bereich öffnet.
- banking_dashboard/static/index.html: nur falls für den Belege-Bereich ein stabiler Tab-/Section-Identifier fehlt oder die Navigation einen passenden Anker benötigt.
- tests/test_dashboard.py: bestehende Dashboard-Tests um die korrekte Zuordnung der Dokumenten-Kachel ergänzen.
- banking_dashboard/server.py: nur prüfen, ob die bereits gelieferte Overview-Konfiguration unverändert konsistent bleibt.

## Muss umgesetzt werden

- Ursache für die falsche Navigation der Karte `unassigned_documents` im Frontend ermitteln und das vorhandene Mapping korrigieren.
- Sicherstellen, dass Karten mit `entity: documents` den bestehenden Belege-/Dokumente-Bereich öffnen.
- Falls `key` und `entity` unterschiedlich behandelt werden, die spezifische Behandlung für `unassigned_documents` repo-konsistent ergänzen.
- Automatisierte Tests so anpassen oder ergänzen, dass die gewünschte Zuordnung abgesichert ist.

## Soll umgesetzt werden

- Wenn die Mapping-Logik an mehreren Stellen ähnlich dupliziert ist, die Korrektur an der zentralsten vorhandenen Stelle vornehmen.
- Prüfen, ob nach dem Öffnen des Belege-Bereichs bereits ein vorhandener Filter oder Fokus für ungeordnete Belege genutzt werden kann, ohne neue UI-Struktur einzuführen.

## Nicht Teil dieses Arbeitspakets

- Ein neuer eigener Top-Level-Reiter nur für Belege/Dokumente
- Mehrfachzuordnung einzelner Mail-Anhänge zu unterschiedlichen Transaktionen innerhalb eines Vorgangs
- Spendenbescheinigungen mit Adressdatenbank oder DFBnet-Integration
- Größere Terminfilter-Überarbeitung

## Akzeptanzkriterien

- Die Overview-API liefert weiterhin eine Karte mit `key = unassigned_documents` und `entity = documents`.
- Ein Klick auf die Kachel „Nicht zugewiesene Dokumente“ öffnet den bestehenden Belege-/Dokumente-Bereich.
- Andere Overview-Kacheln verhalten sich unverändert.
- Die angepassten oder neuen Tests decken die Dokumenten-Zuordnung ab und bleiben grün.

## Hinweise für den Umsetzungs-Agenten

- Im Backend ist die Overview-Card bereits als `entity: documents` modelliert; der Fehler liegt sehr wahrscheinlich im Frontend-Mapping in `static/app.js`.
- Vorhandene Beleg-Endpunkte unter `/api/belege` sollen weiterverwendet werden; keine neue Dokumentenlogik bauen.
- Die Korrektur soll minimal sein und keine neue Navigationsarchitektur einführen.

## Manuelle Testhinweise

- Dashboard starten und die Overview laden.
- Die Kachel „Nicht zugewiesene Dokumente“ anklicken.
- Prüfen, dass der Belege-/Dokumente-Bereich geöffnet wird.
- Kurz gegenprüfen, dass andere Karten weiterhin in ihre bisherigen Bereiche führen.

## Offene Fragen

- Ob der Belege-Bereich im Frontend bereits einen separaten Tab oder nur einen Abschnitt innerhalb eines Sammelbereichs nutzt, muss anhand der vorhandenen `app.js`-Struktur konkret geprüft werden.
- Falls es bereits einen Fokus auf ungeordnete Belege gibt, reicht für dieses Paket das Öffnen des korrekten Bereichs ohne zusätzliche Filterlogik.
