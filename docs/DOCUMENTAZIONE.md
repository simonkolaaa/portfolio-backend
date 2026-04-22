# Documentazione Tecnica — Portfolio Backend

---

## 1. Introduzione

Il progetto è un **backend per portfolio personale** sviluppato con Python e Flask. Espone un'API che consente ai visitatori di inviare messaggi di contatto tramite un form, e permette all'amministratore di consultare e gestire questi messaggi tramite una dashboard protetta da autenticazione.

Il backend è pensato per essere consumato da un frontend separato (es. il portfolio statico su GitHub Pages) ed è strutturato per essere distribuito su PythonAnywhere.

---

## 2. Obiettivi generali

- Permettere a chiunque di inviare un messaggio di contatto tramite form (senza autenticazione).
- Consentire all'amministratore di visualizzare, filtrare e gestire i messaggi ricevuti (Inbox).
- Proteggere la dashboard con un sistema di login basato su sessioni Flask.
- Esporre un endpoint AI (`/api/arus`) per interagire con l'assistente Arus via Gemini.
- Organizzare il codice in modo pulito e scalabile tramite Blueprints e Repository Pattern.

---

## 3. Requisiti funzionali

### Funzionalità principali

1. Invio di un messaggio di contatto con nome, email e testo (`POST /api/contact`).
2. Visualizzazione della lista dei messaggi ricevuti (filtro per testo e preferiti) — richiede login (`GET /api/contacts`).
3. Possibilità di marcare/demarcare un contatto come preferito (`POST /api/contacts/<id>/toggle-favorite`).
4. Registrazione e login dell'amministratore (`/auth/register`, `/auth/login`).
5. Logout e invalidazione della sessione (`/auth/logout`).
6. Interazione con l'assistente AI Arus tramite endpoint dedicato.

### User stories

- Come **visitatore del portfolio**, voglio inviare un messaggio a Simon compilando un form, in modo che possa essere contattato.
- Come **amministratore**, voglio accedere a una dashboard protetta per leggere i messaggi ricevuti.
- Come **amministratore**, voglio filtrare i messaggi per parola chiave o visualizzare solo i preferiti.
- Come **amministratore**, voglio segnare un messaggio come preferito per trovarlo rapidamente in seguito.
- Come **visitatore**, voglio interagire con l'assistente Arus per sapere chi è Simon e cosa sa fare.

---

## 4. Requisiti non funzionali

- Le password degli utenti devono essere memorizzate con hashing sicuro (Werkzeug `generate_password_hash`).
- Il backend deve essere CORS-abilitato per permettere richieste cross-origin dal frontend statico.
- Il codice deve essere organizzato con Flask Blueprints (`auth`, `api`) e Repository Pattern.
- Il progetto deve essere eseguibile localmente con un ambiente virtuale Python (`venv`).
- I dati (messaggi, utenti, progetti) devono essere persistenti su database SQLite.
- Le variabili sensibili (chiavi API, secret key) devono essere gestite tramite file `.env`.

---

## 5. Schema ER (Entità e Relazioni)

Il database SQLite è composto da quattro tabelle. La tabella `contacts` raccoglie i messaggi inviati dai visitatori. La tabella `user` gestisce l'accesso amministrativo. Le tabelle `projects` e `categories` organizzano i contenuti del portfolio esposti via API al frontend.

```mermaid
erDiagram
    USER {
        int id PK
        string username
        string password
    }
    CONTACTS {
        int id PK
        string name
        string email
        string message
        boolean is_favorite
        datetime created_at
    }
    PROJECTS {
        int id PK
        string title
        string description
        string url
        int category_id FK
    }
    CATEGORIES {
        int id PK
        string name
    }

    USER ||--o{ CONTACTS : "gestisce (dashboard)"
    CATEGORIES ||--o{ PROJECTS : "classifica"
```

> `USER` non ha una relazione diretta con `CONTACTS` a livello di chiave esterna nel DB: la relazione è logica — l'utente amministratore gestisce i contatti tramite la dashboard protetta.

