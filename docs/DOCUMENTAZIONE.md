# Documentazione Tecnica - Portfolio Backend

Questa documentazione descrive l'architettura, il database e i casi d'uso del progetto Portfolio Backend, sviluppato con il modulo `03_Sviluppo_Web_e_Database`.

## 1. Diagramma ER (Schema Database)

Il database SQLite è composto da quattro tabelle principali con relazioni per gestire i messaggi, i contenuti e l'accesso sicuro.

```mermaid
erDiagram
    CATEGORIES ||--o{ PROJECTS : "contiene"
    USER ||--o{ CONTACTS : "gestisce (opzionale)"
    
    USER {
        int id PK
        string username
        string password_hash
    }
    CONTACTS {
        int id PK
        string name
        string email
        string message
        boolean is_favorite
        datetime created_at
        int user_id FK
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
```

## 2. Diagramma UML delle Classi

L'applicazione segue il **Repository Pattern**. Tutte le rotte sono protette tramite il blueprint di autenticazione.

```mermaid
classDiagram
    class UserRepository {
        +create_user(username, hash)
        +get_user_by_id(id)
        +get_user_by_username(user)
    }
    class ContactRepository {
        +create_contact(name, email, message)
        +get_all_contacts(search, favorite)
        +toggle_favorite(id)
    }
    class ProjectRepository {
        +get_all_projects()
        +create_project(data)
    }
    class Auth_Blueprint {
        +login()
        +register()
        +logout()
        +login_required(view)
    }
    class API_Blueprint {
        +add_contact()
        +get_contacts()
        +toggle_favorite()
    }
    
    API_Blueprint ..> ContactRepository : usa
    API_Blueprint ..> Auth_Blueprint : richiede
    Auth_Blueprint ..> UserRepository : usa
```

## 3. Casi d'Uso

Il sistema prevede due attori principali: il Visitatore e l'Amministratore del portfolio.

```mermaid
graph LR
    subgraph "Portfolio System"
        UC1(Invia Messaggio)
        UC2(Visualizza Progetti)
        UC3(Gestione Inbox)
        UC4(Cerca Messaggi)
        UC5(Segna come Preferito)
        UC6(Login/Logout)
    end

    V[Visitatore] --> UC1
    V --> UC2
    A[Amministratore] --> UC3
    A --> UC4
    A --> UC5
    A --> UC6
```


