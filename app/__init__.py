import os
from flask import Flask, jsonify
from flask_cors import CORS

def create_app():
    # Factory Pattern
    app = Flask(__name__, instance_relative_config=True)
    
    # CORS TOTALMENTE PERMISSIVO per evitare errori di rete sul frontend
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True) 

    app.config.from_mapping(
        SECRET_KEY='portfolio-secret',
        DATABASE=os.path.join(app.instance_path, 'portfolio.sqlite'),
    )

    # Gestore errori globale per le API: 
    # Anche se il server crasha (500), restituiamo JSON + CORS così il client capisce l'errore
    @app.errorhandler(500)
    def internal_error(error):
        response = jsonify({"error": "Errore interno del server", "details": str(error)})
        response.status_code = 500
        # Forziamo CORS anche sull'errore
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    from . import db
    db.init_app(app)

    # Registriamo il blueprint per le API
    from . import api
    app.register_blueprint(api.bp)

    return app
