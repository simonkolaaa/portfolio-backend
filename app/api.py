from flask import Blueprint, request, jsonify
from app.repositories import contact_repository
import logging

# Configurazione log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint per le rotte API
bp = Blueprint('api', __name__, url_prefix='/api')

# --- ROTTE CONTATTI (Sistema SQLite Blindato) ---

@bp.route('/contact', methods=['POST'])
def add_contact():
    """Riceve un messaggio dal form contatti e lo salva su SQLite."""
    logger.info("Ricevuta richiesta per /api/contact")
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Dati mancanti"}), 400

    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    if not name or not email or not message:
        return jsonify({"error": "Tutti i campi sono obbligatori."}), 400
        
    try:
        contact_repository.create_contact(name, email, message)
        logger.info(f"Messaggio ricevuto correttamente da {email}")
        return jsonify({"success": "Messaggio ricevuto con successo!"}), 201
    except Exception as e:
        logger.error(f"Errore SQLite: {str(e)}")
        return jsonify({"error": f"Errore database: {str(e)}"}), 500

@bp.route('/contacts', methods=['GET'])
def get_contacts():
    """Ritorna tutti i messaggi (per test)."""
    try:
        contacts = contact_repository.get_all_contacts()
        response = jsonify([dict(c) for c in contacts])
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Nota: La rotta Arus AI è stata rimossa per massimizzare la stabilità del server.
# Il codice di logica rimane disponibile nella cartella 'core/' per usi futuri.
