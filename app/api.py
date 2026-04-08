from flask import Blueprint, request, jsonify, Response
from app.repositories import contact_repository
import json

# Blueprint per le rotte API
bp = Blueprint('api', __name__, url_prefix='/api')

# --- ROTTE CONTATTI (Portfolio) ---

@bp.route('/contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    if not name or not email or not message:
        return jsonify({"error": "Tutti i campi sono obbligatori."}), 400
        
    try:
        contact_repository.create_contact(name, email, message)
        return jsonify({"success": "Messaggio ricevuto con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/contacts', methods=['GET'])
def get_contacts():
    # Rotta per leggere tutti i messaggi ricevuti (test) con fix per cache PythonAnywhere
    contacts = contact_repository.get_all_contacts()
    response = jsonify([dict(c) for c in contacts])
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response, 200


# --- ROTTA ARUS AI (Reintegrata) ---

@bp.route('/chat/arus', methods=['POST'])
def chat_arus():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Nessun messaggio fornito'}), 400

    user_message = data['message']

    def generate():
        try:
            from arus_brain import stream_arus
            for chunk in stream_arus(user_message):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'chunk': f'Errore: {str(e)}'})}\n\n"
        yield "data: {}\n\n"

    return Response(generate(), mimetype='text/event-stream')
