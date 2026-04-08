from flask import Blueprint, request, jsonify, Response
from app.repositories import contact_repository
import json
import logging

# Configurazione log di base per il debug su PythonAnywhere
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint per le rotte API
bp = Blueprint('api', __name__, url_prefix='/api')

# --- ROTTE CONTATTI (Portfolio) ---

@bp.route('/contact', methods=['POST'])
def add_contact():
    """Riceve un messaggio dal form contatti."""
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
        logger.error(f"Errore salvataggio contatto: {str(e)}")
        return jsonify({"error": f"Errore interno del database: {str(e)}"}), 500

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


# --- ROTTA ARUS AI (Design Resiliente) ---

@bp.route('/chat/arus', methods=['POST'])
def chat_arus():
    """Interfaccia per Arus AI in streaming."""
    logger.info("Ricevuta richiesta per /api/chat/arus")
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Nessun messaggio fornito'}), 400

    user_message = data['message']

    def generate():
        try:
            # Import dinamico e fail-safe
            try:
                from arus_brain import stream_arus
            except ImportError as e:
                logger.error(f"Modulo arus_brain non trovato o errore dipendenze: {str(e)}")
                yield f"data: {json.dumps({'chunk': 'Errore: Sistema AI non disponibile (dipendenze mancanti).'})}\n\n"
                return

            for chunk in stream_arus(user_message):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        except Exception as e:
            logger.error(f"Errore durante lo streaming AI: {str(e)}")
            yield f"data: {json.dumps({'chunk': f'Spiacente, Arus ha riscontrato un problema tecnico: {str(e)}'})}\n\n"
        
        yield "data: {}\n\n"

    return Response(generate(), mimetype='text/event-stream')
