import sqlite3
import os
from flask import current_app, g

def get_db():
    """Restituisce la connessione al database per la richiesta corrente."""
    if 'db' not in g:
        db_path = current_app.config['DATABASE']
        # Assicuriamoci che la cartella 'instance' esista, altrimenti sqlite3 fallisce
        db_dir = os.path.dirname(db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        g.db = sqlite3.connect(
            db_path,
            isolation_level=None # Forza l'autocommit per SQLite su PythonAnywhere
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """Chiude la connessione alla fine della richiesta."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """Registra la funzione di chiusura automatica."""
    app.teardown_appcontext(close_db)