# Portfolio Backend

Ho creato il mio **Portfolio personale** per avere un sito vetrina dove poter raccontare chi sono, mostrare le mie competenze informatiche e i miei progetti scolastici. Essendo un progetto in sviluppo, continuerò ad aggiornarlo man mano che acquisisco nuove competenze.

Su consiglio del mio **professore di informatica**, ho deciso di integrare un **Backend** al portfolio. Volevo che il form di contatto creato nella sezione *Get in Touch* funzionasse realmente, collegandosi a un server privato.

### Architettura
Invece di partire da zero, ho deciso di prendere come struttura il **"Blog Scolastico"** che avevamo sviluppato in classe con Flask.
L'ho modificata e riadattata per servire esclusivamente come **API** (Backend) in grado di comunicare col frontend React.

### Cosa ho usato e Perché

- **Backend (Python + Flask):** Ho usato Flask, ho mantenuto lo stile ad *Application Factory* e l'uso del *Repository Pattern* per avere codice scalabile.
- **Sicurezza (Flask-CORS):** Ho implementato i CORS per assicurarmi che solo le richieste in entrata dal mio sito Portfolio ufficiale venissero accettate dall'API protetta.
- **Database (SQLite):** Per salvare i messaggi in ingresso, ho tenuto SQLite. È leggero, affidabile e non richiede installazioni pesanti, perfetto per questo progetto.
- **Frontend App:** L'interfaccia (in un altro repository) è sviluppata in React. Ho usato fetch() per collegarlo a questa API asincronamente.
- **Hosting Cloud (PythonAnywhere):** È un servizio di hosting gratuito ottimizzato per Python. L'ho scelto appositamente per la sua comodità e perché (a differenza di altri servizi gratuiti concorrenti come Render) mi permette di mantenere il file SQLite locale intatto, senza perdere lo storico dei messaggi ricevuti quando si spegne.

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

## Struttura del Progetto

```text
├── app/
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

Il server remoto è ora ospitato stabilmente e riceve richieste CORS solo dal mio Portfolio.
