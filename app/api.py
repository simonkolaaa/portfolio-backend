from flask import Blueprint, request, jsonify
from app.repositories import contact_repository

# Blueprint per le rotte API, che sostituisce il tuo vecchio "main.py"
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/contact', methods=['POST'])
def add_contact():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    if not name or not email or not message:
        return jsonify({"error": "Tutti i campi sono obbligatori."}), 400
        
    try:
        # Usiamo il repository per tenere il codice pulito (stessa tecnica usata a scuola)
        contact_repository.create_contact(name, email, message)
        return jsonify({"success": "Messaggio ricevuto con successo!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/contacts', methods=['GET'])
def get_contacts():
    # Rotta per leggere tutti i messaggi ricevuti (solo a scopo di test)
    contacts = contact_repository.get_all_contacts()
    return jsonify([dict(c) for c in contacts]), 200
