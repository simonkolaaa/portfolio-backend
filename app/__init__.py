import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.github import make_github_blueprint
import config

def create_app():
    # Factory Pattern
    app = Flask(__name__, instance_relative_config=True)
    
    # CORS TOTALMENTE PERMISSIVO
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True) 

    # Carichiamo la configurazione dal file config.py unificato
    app.config.from_object(config)

    # Su PythonAnywhere siamo dietro un proxy HTTPS — Flask-Dance richiede questa flag
    app.config['OAUTHLIB_RELAX_TOKEN_SCOPE'] = True
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'  # forza HTTPS in produzione

    @app.errorhandler(500)
    def internal_error(error):
        response = jsonify({"error": "Errore interno del server", "details": str(error)})
        response.status_code = 500
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    from . import db
    db.init_app(app)

    # Chiave segreta per le sessioni (in produzione andrebbe in .env)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_key_portfolio_123')

    # --- Blueprint OAuth ---
    google_bp = make_google_blueprint(
        client_id=config.GOOGLE_CLIENT_ID,
        client_secret=config.GOOGLE_CLIENT_SECRET,
        scope=["openid", "https://www.googleapis.com/auth/userinfo.email"],
        redirect_to="auth.oauth_google_callback",
    )
    app.register_blueprint(google_bp, url_prefix="/auth/oauth")

    github_bp = make_github_blueprint(
        client_id=config.GITHUB_CLIENT_ID,
        client_secret=config.GITHUB_CLIENT_SECRET,
        redirect_to="auth.oauth_github_callback",
    )
    app.register_blueprint(github_bp, url_prefix="/auth/oauth")

    from . import auth
    app.register_blueprint(auth.bp)

    from . import api
    app.register_blueprint(api.bp)

    return app
