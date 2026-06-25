# Read-only Onlinebanking Login-Test

Dieses eigenstaendige Python-Projekt oeffnet einen sichtbaren Chromium-Browser,
prueft den Login inklusive einer gegebenenfalls erforderlichen manuellen MFA
und kann rohe CSV-Umsatzdateien fuer freigegebene Volksbank- und
Sparkassenkonten herunterladen.

Im konfigurierten `env`-Modus liest der Code Benutzerkennung und Passwort aus
einer lokalen `.env`-Datei, fuellt ausschliesslich die Loginfelder und sendet
das Loginformular ab. Er bestaetigt keine MFA-Abfrage und enthaelt keine
Ueberweisungs- oder sonstige schreibende Banking-Funktion. CSV-Dateien werden
nur heruntergeladen, nicht eingelesen oder verarbeitet.

## Voraussetzungen

- Python 3.9 oder neuer
- Windows, macOS oder Linux mit grafischer Oberflaeche
- Offizielle HTTPS-Login-URL der Bank
- Stabiler CSS-Selektor oder URL-Regulaerausdruck fuer die Seite nach dem Login

## Installation

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m playwright install chromium
```

macOS/Linux:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m playwright install chromium
```

## Konfiguration

Lokale Konfiguration aus der Vorlage erzeugen:

```powershell
.\.venv\Scripts\python main.py --init-config
```

Danach `config.toml` bearbeiten:

```toml
[bank]
provider = "volksbank"
login_url = "https://offizielle-bank.example/login"

[credentials]
mode = "env"
env_file = "D:/.secrets/bsv_banking.env"
username_variable = "VOLKSBANK_USERNAME"
password_variable = "VOLKSBANK_PASSWORD"
username_selector = "#vrNetKey"
password_selector = "#pin"
submit_selector = "button[type='submit']"

[export]
format = "CSV"
period = "FROM_SEARCH"
output_dir = ".runtime/exports"
download_timeout_seconds = 60

[detection]
success_selector = "main[data-testid='account-overview']"
success_url_pattern = '^https://offizielle-bank\.example/(overview|accounts)'
timeout_seconds = 300
```

Fuer die Sparkasse wird eine separate Konfiguration mit getrenntem
Browserprofil angelegt:

```powershell
.\.venv\Scripts\python main.py --init-sparkasse-config --config config.sparkasse.local.toml
```

Die Vorlage [config.sparkasse.example.toml](config.sparkasse.example.toml)
enthaelt bereits die drei freigegebenen Sparkassenkonten und das feste
Exportformat `Excel (CSV-MT940)`.

Mindestens eines der drei Erfolgskriterien ist erforderlich:

- `success_selector`: bevorzugt ein stabiles `data-testid`, eine feste ID oder
  ein bankspezifisches ARIA-/Layout-Merkmal der Konto-Uebersicht.
- `success_url_pattern`: Regulaerausdruck, der nur auf authentifizierte Seiten
  passt. Punkte im Hostnamen muessen mit `\.` maskiert werden.
- `success_text_pattern`: Regulaerausdruck fuer einen stabilen Text der
  authentifizierten Konto-Uebersicht, beispielsweise eine freigegebene IBAN.

Die externe Datei `D:\.secrets\bsv_banking.env` muss enthalten:

```dotenv
VOLKSBANK_USERNAME=...
VOLKSBANK_PASSWORD=...
SPARKASSE_USERNAME=...
SPARKASSE_PASSWORD=...
```

Keine Credential-Werte, MFA-Codes oder Session-Token in `config.toml`
eintragen. Mit `mode = "manual"` wird die `.env`-Datei nicht gelesen und die
Eingabe bleibt vollstaendig manuell.

Konfiguration ohne Browserstart pruefen:

```powershell
.\.venv\Scripts\python main.py --validate-config
.\.venv\Scripts\python main.py --config config.sparkasse.local.toml --validate-config
```

Im `env`-Modus prueft dieser Befehl auch, ob die Secrets-Datei und beide
Variablen vorhanden und nicht leer sind. Werte werden nicht ausgegeben.

## Start und Testablauf

```powershell
.\.venv\Scripts\python main.py
```

1. Chromium oeffnet die konfigurierte Loginseite sichtbar.
2. Im `env`-Modus werden nur Benutzerkennung und Passwort beziehungsweise
   Anmeldename und Online-Banking-PIN lokal eingesetzt. Der Sparkassen-Login
   erfolgt zweistufig ueber `Weiter` und `Anmelden`. Es gibt keine
   automatischen Login-Wiederholungen.
   Wenn die erwartete Loginmaske nicht eindeutig erkannt wird, bedient das
   Programm keine Felder und fordert stattdessen zum manuellen Login auf.
3. MFA manuell am Handy ueber das von der Bank vorgesehene Verfahren
   bestaetigen.
