import os
from flask import Flask
from flask_cors import CORS

def create_app():
    # Mantiene la tipica Factory Pattern che avevi usato a scuola
    app = Flask(__name__, instance_relative_config=True)
    
    # Aggiungiamo i CORS per permettere al Frontend React di contattare Flask
    CORS(app) 

    app.config.from_mapping(
        SECRET_KEY='portfolio-secret',
        DATABASE=os.path.join(app.instance_path, 'portfolio.sqlite'),
    )

    from . import db
    db.init_app(app)

    # Invece di 'main' e 'auth', registriamo un blueprint per le 'api'
    from . import api
    app.register_blueprint(api.bp)

    return app
