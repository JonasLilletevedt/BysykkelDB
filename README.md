# Bysykkel-database — kort oversikt

**TL;DR:** Design og implementasjon av en relasjonsdatabase for et bysykkelsystem, med transaksjonell check-in/check-out, REST API og en enkel Flask-frontend for brukerregistrering og sanntids bruk. Inkluderer schema, transaksjonstester og demo/kode.

## Hva prosjektet handler om

- Designet en relasjonsdatabase (SQLite) for bysykler med hovedtabeller: `users`, `bikes`, `stations`, `trips`. Skjemaet er normalisert for dataintegritet og effektive spørringer.
- Implementerte og testet transaksjonell logikk for sikker check-in/check-out og samtidighetskontroll (ACID-tenkning), transaksjonene er atomiske: hele transaksjonsomgangen commit'es eller rollback'es ved feil.
- Bygget Shiny-applikasjoner som håndterer UI, input og serverlogikk; Shiny fungerer her både som «frontend» og applikasjonsserver.
- Repository inneholder `schema.sql` / init-skript, Shiny-app-filer (`1app.py`, `2app.py`, `3and4app.py`) og dokumentasjon for hvordan man starter og tester lokalt.

## Teknologistack

- Database: **SQLite** (lokal fil-basert DB)
- UI / server: **Shiny for Python** (Shiny håndterer view, UI og input/server-logikk)
- Datahåndtering: **pandas** (ETL, rensing og transformasjoner)
- Testing: **Manuell testing**
- Miljø: **`requirements.txt`** for å installere avhengigheter i et virtuelt miljø (venv)

## Skjemastruktur (kort)

- `users(id, name, email,  ...)`
- `bikes(id, bike_code, status, station_id, ...)`
- `stations(id, name, capacity, location_lat, location_lng, ...)`
- `trips(id, user_id, bike_id, start_station_id, end_station_id, start_time, end_time, ...)`

## Viktige implementasjonsdetaljer

- **Transaksjoner:** Check-in/check-out håndteres i en enkelt transaksjon som oppdaterer `bikes` og skriver til `trips` for å unngå race conditions. Bruker låsing (`SELECT ... FOR UPDATE`) der nødvendig. Transaksjonen er atomisk: Vi behandler kun én transaksjon om gangen og verifiserer at hele transaksjonen kan gjennomføres før vi gjør endringer i databasen. Slik opprettholder vi konsistens.
- **Validering:** APIen validerer input for å forhindre inkonsistente tilstander (f.eks. sjekker at sykkel er tilgjengelig før checkout).
- **Feilhåndtering:** Retry-/logging-strategi for transaksjonsfeil og konflikter; hvis en transaksjon feiler, rulles den tilbake og et kontrollert retry-forsøk eller feilmelding håndteres av APIen. En kort beskrivelse av retry-logikk og loggformat er inkludert i README.

## Hva du finner i repoet

- `schema.sql`: DDL-skript for å opprette databasetabeller og indekser
- `1app.py`, `2app.py`, `3and4app.py`: Shiny-applikasjoner for ulike deler av funksjonaliteten
- `requirements.txt`: Liste over Python-pakker som kreves for å kjøre applikasjonene
- `README.md`: Prosjektoversikt og instruksjoner for oppsett/kjøring
- `.gitignore`: Filer som skal ignoreres av versjonskontroll

## Kjapp demo (for å prøve lokalt)

## Oppsett og kjøring

Følg disse trinnene for å sette opp miljøet og kjøre Shiny-webapplikasjonene.

1. **Klon repositoriet:**
   Åpne terminalen eller kommandolinjen og last ned prosjektfilene fra GitHub.

   ```bash
   git clone https://github.com/JonasLilletevedt/BysykkelDB
   ```

2. **Naviger til prosjektmappen:**
   Gå inn i den nyopprettede prosjektmappen.

   ```bash
   cd BysykkelDB/
   ```

3. **Opprett et virtuelt miljø:**
   Lag et isolert Python-miljø for prosjektet. Vi kaller det `.venv`.

   ```bash
   python3 -m venv .venv
   ```

4. **Aktiver det virtuelle miljøet:**
   Aktiver miljøet med kommandoen som passer til ditt shell:

   - **Linux/macOS (bash/zsh):**
     ```bash
     source .venv/bin/activate
     ```

   Terminalprompten din skal nå indikere at `.venv`-miljøet er aktivt.

5. **Installer krav:**
   Installer de nødvendige Python-pakkene som er listet i `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

6. **Kjør nettsidene:**
   Prosjektet inneholder tre separate Shiny-applikasjoner: `1app.py`, `2app.py` og `3and4app.py`.
   Hver fil oppretter sin egen nettside med sine respektive oppgaver.

   For å kjøre en spesifikk applikasjon, bruk `shiny run`-kommandoen etterfulgt av filnavnet. For eksempel:

   - **For å kjøre den første appen:**
     ```bash
     shiny run 1app.py
     ```
   - **For å kjøre den andre appen:**
     ```bash
     shiny run 2app.py
     ```
   - **For å kjøre den tredje/fjerde appen:**
     ```bash
     shiny run 3and4app.py
     ```

   Etter å ha kjørt kommandoen vil Shiny vise en lokal URL (vanligvis som `http://127.0.0.1:8000`).
   Åpne denne URL-en i nettleseren din for å se applikasjonen.
   Du må kanskje stoppe én app (vanligvis med `Ctrl+C` i terminalen) før du starter en annen.