---

## 6. Diagramma UML delle Classi

L'applicazione segue il **Repository Pattern**: la logica di accesso al database è separata dalle rotte Flask. I Blueprint `auth` e `api` orchestrano le operazioni delegando al layer dei repository.

```mermaid
classDiagram
    class UserRepository {
        +create_user(username, password_hash) bool
        +get_user_by_id(id) dict
        +get_user_by_username(username) dict
    }
    class ContactRepository {
        +create_contact(name, email, message) void
        +get_all_contacts(search, favorite_only) list
        +toggle_favorite(id) void
    }
    class ProjectRepository {
        +get_all_projects() list
        +create_project(data) void
    }

    class Auth_Blueprint {
        -url_prefix : string
        +register() Response
        +login() Response
        +logout() Response
        +login_required(view) decorator
        +load_logged_in_user() void
    }
    class API_Blueprint {
        -url_prefix : string
        +add_contact() Response
        +get_contacts() Response
        +toggle_favorite(id) Response
    }
    class ArusBrain {
        -SIMON_CONTEXT : string
        -ARUS_SYSTEM_PROMPT : string
        -GEMINI_MODEL : string
        +stream_arus(user_message) Generator
    }

    API_Blueprint ..> ContactRepository : usa
    API_Blueprint ..> Auth_Blueprint : richiede (login_required)
    Auth_Blueprint ..> UserRepository : usa
    ArusBrain ..> GeminiAPI : chiama (HTTP REST)
```

---

## 7. Glossario

| Termine | Definizione |
| --- | --- |
| `Blueprint` | Componente Flask che raggruppa rotte e logica in moduli separati (`auth`, `api`). |
| `Repository Pattern` | Architettura che separa l'accesso al DB dal layer delle rotte, rendendolo sostituibile e testabile. |
| `Contact` | Messaggio inviato da un visitatore tramite il form del portfolio (nome, email, testo). |
| `Preferito` | Flag booleano (`is_favorite`) su un contatto, gestibile dalla dashboard. |
| `User` | Account amministratore unico che può accedere alla dashboard protetta. |
| `Project` | Voce del portfolio (titolo, descrizione, link, categoria) esposta tramite API al frontend. |
| `Category` | Raggruppamento tematico dei progetti (es. `Web`, `AI`, `Backend`). |
| `Arus` | Assistente AI integrato nel portfolio. Chiama Google Gemini via HTTP REST e risponde in streaming. |
| `Sessione` | Meccanismo Flask basato su cookie firmati per mantenere l'utente autenticato tra le richieste. |
| `CORS` | Cross-Origin Resource Sharing: configurazione che permette al frontend (GitHub Pages) di chiamare il backend. |
| `.env` | File locale (non versionato) contenente variabili sensibili come `GOOGLE_API_KEY` e `SECRET_KEY`. |

---

## 8. Pianificazione del progetto (Gantt)

Il progetto è stato sviluppato in tre fasi: analisi e setup, implementazione delle funzionalità core, e rifinitura per la distribuzione.

```mermaid
gantt
    dateFormat  YYYY-MM-DD
    title Portfolio Backend — Piano di Sviluppo

    section Analisi e Setup
    Scelta architettura e struttura cartelle   :a1, 2026-02-10, 3d
    Configurazione ambiente (venv, Flask)      :a2, after a1, 2d
    Definizione schema DB e schema.sql         :a3, after a2, 2d

    section Backend Core
    Implementazione DB layer (db.py)           :b1, after a3, 2d
    Repository Pattern (user, contact, project):b2, after b1, 4d
    Blueprint autenticazione (auth.py)         :b3, after b2, 3d
    Blueprint API REST (api.py)                :b4, after b3, 4d

    section Funzionalità AI
    Modulo Arus con Gemini REST API            :c1, after b4, 3d
    Configurazione streaming SSE               :c2, after c1, 2d

    section Frontend e Integrazione
    Template dashboard contatti (contacts.html):d1, after b4, 3d
    CORS e collegamento con portfolio esterno  :d2, after d1, 2d

    section Distribuzione e Consegna
    Configurazione PythonAnywhere              :e1, after c2, 2d
    Test endpoint, sicurezza e .env            :e2, after e1, 2d
    Documentazione e README                    :e3, after e2, 3d
    Commit finale su GitHub                    :e4, after e3, 1d
```