4. Das Programm wartet, bis Selektor oder URL-Muster fuer mindestens zwei
   Sekunden stabil erkannt werden.
5. Nach Login-Test oder CSV-Export meldet das Programm die Sitzung ab und
   wartet auf die bankspezifische Logout-Bestaetigung. Bei einem unbekannten
   Abmeldefenster muss die Abmeldung manuell im Browser abgeschlossen werden.
6. Erfolg wird erst nach bestaetigter Abmeldung im Terminal und in der
   lokalen Logdatei vermerkt.
7. Bei Timeout oder Browserfehler wird vor dem Schliessen ein Screenshot
   gespeichert.

Der Browser wird erst nach dem Abmeldeversuch geschlossen. Im normalen
Login-Test erfolgt nach dem Loginformular nur die abschliessende Abmeldung.
Der Exportmodus bedient nur Kontenauswahl, Export und Logout;
Ueberweisungs- oder sonstige schreibende Banking-Funktionen existieren nicht.

## CSV-Export

```powershell
.\.venv\Scripts\python main.py --export-csv
```

Dieser Aufruf exportiert mit `config.toml` die vier Volksbankkonten:

| Konto | Freigegebene IBAN |
| --- | --- |
| Hauptkonto | `DE31 3846 2135 0101 2060 17` |
| Ruecklagen | `DE09 3846 2135 0101 2060 25` |
| Ausstattung | `DE98 3846 2135 0103 0380 14` |
| Sparkonto | `DE25 3846 2135 0101 2064 16` |

Die Sparkassenkonten werden mit der separaten Konfiguration exportiert:

```powershell
.\.venv\Scripts\python main.py --config config.sparkasse.local.toml --export-csv
```

| Konto | Freigegebene IBAN | Zieldatei |
| --- | --- | --- |
| Veranstaltungen: Sichteinlagen | `DE29 3845 0000 0000 3592 32` | `veranstaltungen.csv` |
| Jugend: Sichteinlagen - Abt. Jugendfussball | `DE71 3845 0000 0000 8164 13` | `jugend.csv` |
| Vereinsheim: Sichteinlagen - Vereinsheim | `DE85 3845 0000 0001 0135 56` | `vereinsheim.csv` |

Vor jedem Kontoaufruf muessen Name und vollstaendige normalisierte IBAN aus
der jeweiligen `[[accounts]]`-Allowlist uebereinstimmen. Andere Konten werden
nicht exportiert.

Die Parameter sind fest validiert:

- Volksbank: Format `CSV`, Zeitraum `FROM_SEARCH` beziehungsweise **Aus Suche**
- Sparkasse: Format **Excel (CSV-MT940)**, vorhandener Zeitraum bleibt
  unveraendert (`CURRENT_VIEW`)

Jeder Lauf erzeugt unter dem konfigurierten Exportverzeichnis einen neuen
Zeitstempelordner. Die Sparkassen-Vorlage verwendet
`.runtime/exports/sparkasse/`. Zusaetzlich zu den CSV-Dateien wird der
aktuelle Kontostand jedes freigegebenen Kontos aus der Konto-Uebersicht in
`account_balances.json` gespeichert.

## Transaktionsarchiv und Datenbank

Jeder erfolgreiche `--export-csv`-Lauf wird nach der bestaetigten Abmeldung
automatisch archiviert, normalisiert und in die gemeinsame Datenbank
importiert. Bereits vorhandene Exportlaeufe koennen jederzeit idempotent
nachgezogen werden:

```powershell
.\.venv\Scripts\python main.py --import-transactions
```

Historische Verzeichnisse mit gemischten Dateien koennen rekursiv durchsucht
werden. Unterstuetzte Volksbank- und Sparkassen-CSV-Ausgaben werden anhand
ihres Schemas erkannt; andere Dateien bleiben unangetastet:

```powershell
.\.venv\Scripts\python main.py --import-directory "C:\Pfad\Zum\Ordner"
```

Der Import validiert zuerst alle erkannten Dateien, Saldenketten und
ueberlappenden Saldo-Beobachtungen. Erst danach werden die Originaldateien
archiviert und dedupliziert importiert. Wiederholte Aufrufe sind idempotent.

Standardmaessig werden `config.toml` und, falls vorhanden,
`config.sparkasse.local.toml` verwendet. Weitere Quellen koennen explizit
angegeben werden:

```powershell
.\.venv\Scripts\python main.py --import-transactions `
  --source-config config.toml `
  --source-config config.sparkasse.local.toml
```

Die sensiblen Daten liegen unter `data/transactions/`:

```text
data/transactions/
  archive/
    raw/<bank>/<jahr>/<monat>/<exportlauf>/*.csv
    manifests/<bank>/<jahr>/<monat>/<exportlauf>.json
  normalized/
    runs/<bank>/<jahr>/<monat>/<exportlauf>.csv
    transactions.csv
  database/
    transactions.sqlite3
    rules.sqlite3
```

