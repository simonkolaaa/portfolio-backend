import functools
import secrets
from flask import Blueprint, g, redirect, render_template, request, session, url_for, Response
from werkzeug.security import check_password_hash, generate_password_hash
from app.repositories import user_repository

bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    """Decoratore per proteggere le rotte che richiedono l'autenticazione."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # Per semplicità e sicurezza, se non sei loggato ti mandiamo sempre al login
            return redirect(url_for('auth.login'))
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


# --- CALLBACK OAUTH ---

def _oauth_login_or_create(username: str) -> Response:
    """Helper: cerca o crea l'utente OAuth nel DB e imposta la sessione."""
    user = user_repository.get_user_by_username(username)
    if user is None:
        # Crea l'utente OAuth con una password casuale inutilizzabile
        dummy_hash = generate_password_hash(secrets.token_hex(32))
        user_repository.create_user(username, dummy_hash)
        user = user_repository.get_user_by_username(username)
    session.clear()
    session['user_id'] = user['id']
    return redirect(url_for('api.get_contacts'))

@bp.route('/oauth/google/callback')
def oauth_google_callback():
    """Callback dopo il login Google. Legge email e crea/trova l'utente."""
    from flask_dance.contrib.google import google  # type: ignore[import-untyped]
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return redirect(url_for('auth.login'))
    email = resp.json().get("email", "")
    return _oauth_login_or_create(f"google:{email}")

@bp.route('/oauth/github/callback')
def oauth_github_callback():
    """Callback dopo il login GitHub. Legge username e crea/trova l'utente."""
    from flask_dance.contrib.github import github  # type: ignore[import-untyped]
    if not github.authorized:
        return redirect(url_for('github.login'))
    resp = github.get("/user")
    if not resp.ok:
        return redirect(url_for('auth.login'))
    login = resp.json().get("login", "")
    return _oauth_login_or_create(f"github:{login}")
