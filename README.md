# Portfolio Backend

Ho creato il mio **Portfolio personale** per avere un sito vetrina dove poter raccontare chi sono, mostrare le mie competenze informatiche e i miei progetti scolastici. Essendo un progetto in sviluppo, continuerò ad aggiornarlo man mano che acquisisco nuove competenze.

Su consiglio del mio **professore di informatica**, ho deciso di integrare un **Backend** al portfolio. Volevo che il form di contatto creato nella sezione *Contatti* funzionasse realmente, collegandosi a un server privato.

### Architettura
Invece di partire da zero, ho deciso di prendere come struttura il **"Blog Scolastico"** che avevamo sviluppato in classe con Flask.
L'ho modificata e riadattata per servire esclusivamente come **API** (Backend) in grado di comunicare col frontend React.

### Dashboard Messaggi nuova
Invece di vedere i messaggi nel formato grezzo JSON, ora la rotta `/api/contacts` restituisce una **Dashboard HTML professionale**.
Sempre su richiesta del professore, ho usato **Jinja2** per creare un'interfaccia **Monochrome (Bianco e Nero)** , con un pulsante dinamico per passare dalla modalità Chiara alla modalità Scura.

### Cosa ho usato e Perché

- **Backend (Python + Flask):** Ho usato Flask, mantenendo lo stile ad *Application Factory* e il *Repository Pattern* per avere codice pulito.
- **Rendering (Jinja2):** Usato per generare la dashboard dei messaggi in modo dinamico direttamente dal server.
- **Sicurezza (Flask-CORS):** Fondamentale per far comunicare il frontend React con le API Flask senza blocchi di sicurezza del browser.
- **Database (SQLite):** Per salvare i messaggi in ingresso. È leggero, affidabile e non richiede database esterni pesanti.
- **Hosting Cloud (PythonAnywhere):** Scelto per la sua comodità e perché permette di mantenere persistente il file SQLite locale.
- **Sicurezza (Flask-CORS):** Ho implementato i CORS per assicurarmi che solo le richieste in entrata dal mio sito Portfolio ufficiale venissero accettate dall'API protetta.

---

## Messa in Produzione su PythonAnywhere
Per pubblicare l'API e renderla ascoltante su internet giorno e notte, ho eseguito il deploy direttamente sul cloud.
Ecco i brevi passaggi che ho seguito per configurare (o per sistemare/ricreare il progetto in caso di bisogno):
1. **Clonazione da GitHub:** Si accede alla console *Bash* cloud di PythonAnywhere e si esegue il `git clone` di questo repository per avere tutti i file sul server.
2. **Installazione Dipendenze:** Nel terminale (dentro la cartella del progetto) si installano le librerie base con `pip3 install --user -r requirements.txt`.
3. **Inizializzazione Database:** Si avvia lo script locale con `python3 setup_db.py`, che genera il nuovo file vuoto di database `portfolio.sqlite` usando lo schema SQL per accogliere i messaggi.
4. **Endpoint WSGI:** Infine, nella sezione **"Web"** di PythonAnywhere, si inizializza una nuova *Web App Manuale* per Python 3.12. Attraverso il file di configurazione `WSGI`, si collegano le rotte del webserver alla mia "Application Factory" di Flask per rispondere ufficialmente all'indirizzo HTTPS generato in origine, abilitando così la POST dal form.

> **Come Aggiornare il Codice Live:**
> Se dovessi fare modifiche ai file in locale su VS Code (e poi _pusharli_ su GitHub), per aggiornare il sito online mi basterà aprire nuovamente il terminale *Bash* su PythonAnywhere, digitare `git pull` per ricevere le variazioni, e poi sulla pagina **"Web"** premere il grosso bottone verde **"Reload"** per far riavviare il servizio.
---
## Links
- **Link dashboard messaggi:** [https://simonkolaaa.pythonanywhere.com/api/contacts](https://simonkolaaa.pythonanywhere.com/api/contacts)
---

## Struttura del Progetto (in continuo sviluppo)

```text
│   ├── __init__.py           <-- Factory (create_app) & CORS config
│   ├── api.py                <-- Route d'ascolto (POST /api/contact)
│   ├── db.py                 <-- Connessione al Database
│   └── repositories/
│       └── contact_repo.py   <-- Gestione queries SQLite pulite (INSERT)
├── instance/
│   └── portfolio.sqlite      <-- Il file in cui vengono salvati i messaggi
├── schema.sql                <-- Schema base della tabella contacts
├── run.py                    <-- Entry point per avviare il server (localhost:5000)
└── setup_db.py               <-- Script per inizializzare il DB da zero
```
## Nuove Funzionalità e Requisiti Modulo 03

Il progetto è stato aggiornato per soddisfare pienamente i requisiti del modulo `03_Sviluppo_Web_e_Database`.

### Autenticazione e Sicurezza
- **Sistema di Login/Registrazione**: Accesso protetto alla dashboard Inbox.
- **Password Hashing**: Le password sono gestite in modo sicuro tramite `werkzeug.security` (hashing PBKDF2), garantendo che nessuna credenziale sia salvata in chiaro nel database.
- **Gestione Sessioni**: Utilizzo di sessioni Flask per proteggere le rotte.

###  Database Relazionale
- **Schema**: Implementazione di tabelle multiple (`user`, `contacts`, `projects`, `categories`).
- **Relazioni**: Utilizzo di chiavi esterne (Foreign Keys) per gestire le relazioni tra categorie e progetti.
- **Persistenza**: Database SQLite ottimizzato per la velocità e la portabilità.

### Dashboard Inbox
- **Ricerca Intelligente**: Filtra i messaggi per nome, email o contenuto testuale.
- **Sistema Preferiti**: Possibilità di contrassegnare i messaggi importanti con una stella (★) tramite interazioni asincrone.
- **Filtri**: Visualizzazione rapida di tutti i messaggi o solo dei preferiti.

### Documentazione Tecnica
Tutta la progettazione concettuale è disponibile nella cartella `docs/`:
- **Diagramma ER**: Schema concettuale del database.
- **UML Class Diagram**: Architettura delle classi e dei repository.
- **Casi d'Uso**: Descrizione delle interazioni tra utenti e sistema.

---

### 🛠️ Come avviare il progetto (Locale)
1. Installa le dipendenze: `pip install -r requirements.txt`
2. Inizializza il DB: `python setup_db.py`
3. Avvia l'app: `python run.py`
4. Accedi alla Inbox: Vai su `/api/contacts` (ti verrà chiesto di registrarti/accedere).