- `archive/raw`: unveraenderte Originaldateien jedes Exportlaufs.
- `archive/manifests`: SHA-256, Encoding, Zeilenzahl und Archivpfad.
- `normalized/runs`: einheitliche CSV je Exportlauf.
- `normalized/transactions.csv`: deduplizierter Gesamtbestand.
- `database/transactions.sqlite3`: SQLite-Datenbank inklusive
  Quellenverknuepfungen und zusaetzlicher Bankfelder.
- `database/rules.sqlite3`: erweiterbare Regeldatenbank fuer die automatische
  Klassifikation.

Die normalisierten CSV-Dateien verwenden UTF-8 mit Semikolon, ISO-Datum und
Dezimalpunkt:

```text
transaktions_id;datum;kontoname;kontonummer;zahlungsbeteiligter;verwendungszweck;betrag;kontostand_konto;kontostand_gesamt;kontostand_gesamt_vollstaendig;transaktionstyp;oberkategorie;unterkategorie;sphaere;fachliche_beschreibung;klassifikationsstatus;budget_id
```

`kontonummer` enthaelt die normalisierte eigene IBAN. Fehlende
Zahlungsbeteiligte bleiben leer und werden nicht erfunden.
`verwendungszweck` wird unveraendert aus den eingelesenen Bankdaten
uebernommen.

Bei jedem neuen Volksbank- und Sparkassen-Export wird der aktuelle
Kontostand aus der eindeutig per IBAN zugeordneten Konto-Uebersicht
ausgelesen. Bei Volksbank-Exporten muss dieser Wert fuer Konten mit
Umsaetzen exakt zum neuesten Feld `Saldo nach Buchung` passen. Dadurch kann
auch ein umsatzloses Konto einen aktuellen Saldo erhalten.

Das Sparkassen-CSV-Format enthaelt selbst kein Kontostandsfeld. Der
Uebersichtssaldo dient dort als Anker. Ausgehend davon wird der Kontostand
fuer jede Position ueber die gesamte vorhandene Transaktionshistorie
rueckwaerts berechnet. Die Reihenfolge innerhalb eines Buchungstags stammt
aus den archivierten CSV-Zeilen. Widerspruechliche Reihenfolgen,
Saldo-Ketten oder ueberlappende Beobachtungen brechen den Import ab.

`kontostand_konto` enthaelt den Saldo des jeweiligen Kontos nach der
Transaktion. `kontostand_gesamt` ist die Summe aller aktuell bekannten
Kontostaende. `kontostand_gesamt_vollstaendig` ist nur `1`, wenn fuer jedes
registrierte Konto ein aktueller Saldo vorliegt. Fehlt bei einem alten,
noch nicht erneut exportierten Konto ein belastbarer Saldoanker, bleibt der
Gesamtstand als Teilstand mit Kennzeichen `0` markiert.

Die Klassifikation besteht aus `transaktionstyp`, `oberkategorie`,
`unterkategorie`, `sphaere` und der optionalen
`fachliche_beschreibung`. `klassifikationsstatus` wird daraus abgeleitet:

- `unklassifiziert`: alle fuenf Klassifikationsfelder sind leer.
- `vollstaendig_klassifiziert`: alle vier Pflichtfelder sind befuellt.
- `unvollstaendig_klassifiziert`: mindestens ein Feld ist befuellt, aber
  nicht alle Pflichtfelder. Diese Datensaetze sind manuell zu pruefen.

Eine automatische Klassifikation ist ausschliesslich fuer
`unklassifiziert` zulaessig. Die zentrale Funktion
`transaction_store.can_be_auto_classified(transaction)` setzt diese Sperre
um. Bereits ein einzelner vorhandener Wert, auch nur in der optionalen
Beschreibung, verhindert automatische Aenderungen.

Aktive automatische Regel:

- Enthaelt der normalisierte Verwendungszweck
  `Vergütung Trainer BSV 1`, werden Transaktionstyp `Vergütung`,
  Oberkategorie `Personal und Vergütungen`, Unterkategorie
  `Vergütungen - BSV 1`, Sphaere `Ideeller Bereich` und fachliche
  Beschreibung `Vergütung Trainer BSV 1` gesetzt.
- Enthaelt der normalisierte Verwendungszweck
  `Vergütung Co Trainer BSV 1`, werden Transaktionstyp `Vergütung`,
  Oberkategorie `Personal und Vergütungen`, Unterkategorie
  `Vergütungen - BSV 1`, Sphaere `Ideeller Bereich` und fachliche
  Beschreibung `Vergütung Co-Trainer BSV 1` gesetzt.

