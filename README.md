# Portfolio Backend

Ho creato il mio **Portfolio personale** per avere un sito vetrina dove poter raccontare chi sono, mostrare le mie competenze informatiche e i miei progetti scolastici. Essendo un progetto in sviluppo, continuerò ad aggiornarlo man mano che acquisisco nuove competenze.

Su consiglio del mio **professore di informatica**, ho deciso di integrare un **Backend** al portfolio. Volevo che il form di contatto creato nella sezione *Get in Touch* funzionasse realmente, collegandosi a un server privato.

### Novità dell'ultimo aggiornamento (Super-Stabilità)
Recentemente ho effettuato un importante lavoro di stabilizzazione del backend:
- **CORS Universale:** Per evitare errori di rete ("Impossibile contattare il server"), ho configurato le API per rispondere in modo sicuro a ogni richiesta proveniente dal mio frontend.
- **Isolamento Moduli:** Ho separato la logica del form da quella di Arus AI. Anche se un modulo dovesse avere problemi, il form continuerà a funzionare correttamente.
- **Autogestione delle cartelle:** Il server ora è più intelligente e crea da solo le cartelle necessarie (come `instance/`) se mancano al primo avvio.

### Dashboard Messaggi Premium
Invece di vedere i messaggi nel formato grezzo JSON, ora la rotta `/api/contacts` restituisce una vera e propria **Dashboard HTML professionale**.
Sempre su richiesta del professore, ho usato **Jinja2** per creare un'interfaccia **Monochrome (Bianco e Nero)** ad alto contrasto, con un pulsante dinamico per passare dalla modalità Chiara alla modalità Scura.

### Cosa ho usato e Perché

- **Backend (Python + Flask):** Ho usato Flask, mantenendo lo stile ad *Application Factory* e il *Repository Pattern* per avere codice pulito.
- **Rendering (Jinja2):** Usato per generare la dashboard dei messaggi in modo dinamico direttamente dal server.
- **Sicurezza (Flask-CORS):** Fondamentale per far comunicare il frontend React con le API Flask senza blocchi di sicurezza del browser.
- **Database (SQLite):** Per salvare i messaggi in ingresso. È leggero, affidabile e non richiede database esterni pesanti.
- **Hosting Cloud (PythonAnywhere):** Scelto per la sua comodità e perché permette di mantenere persistente il file SQLite locale.

---

## Messa in Produzione su PythonAnywhere

1. **Clonazione:** Si accede alla console *Bash* e si esegue il `git clone`.
2. **Setup Ambiente:** Si installano le librerie con `pip3 install -r requirements.txt`. (Assicurati di avere `flask-cors`, `requests` e `python-dotenv`).
3. **Inizializzazione:** Si avvia `python3 setup_db.py` per generare il file `portfolio.sqlite`.
4. **Reload:** Nella sezione **"Web"** si preme il bottone **"Reload"** per attivare le modifiche.

---
## Links
- **Link dashboard messaggi:** [https://simonkolaaa.pythonanywhere.com/api/contacts](https://simonkolaaa.pythonanywhere.com/api/contacts)
---

## Struttura del Progetto

```text
├── app/
│   ├── __init__.py           <-- Factory, CORS config & Global Error Handler
│   ├── api.py                <-- Route d'ascolto e Dashboard HTML
│   ├── db.py                 <-- Connessione al DB con autocreazione cartelle
│   ├── templates/
│   │   └── contacts.html     <-- Dashboard dinamica (Light/Dark Mode)
│   └── repositories/         <-- Logica di salvataggio messaggi
├── core/                     <-- Moduli logica avanzata (IA e Memoria)
├── config.py                 <-- File di configurazione unificato
├── schema.sql                <-- Schema SQL per la tabella contacts
├── run.py                    <-- Entry point locale
└── setup_db.py               <-- Script di inizializzazione DB
```

Il server remoto è ora ospitato stabilmente, è resiliente agli errori e presenta una dashboard professionale curata nei minimi dettagli.
