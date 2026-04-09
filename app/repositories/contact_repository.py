from app.db import get_db

def create_contact(name, email, message):
    db = get_db()
    db.execute(
        'INSERT INTO contacts (name, email, message) VALUES (?, ?, ?)',
        (name, email, message)
    )
    db.commit()

def get_all_contacts(search_query=None, favorite_only=False):
    db = get_db()
    query = 'SELECT id, name, email, message, is_favorite, created_at FROM contacts WHERE 1=1'
    params = []

    if favorite_only:
        query += ' AND is_favorite = 1'
    
    if search_query:
        query += ' AND (name LIKE ? OR email LIKE ? OR message LIKE ?)'
        wildcard = f'%{search_query}%'
        params.extend([wildcard, wildcard, wildcard])

    query += ' ORDER BY created_at DESC'
    return db.execute(query, params).fetchall()

def toggle_favorite(contact_id):
    db = get_db()
    db.execute(
        'UPDATE contacts SET is_favorite = NOT is_favorite WHERE id = ?',
        (contact_id,)
    )
    db.commit()