Die Regeln liegen in der Tabelle `classification_rules` der separaten
Regeldatenbank. Jede Regel besitzt eine stabile ID, einen Namen, Aktivstatus,
Vergleichsfeld, Operator, Vergleichswert und den zu setzenden
Klassifikationssatz. Aktuell werden `contains`, `equals`, `starts_with` und
`ends_with` unterstuetzt.

Treffen mehrere Regeln auf eine noch unklassifizierte Transaktion zu, werden
die vier Pflichtfelder nicht befuellt. Nur `fachliche_beschreibung` erhaelt
den Hinweis `Mehrere zutreffende Regeln: Regel1, Regel2, ...`. Dadurch wird
die Transaktion als `unvollstaendig_klassifiziert` markiert, fuer weitere
Automatik gesperrt und kann manuell geprueft werden.

Die Transaktions-ID beginnt mit `tx_` und ist ein deterministischer SHA-256
aus Provider, eigener IBAN, Buchungs- und Valutadatum, Betrag, Waehrung,
Zahlungsbeteiligtem, Gegenkonto, Buchungstext, Verwendungszweck und
vorhandenen Mandats-/Glaeubigerreferenzen. Ein Vorkommensindex unterscheidet
auch zwei inhaltlich identische Buchungen innerhalb desselben Exports.
Wiederholte oder ueberlappende Exporte behalten dieselben IDs.

Die SQLite-Datenbank enthaelt:

- `accounts`: registrierte Konten inklusive aktuell bekanntem Kontostand.
- `source_files`: jede archivierte Quelldatei inklusive vorhandenem
  Kontostandsanker.
- `transactions`: deduplizierte Transaktionen; `amount_minor` speichert den
  Betrag und `account_balance_minor` den Kontostand zusaetzlich als
  ganzzahlige Centzahl.
- `transaction_sources`: Herkunft jeder Transaktion aus allen Exportlaeufen
  inklusive der jeweiligen Saldo-Beobachtung.
- `normalized_transactions`: Sicht mit normalisierten Feldern und
  abgeleitetem Klassifikationsstatus sowie `budget_id`.
- `budgets`: Budgettabelle mit `saison`, `oberkategorie`,
  `unterkategorie`, `einnahmen`, `ausgaben`, dem berechneten Wert
  `budget = ausgaben - einnahmen` und der automatisch erzeugten
  `budget_id`.
- `vorgaenge`: zentrale Vorgangstabelle mit `vorgangs_id`, `vorgangstyp`,
  `status`, `erstellt_am` und `aktualisiert_am`. Erlaubte Statuswerte sind
  `in_bearbeitung` und `abgeschlossen`.
- `transaktion_vorgaenge`: N:M-Zuordnung mit `transaktions_id` und
  `vorgangs_id`; beide Spalten besitzen Fremdschluessel.
- `belege`: Dokumentkatalog mit stabiler Beleg-ID, absolutem Dateipfad,
  Dateiname, Typ, Groesse, SHA-256 und Verfuegbarkeitsstatus.
- `vorgang_belege`: N:M-Zuordnung mit `vorgangs_id` und `beleg_id`;
  direkte Beziehungen zwischen Transaktionen und Belegen existieren nicht.

Fuer jede Transaktion wird automatisch ein Vorgang mit der ID
`vorgang_<transaktions_id>` erzeugt und ueber `transaktion_vorgaenge`
zugeordnet. Der Vorgangstyp wird mit dem Transaktionstyp synchronisiert.
Eine vollstaendig klassifizierte Transaktion vom Typ `Vergütung` setzt den
Vorgang auf `abgeschlossen`; alle anderen Zustaende setzen ihn auf
`in_bearbeitung`. Bestehende Transaktionen werden bei der Schema-Migration
nachgezogen.

Jede Kombination aus Transaktion und Vorgang beziehungsweise Vorgang und
Beleg kann nur einmal vorkommen. Eine Transaktion kann mehreren Vorgaengen
zugeordnet werden; ein Beleg kann ueber `vorgang_belege` mehreren Vorgaengen
zugeordnet werden.

Der Belegordner wird ueber `BSV_BELEGE_DIR` konfiguriert. Beim Start des
Dashboards wird der Ordner rekursiv eingelesen und der Dokumentkatalog
aktualisiert. Der gespeicherte `dateipfad` ist immer absolut. Nicht mehr
vorhandene Dateien bleiben als Datensatz erhalten und werden mit
`vorhanden = 0` markiert. Bestehende `transaktion_belege`-Eintraege werden
bei der Migration einmalig auf alle zugeordneten Vorgaenge uebertragen und
die alte Tabelle wird anschliessend entfernt.

```dotenv
BSV_BELEGE_DIR=D:\BSV_Banking\data\belege
```

