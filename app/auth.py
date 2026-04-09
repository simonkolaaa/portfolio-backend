import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories import user_repository

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    """Decoratore per proteggere le rotte che richiedono l'autenticazione."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # Se la richiesta accetta HTML (richiesta da browser), facciamo redirect.
            # Altrimenti (richiesta API pura), restituiamo 401 Unauthorized.
            if 'text/html' in request.headers.get('Accept', ''):
                return redirect(url_for('auth.login'))
            return jsonify({"error": "Autenticazione richiesta"}), 401
        return view(**kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """Carica l'utente loggato dalla sessione prima di ogni richiesta."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = user_repository.get_user_by_id(user_id)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Gestisce la registrazione di un nuovo utente."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username richiesto.'
        elif not password:
            error = 'Password richiesta.'

        if error is None:
            hashed_pw = generate_password_hash(password)
            if user_repository.create_user(username, hashed_pw):
                return redirect(url_for('auth.login'))
            else:
                error = f"L'utente {username} è già registrato."

        return render_template('auth.html', error=error, mode='register')

    return render_template('auth.html', mode='register')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Gestisce l'accesso dell'utente."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = user_repository.get_user_by_username(username)

        if user is None:
            error = 'Username errato.'
        elif not check_password_hash(user['password'], password):
            error = 'Password errata.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('api.get_contacts'))

        return render_template('auth.html', error=error, mode='login')

    return render_template('auth.html', mode='login')

@bp.route('/logout')
def logout():
    """Effettua il logout dell'utente."""
    session.clear()
    return redirect(url_for('auth.login'))
