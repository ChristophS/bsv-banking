# Review Report

## Ergebnis

**Accepted:** true

**Needs more context:** false

## Zusammenfassung

Die Umsetzung erfüllt die Muss-Anforderungen. Fehlende externe Mailobjekte werden über ExternalMailNotFoundError klassifiziert, Graph-404/ErrorItemNotFound sowie Outlook-MAPI_E_NOT_FOUND werden typbasiert übersetzt, generische Outlook- und Mailbox-Fehler bleiben unterscheidbar. Der Fehlertyp wird über die Outlook-Prozessgrenze transportiert. Geeignete Mock-/Fake-Tests decken die Erkennung und Abgrenzung ab; bestehende vorgangsbasierte Mailstrukturen bleiben unverändert.

## Review-Ergebnis

**Akzeptiert.**

### Erfüllte Anforderungen

- `ExternalMailNotFoundError` ist als expliziter, stabil auswertbarer Fehlertyp vorhanden.
- Microsoft-Graph-Fehler werden anhand des HTTP-Status 404 oder des strukturierten Graph-Codes `ErrorItemNotFound` in diesen Fehlertyp übersetzt.
- Outlook klassifiziert das stabile HRESULT `MAPI_E_NOT_FOUND` (`0x8004010F`) ohne Auswertung instabiler Fehlermeldungstexte.
- Andere Outlook-COM-Fehler werden weiterhin als generischer `MailIntegrationError` behandelt.
- Der explizite Fehlertyp wird über die Outlook-Worker-Prozessgrenze mit einem eigenen Status erhalten.
- Die Synchronisationslogik wertet beim Stale-Mail-Verhalten ausschließlich `ExternalMailNotFoundError` aus. Generische Fehler mit ähnlichen Texten, darunter `ErrorItemNotFound`, entfernen keinen lokalen Eintrag.
- Vorhandene Mail-, Vorgangs- und Verknüpfungsstrukturen wurden nicht umgangen oder neu aufgebaut.
- Tests verwenden ausschließlich Mocks, Fakes und simulierte Fehler; echte externe Mailaktionen finden nicht statt.

### Testabdeckung

Die ergänzten Tests belegen:

- explizites Stale-Verhalten bei `ExternalMailNotFoundError`,
- gegenteiliges Verhalten bei einem generischen Fehler mit fehlend wirkendem Meldungstext,
- Graph-404-Übersetzung zu `ExternalMailNotFoundError`,
- Outlook-Erkennung des fehlenden Objekts anhand des HRESULT,
- Abgrenzung eines anderen Outlook-HRESULTs als generischer `MailIntegrationError`.

Der gemeldete GitHub-Compare ist brauchbar (`ahead_by: 2`, `behind_by: 0`), und es gibt keine Abweichungen zwischen Runner- und GitHub-Änderungspfaden.

### Nicht blockierende Hinweise

- Ein zusätzlicher Test für `ErrorItemNotFound` bei einem Nicht-404-Graph-Status wäre sinnvoll, aber für die Freigabe nicht erforderlich.
- Die Outlook-HRESULT-Konstante könnte noch etwas stärker dokumentiert werden.