Eine Saison beginnt am 1. Juli. Beispielsweise gehoert der Zeitraum vom
1. Juli 2025 bis zum 30. Juni 2026 zur Saison `2025/2026`. Sobald bei einer
normalisierten Transaktion Ober- und Unterkategorie befuellt sind, wird ihre
`budget_id` aus Saison und beiden Kategorien abgeleitet. Ein Budgeteintrag
mit derselben Saison und denselben Kategorien erhaelt automatisch dieselbe
ID. `budget` und `budget_id` sind berechnete Spalten und werden beim
Einfuegen in `budgets` nicht explizit angegeben.

## Lokales Dashboard

Das Dashboard wird lokal gestartet und bindet standardmaessig nur an
`127.0.0.1`:

```powershell
.\.venv\Scripts\python main.py --dashboard
```

Danach ist es unter `http://127.0.0.1:8765/` erreichbar. Der Browser wird
automatisch geoeffnet. Fuer einen Start ohne automatisches Browserfenster:

```powershell
.\.venv\Scripts\python main.py --dashboard --no-browser
```

Der Reiter `Transaktionen` ist standardmaessig auf die letzten drei
Kalendermonate eingestellt. Der Zeitraum kann ueber `Von` und `Bis`
geaendert oder zurueckgesetzt werden. Angezeigt werden Datum, Kontoname,
Zahlungsbeteiligter, gekuerzter Verwendungszweck, Betrag und
`Kontostand Konto`. Alle Spalten sind sortierbar; das Suchfeld durchsucht
alle angezeigten Spalten. Oberhalb der Tabelle stehen die bekannten
Kontostaende je Konto und deren Summe. Fehlende Salden werden sichtbar
ausgewiesen und der Gesamtwert als Teilstand bezeichnet.

Ein Klick auf eine Zeile oeffnet alle normalisierten Daten inklusive
Kontostaenden, Bankfeldern, Klassifikationen, Zuordnungen, Importquellen und
Rohdaten. Die Felder `Transaktionstyp`, `Oberkategorie`, `Unterkategorie`,
`Sphaere` und `Fachliche Beschreibung` koennen in der Detailansicht
bearbeitet werden. Transaktionstyp und Oberkategorie bieten bisherige Werte
als Vorschlaege an; Unterkategorie und Sphaere werden wie bei der
Regelerstellung von den gewaehlten Kategorien abhaengig angeboten.
Aenderungen werden automatisch gespeichert und der Klassifikationsstatus
wird direkt neu berechnet.

Der Reiter `Vorgaenge` zeigt die zentrale Vorgangsliste mit Vorgangstyp,
Status, Bezug, Betrag und Anzahl der zugeordneten Transaktionen. In den
Vorgangsdetails koennen die Klassifikationsfelder der zugeordneten
Transaktionen ebenfalls bearbeitet werden. Die Regelverwaltung steht direkt
daneben im Vorgangsfenster, sodass Vorgangsdaten beim Erstellen oder
Bearbeiten einer Regel sichtbar bleiben und uebernommen werden koennen. Die
Liste vorhandener Regeln ist dort standardmaessig eingeklappt. Eine
eigene Abschlussregelverwaltung steht sowohl in Transaktions- als auch in
Vorgangsdetails zur Verfuegung. Abschlussregeln laufen nach den
Klassifikationsregeln. Ein Vorgang wird nur automatisch abgeschlossen, wenn
alle zugeordneten Transaktionen vollstaendig klassifiziert sind und jeweils
zu einer aktiven Abschlussregel passen. Manuell gesetzte Vorgangsstatus
werden dabei nicht ueberschrieben. Die bisherige Verguetungslogik ist als
bearbeitbare Standard-Abschlussregel angelegt. Der Reiter `Budget` zeigt die
Eintraege der Budgettabelle oder einen Leerzustand.

Der Reiter `To-Dos` verwaltet Aufgaben mit stabilen IDs im Format
`todo_<uuid>`. Manuelle Aufgaben enthalten Titel, Beschreibung, Fälligkeit,
Priorität und Abschlussstatus. Sie können bei der Anlage oder später mit
beliebig vielen Vorgängen verknüpft werden. Die Tabelle `todos` enthält
zusätzlich Herkunft und Quellenreferenz, damit spätere automatische
Erzeuger wie die Mailverarbeitung ohne Schemaänderung ergänzt werden
können. `todo_vorgaenge` bildet die n:m-Zuordnung zu `vorgaenge` mit
Fremdschlüsseln ab. Verknüpfte To-Dos werden auch im jeweiligen
Vorgangsdatensatz ausgegeben.

Die API stellt `GET/POST /api/todos`, `GET/PATCH/DELETE /api/todos/<todo_id>`
sowie Endpunkte unter `/api/todos/<todo_id>/vorgaenge` für einzelne
Zuordnungen bereit. Die Oberfläche unterstützt Erstellen, Bearbeiten,
Abschließen, Wiederöffnen, Filtern und Löschen.