---

## 9. Diagramma dei casi d'uso

Il sistema ha due attori principali: il **Visitatore** (chiunque acceda al portfolio) e l'**Amministratore**. L'Amministratore è una specializzazione del Visitatore: può fare tutto ciò che fa il Visitatore, più le azioni protette da login.

### Diagramma visivo (Mermaid)

```mermaid
graph LR
    V([Visitatore])
    A([Amministratore])

    subgraph PUB["Azioni pubbliche"]
        UC1(Invia messaggio di contatto)
        UC2(Interagisci con Arus)
    end

    subgraph AUTH["Autenticazione"]
        UC6(Login)
        UC7(Logout)
        UCAUTH{Verifica autenticazione}
    end

    subgraph DASH["Dashboard protetta"]
        UC3(Visualizza inbox)
        UC4(Filtra messaggi)
        UC5(Segna come preferito)
    end

    V --> UC1
    V --> UC2
    A --->|può fare| V
    A --> UC6
    A --> UC7
    A --> UC3
    A --> UC4
    A --> UC5

    UC3 -. "«include»" .-> UCAUTH
    UC4 -. "«include»" .-> UCAUTH
    UC5 -. "«include»" .-> UCAUTH

    UC4 -. "«extend»" .-> UC3
    UC5 -. "«extend»" .-> UC3
    UC2 -. "«extend»" .-> UC1
```

### Notazione formale (PlantUML)

```plantuml
@startuml uc
left to right direction
actor Visitatore
actor Amministratore
Visitatore <|-- Amministratore

Visitatore --> (Invia messaggio di contatto)
Visitatore --> (Interagisci con Arus)

Amministratore --> (Login)
Amministratore --> (Logout)
Amministratore --> (Visualizza inbox)
Amministratore --> (Filtra messaggi)
Amministratore --> (Segna come preferito)

(Visualizza inbox)     .> (Verifica autenticazione) : <<include>>
(Filtra messaggi)      .> (Verifica autenticazione) : <<include>>
(Segna come preferito) .> (Verifica autenticazione) : <<include>>

(Filtra messaggi)      .> (Visualizza inbox)            : <<extend>>
(Segna come preferito) .> (Visualizza inbox)            : <<extend>>
(Interagisci con Arus) .> (Invia messaggio di contatto) : <<extend>>
@enduml
```

### Relazioni tra casi d'uso

**`<<include>>`** — comportamento obbligatorio sempre eseguito:

- `Visualizza inbox` `<<include>>` `Verifica autenticazione`
- `Filtra messaggi` `<<include>>` `Verifica autenticazione`
- `Segna come preferito` `<<include>>` `Verifica autenticazione`

Tutte le azioni della dashboard richiedono sempre il login: se la sessione non è attiva, il sistema reindirizza automaticamente a `/auth/login`.

**`<<extend>>`** — comportamento opzionale o condizionale:

- `Filtra messaggi` `<<extend>>` `Visualizza inbox`: filtrare per parola chiave o preferiti è opzionale rispetto alla semplice lettura dell'inbox.
- `Segna come preferito` `<<extend>>` `Visualizza inbox`: l'azione si attiva durante la consultazione dell'inbox, non è obbligatoria.
- `Interagisci con Arus` `<<extend>>` `Invia messaggio di contatto`: il visitatore può usare l'assistente AI invece (o in alternativa) al form di contatto.

---

> [!NOTE]
> Il frontend del portfolio (HTML/CSS/JS statico) è separato da questo backend ed è distribuito su GitHub Pages all'indirizzo `simonkolaaa.github.io`. Il backend risponde alle sue richieste tramite l'API REST ed è hostato su PythonAnywhere.




