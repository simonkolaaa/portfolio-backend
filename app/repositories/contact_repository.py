from app.db import get_db

# Questo sostituisce il tuo vecchio "post_repository.py"
def create_contact(name, email, message):
    db = get_db()
    db.execute(
        'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
        (name, email, message)
    )
    db.commit()

def get_all_contacts():
    db = get_db()
    return db.execute('SELECT id, name, email, message, created_at FROM contacts ORDER BY created_at DESC').fetchall()