Der Reiter `Mails` bindet Microsoft 365 ueber OAuth2 und Microsoft Graph an.
`MS_CLIENT_ID` und `MS_AUTHORITY` werden aus
`D:\.secrets\bsv_banking.env`, `D:\.secrets\personalhub.env` oder der
Prozessumgebung gelesen. Beim ersten Zugriff startet ein Device-Code-Login.
Der Mail-Reiter zeigt die Microsoft-Anmelde-URL und den Code an; nach der
Anmeldung laedt der Button `Mails neu laden` die Nachrichten. Das
Refresh-Token wird lokal unter `.runtime/auth/ms_graph_token.json`
gespeichert. Der Client benoetigt die delegierten Rechte `Mail.Read`,
`Mail.ReadWrite`, `Mail.Send`, `offline_access` und `User.Read`.

Gelesen werden ungelesene Nachrichten aus Posteingang, Junk-E-Mail und
Ordnern mit Anzeigename `BSV`. Die Mailliste laedt zielordnerweise in
kleinen Seiten von aktuell nach alt und zeigt jede geladene Seite sofort an.
Beim Listenladen werden nur technische IDs, Betreff, Absender, Vorschau,
Ordner, Empfangszeit und Kategorien lokal gespeichert. Volltext und bis zu
zwoelf Anhaenge werden erst beim Oeffnen, Zusammenfassen oder Vorgang-Import
ueber Graph in die lokale Transaktionsdatenbank uebernommen. Ein Klick zeigt
die gespeicherten Inhalte
an; Mailtext und Anhang werden nebeneinander dargestellt. Bilder,
PDF-Dateien und extrahierte Textinhalte koennen zwischen 25 und 800 Prozent
vergroessert werden. DOCX-Texte werden ohne Office-Automatisierung gelesen;
fuer PDF-Textextraktion wird `pypdf` verwendet.

Der sichtbare Tag `BSV` oder `Privat` kann durch Anklicken gewechselt werden
und wird als Microsoft-Graph-Kategorie gespeichert. Andere vorhandene
Kategorien bleiben erhalten. Antworten werden ueber Graph gesendet. Jede
Mail kann direkt in der Liste ohne Oeffnen als gelesen markiert werden.
Daneben steht eine Loesch-Checkbox; der Sammelbutton `Markierte Mails
loeschen` entfernt alle bewusst markierten Nachrichten unabhaengig vom
Spam-Score.

Mailverlaeufe werden anhand der `conversationId` erkannt. Wenn zu einer Mail
mehrere Nachrichten im Verlauf gefunden werden, zeigt die Oberflaeche ein
Verlauf-Badge mit Nachrichtenzahl. Lesen, Taggen, Loeschen und
Zusammenfassung werden dann auf den ganzen Verlauf angewendet. Die
Zusammenfassung erhaelt die Mailtexte des Verlaufs chronologisch
zusammengefuehrt; Aktionen deduplizieren die betroffenen Inbox-IDs.

Jede Mail besitzt ausserdem den Button `Zusammenfassung`. Erst beim Klick
werden Volltext und bis zu sechs ausgelesene Anhangstexte an
`OPENAI_SUMMARY_MODEL` (ersatzweise `OPENAI_MODEL`) gesendet. Die Ansicht
zeigt Zusammenfassung, wichtige Punkte und ToDos direkt unter der Mail.
Aufgaben fuer Christoph Suessmeier werden hervorgehoben. Die Zuordnung
behandelt Christof Fries und Christopher Pethe ausdruecklich als andere
Personen; unklare Aufgaben bleiben als solche gekennzeichnet.

Fuer jede geladene Mail wird ein Spam-Score berechnet. Wenn
`OPENAI_API_KEY` in `D:\.secrets\bsv_banking.env`,
`D:\.secrets\personalhub.env` oder der Prozessumgebung vorhanden ist, werden
nur Betreff, Absender, Empfangszeit und die kurze Mail-Vorschau an das
konfigurierte Modell (`OPENAI_MODEL`, Standard `gpt-5-nano`) gesendet.
Andernfalls wird eine lokale Heuristik verwendet. Mailtext und Anhaenge
werden nicht an die Spam-Bewertung uebergeben. Die Loeschgrenze liegt pro
Dashboard-Start standardmaessig bei mehr als 70 Prozent und kann im
Mail-Reiter geaendert werden. Der Server erzwingt diese Grenze auch fuer
direkte API-Aufrufe. Der Sammelbutton neben der Schwelle zeigt die Anzahl
der betroffenen Mails und loescht mit einem Klick alle aktuell geladenen
Mails oberhalb der Schwelle.

