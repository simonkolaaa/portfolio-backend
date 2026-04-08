from flask import Blueprint, request, jsonify, Response
from app.repositories import contact_repository
import json
import logging
import os

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
        return jsonify({"success": "Messaggio ricevuto con successo!"}), 201
    except Exception as e:
        logger.error(f"Errore SQLite: {str(e)}")
        return jsonify({"error": f"Errore database: {str(e)}"}), 500

@bp.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        contacts = contact_repository.get_all_contacts()
        response = jsonify([dict(c) for c in contacts])
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        return response, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ROTTA ARUS AI (Integrata Jarvis-2 con isolamento) ---

@bp.route('/chat/arus', methods=['POST'])
def chat_arus():
    """Interfaccia per Arus AI con caricamento pigro dei moduli core."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Nessun messaggio fornito'}), 400

    user_message = data['message']

    def generate():
        try:
            # Fix per SQLite vecchio su PythonAnywhere (necessario per ChromaDB)
            try:
                __import__('pysqlite3')
                import sys
                sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
            except Exception:
                pass

            # Import dinamico: se core fallisce, il form contatti continua a funzionare
            try:
                import config
                from core.brain import stream_ai
                from core.memory import get_vectorstore, get_relevant_context
            except ImportError as e:
                logger.error(f"Moduli IA non disponibili: {e}")
                yield f"data: {json.dumps({'chunk': 'Errore: Sistema AI non disponibile in questo ambiente.'})}\n\n"
                return

            # Gestione Memoria RAG
            context = "Simon Kola è un programmatore specializzato in Flask, Python e React."
            try:
                vs = get_vectorstore(config.CHROMA_JARVIS_DIR)
                if vs:
                    rag_context = get_relevant_context(user_message, vs, top_k=config.JARVIS_RAG_TOP_K)
                    if rag_context:
                        context += "\n\n" + rag_context
            except Exception:
                pass

            # Streaming
            for chunk in stream_ai("arus", user_message, context):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        
        except Exception as e:
            logger.error(f"Errore streaming IA: {e}")
            yield f"data: {json.dumps({'chunk': f'Errore tecnico: {str(e)}'})}\n\n"
        
        yield "data: {}\n\n"

    return Response(generate(), mimetype='text/event-stream')
 burial_of_the_dead = """
