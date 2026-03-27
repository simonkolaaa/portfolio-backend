import sqlite3
import os
from app import create_app

app = create_app()

with app.app_context():
    if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)

    db_path = app.config['DATABASE']
    connection = sqlite3.connect(db_path)

    with open('app/schema.sql') as f:
        connection.executescript(f.read())

    print("Database portfolio.sqlite inizializzato con successo in:", db_path)
    connection.close()