Jede Mail erhaelt eine stabile interne ID im Format `inbox_<uuid>`. Die
Graph-Message-ID bleibt als technische Quellen-ID erhalten; wenn eine
Internet-Message-ID geliefert wird, wird sie zur Wiedererkennung nach einem
Verschieben der Mail verwendet. Die Tabellen `inbox_messages` und
`inbox_attachments` in der Transaktionsdatenbank speichern Absender,
Empfaenger, Betreff, Empfangszeit, Ordner, Tag, Volltext, technische IDs
sowie Anhangsmetadaten, extrahierten Text und den Anhang selbst als BLOB.
Gelesen-Markieren entfernt diese lokalen Daten nicht. Explizites Loeschen
entfernt die Mail ueber Graph und loescht den lokalen Inbox-Datensatz
inklusive Anhaengen und Vorgangsverknuepfungen.

Die Tabelle `inbox_vorgaenge` verknuepft `inbox_id` und `vorgangs_id` mit
Fremdschluesseln. Die Zuordnung kann ueber
`GET/POST /api/mail/<inbox_id>/vorgaenge` gelesen beziehungsweise angelegt
und mit `DELETE /api/mail/<inbox_id>/vorgaenge/<vorgangs_id>` entfernt
werden. Die Oberflaeche zeigt die stabile Inbox-ID an; eine automatische
Vorgangserstellung ist noch nicht Bestandteil dieses Schritts.
Gelesene oder geloeschte Mails erscheinen nicht in den Mail-Statistiken; die
Uebersicht zeigt nur die Anzahl ungelesener Mails.

Bereits berechnete Spam-Ergebnisse und auf Knopfdruck erstellte
Zusammenfassungen werden in `mail_processing.sqlite3` neben der
Transaktionsdatenbank gespeichert. Fuer Zusammenfassungen liegen dort nur
das abgeleitete JSON-Ergebnis und ein SHA-256-Fingerabdruck des Inhalts.
Eine unveraenderte Mail wird beim naechsten Dashboard-Start nicht erneut
durch das jeweilige Modell verarbeitet; bei geaendertem Inhalt oder Modell
wird sie neu bewertet. Spam-Ergebnisse unter 0,5 Prozent, die in der
Oberflaeche als `0 %` erscheinen, gelten nicht als verlaesslicher
Cachetreffer und werden bei jedem erneuten Laden neu klassifiziert, auch
wenn sie bereits in der Cache-Datenbank lagen. Lesen, Taggen,
Gelesen-Markieren, Antworten und Loeschen arbeiten unmittelbar gegen
Microsoft Graph. Die automatische Spam-Loeschung bleibt auf Mails oberhalb
der Schwelle begrenzt; eine manuelle Checkbox-Auswahl gilt als
ausdrueckliche Loeschentscheidung.

Im Transaktionsbereich stehen drei weitere Funktionen zur Verfuegung:

- `Kontoverlauf anzeigen` oeffnet ein SVG-Diagramm. Standardmaessig ist der
  Gesamtkontostand der letzten drei Monate aktiviert. Gesamtkontostand und
  einzelne Konten koennen ueber Checkboxen beliebig kombiniert werden; der
  Zeitraum ist frei waehlbar. Die historischen Tagesstaende werden aus dem
  aktuellen Kontostand und den gespeicherten Kontobewegungen rekonstruiert.
  Die Y-Achse verwendet automatisch gerundete Schritte wie 100, 500, 1.000,
  5.000 oder 10.000 Euro und zeigt ungefaehr zehn Hilfslinien. Die Nulllinie
  wird hervorgehoben.
- `Regeln verwalten` zeigt alle aktiven und inaktiven
  Klassifikationsregeln. Neue Regeln bestehen aus Vergleichsfeld, Operator,
  Vergleichswert und den vier Pflichtfeldern des Klassifikationsergebnisses.
  Die fachliche Beschreibung ist optional. Optional wird eine neue aktive
  Regel sofort angewendet. Regeln bearbeiten nur
  vollstaendig unklassifizierte Transaktionen und ueberschreiben keine
  manuellen Eingaben. Die Regeluebersicht kann durchsucht werden. Ein Klick
  auf eine Regel laedt ihre Felder zur nachtraeglichen Bearbeitung in das
  Formular. Regeln koennen auch dauerhaft entfernt werden; bereits
  klassifizierte Transaktionen bleiben dabei unveraendert. Transaktionstyp
  und Oberkategorie bieten bisherige Werte als frei ergaenzbare Vorschlaege
  an. Unterkategorien werden passend zur eingegebenen Oberkategorie
  vorgeschlagen und erst danach freigeschaltet. Fuer bekannte Kombinationen
  aus Ober- und Unterkategorie wird die bisher am haeufigsten verwendete
  Sphaere vorausgewaehlt.
