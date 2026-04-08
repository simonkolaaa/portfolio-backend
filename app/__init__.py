import os
from flask import Flask, jsonify
from flask_cors import CORS
import config

def create_app():
    # Factory Pattern
    app = Flask(__name__, instance_relative_config=True)
    
    # CORS TOTALMENTE PERMISSIVO
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True) 

    # Carichiamo la configurazione dal file config.py unificato
    app.config.from_object(config)

    @app.errorhandler(500)
    def internal_error(error):
        response = jsonify({"error": "Errore interno del server", "details": str(error)})
        response.status_code = 500
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    return app
