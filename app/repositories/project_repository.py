from app.db import get_db

def get_all_projects():
    db = get_db()
    return db.execute(
        'SELECT p.id, p.title, p.description, p.url, c.name as category_name '
        'FROM projects p JOIN categories c ON p.category_id = c.id'
    ).fetchall()

def create_project(title, description, category_name, url=None):
    db = get_db()
    # Trova o crea la categoria
    category = db.execute('SELECT id FROM categories WHERE name = ?', (category_name,)).fetchone()
    if not category:
        db.execute('INSERT INTO categories (name) VALUES (?)', (category_name,))
        db.commit()
        category = db.execute('SELECT id FROM categories WHERE name = ?', (category_name,)).fetchone()
    
    db.execute(
        'INSERT INTO projects (title, description, url, category_id) VALUES (?, ?, ?, ?)',
        (title, description, url, category['id'])
    )
    db.commit()