- Im selben Bereich koennen `Abschlussregeln` erstellt, bearbeitet,
  durchsucht, deaktiviert und entfernt werden. Ihre Bedingungen duerfen
  neben Buchungsfeldern auch Transaktionstyp, Oberkategorie,
  Unterkategorie, Sphaere und fachliche Beschreibung auswerten. Optional
  werden sie sofort auf bestehende Vorgaenge angewendet.
- `Aktuelle Kontobewegungen anfordern` startet im Hintergrund fuer alle
  konfigurierten Bankquellen den bestehenden CSV-Export und anschliessenden
  Import. Der sichtbare Bankbrowser wird geoeffnet; Login und MFA muessen
  gegebenenfalls dort abgeschlossen werden. Das Dashboard zeigt den
  Auftragsstatus und verhindert parallele Aktualisierungslaeufe.

Sparkassenumsätze im Status `Umsatz vorgemerkt` werden nicht importiert.
Sie werden erst als Transaktion und Vorgang angelegt, sobald die Bank sie als
gebucht ausweist.

### Spielerprämien aus DFBnet

Im Dashboard steht unter `Sonstige Aufgaben` die Aktion
`Spielerprämien ermitteln` zur Verfügung. Sie wertet für die ausgewählte
Saison und die ausgewählten BSV-Mannschaften Meisterschafts- und Pokalspiele
aus. Freundschaftsspiele werden ignoriert. Startaufstellung und tatsächlich
eingewechselte Spieler erhalten je nach Ergebnis 3 Punkte für einen Sieg,
1 Punkt für ein Unentschieden und 0 Punkte für eine Niederlage.

Die Zugangsdaten werden ausschließlich lokal aus
`D:\.secrets\bsv_banking.env` geladen:

```dotenv
DFBNET_USERNAME=...
DFBNEET_PASSWORD=...
```

Alternativ wird für das Passwort auch `DFBNET_PASSWORD` unterstützt. Der
Browser verwendet ein separates Profil unter
`.runtime/session/dfbnet-chromium`. Ergebnisse werden zusätzlich als lokale
JSON-Dateien unter `.runtime/dfbnet/player_premiums` abgelegt.

Pro Mannschaft kann die `Summe pro Punkt` vor dem Start angepasst werden.
Voreingestellt sind 5,00 Euro fuer Herren 1 sowie 2,50 Euro fuer Herren 2 und
Damen. Die Ergebnistabelle zeigt Punkte und die daraus berechnete Praemie je
Spiel sowie die Gesamtpraemie je Spieler.

Historische DFBnet-Namen werden zusammen mit der Mannschaftsart des
Wettbewerbs ausgewertet: Der Vereinsname ohne Zusatz gehoert in
Frauen-Wettbewerben zu den Damen und in Herren-Wettbewerben zu Herren 1.
Der Zusatz `I` steht ebenfalls fuer Herren 1, `II` fuer Herren 2. Weitere
Mannschaften werden ignoriert.

## Lokale Daten und Sicherheit

Standardmaessig liegen alle Laufzeitdaten unter `.runtime/`:

- `.runtime/session/chromium/`: separates Chromium-Profil mit Cookies und
  Local Storage
- `.runtime/logs/`: rotierende Logdatei
- `.runtime/screenshots/`: Fehler-Screenshots
- `.runtime/exports/`: rohe CSV-Umsatzdateien pro Exportlauf

Diese Pfade sowie `config.toml`, `.env`, `*.env` und virtuelle Umgebungen stehen
in `.gitignore`. Auch `data/` ist ausgeschlossen. Credential-Werte werden
nicht geloggt. URL-Querystrings und
URL-Zugangsdaten werden vor dem Logging redigiert. Loginfelder werden auf
Fehler-Screenshots schwarz maskiert. Die Anwendung versucht restriktive Datei-
und Verzeichnisrechte zu setzen; unter Windows gelten zusaetzlich die
NTFS-Rechte des Benutzerkontos.

Screenshots, CSV-Dateien und das Browserprofil koennen sensible Bankdaten
enthalten. Das Projekt daher nur in einem lokalen, nicht synchronisierten
Verzeichnis unter einem geschuetzten Benutzerkonto verwenden. Fuer einen
garantiert frischen Login inklusive MFA kann `.runtime/session/` bei
geschlossenem Browser manuell entfernt werden.

## Unit-Tests

Die Tests starten keinen Browser und greifen nicht auf eine Bank zu:

```powershell
.\.venv\Scripts\python -m unittest discover -s tests -v
```

## Fehlerausgaben

- Exit-Code `0`: Login erfolgreich erkannt
- Exit-Code `1`: Laufzeit- oder Loginfehler; Screenshot wird versucht
- Exit-Code `2`: ungueltige oder fehlende Konfiguration
- Exit-Code `3`: Playwright fehlt
- Exit-Code `130`: manueller Abbruch mit `Ctrl+C`

Die Playwright-Installation folgt der offiziellen Dokumentation:
https://playwright.dev/python/docs/intro
