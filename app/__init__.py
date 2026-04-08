import os
from flask import Flask
from flask_cors import CORS

def create_app():
    # Factory Pattern
    app = Flask(__name__, instance_relative_config=True)
    
    # Configurazione CORS esplicita per autorizzare il frontend
    CORS(app, resources={r"/api/*": {"origins": ["https://simonkolaaa.github.io", "http://localhost:3000"]}}) 

    app.config.from_mapping(
        SECRET_KEY='portfolio-secret',
        DATABASE=os.path.join(app.instance_path, 'portfolio.sqlite'),
    )

    from . import db
    db.init_app(app)

    # Registriamo il blueprint per le API
    from . import api
    app.register_blueprint(api.bp)

    return app
