from flask import Blueprint, request, jsonify, render_template
from app.repositories import contact_repository
from app.auth import login_required
import logging
import time
from collections import defaultdict

# Configurazione log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Blueprint per le rotte API
bp = Blueprint('api', __name__, url_prefix='/api')

# --- RATE LIMITER IN MEMORIA (anti-spam Arus) ---
# Struttura: { "ip": [timestamp1, timestamp2, ...] }
_rate_store = defaultdict(list)
RATE_LIMIT = 10       # max richieste
RATE_WINDOW = 60      # in secondi

def _is_rate_limited(ip: str) -> bool:
    """Restituisce True se l'IP ha superato il limite di richieste."""
    now = time.time()
    # Mantieni solo i timestamp nell'ultima finestra
    _rate_store[ip] = [t for t in _rate_store[ip] if now - t < RATE_WINDOW]
    if len(_rate_store[ip]) >= RATE_LIMIT:
        return True
    _rate_store[ip].append(now)
    return False


# --- ROTTE CONTATTI ---

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
@login_required
def get_contacts():
    """Ritorna la Dashboard HTML con tutti i messaggi ricevuti (filtri supportati)."""
    search_query = request.args.get('search')
    favorite_filter = request.args.get('filter') == 'favorites'
    
    try:
        contacts = contact_repository.get_all_contacts(
            search_query=search_query, 
            favorite_only=favorite_filter
        )
        return render_template('contacts.html', contacts=contacts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/contacts/<int:contact_id>/toggle-favorite', methods=['POST'])
@login_required
def toggle_favorite(contact_id):
    """Sposta o rimuove un contatto dai preferiti."""
    try:
        contact_repository.toggle_favorite(contact_id)
        return jsonify({"success": "Stato preferito aggiornato"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- ROTTA ARUS AI ---

@bp.route('/arus', methods=['POST'])
def arus_chat():
    """
    Endpoint chat Arus.
    Riceve { "message": "..." } e restituisce { "reply": "..." }.
    Protetto da rate limiting per IP.
    """
    # Rate limiting
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip:
        ip = ip.split(',')[0].strip()  # prende il primo IP in caso di proxy
    
    if _is_rate_limited(ip):
        logger.warning(f"Rate limit raggiunto per IP: {ip}")
        return jsonify({"error": "Troppe richieste. Aspetta un momento prima di scrivere ancora."}), 429

    # Validazione input
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Richiesta non valida."}), 400

    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({"error": "Il messaggio non può essere vuoto."}), 400

    if len(user_message) > 500:
        return jsonify({"error": "Messaggio troppo lungo (max 500 caratteri)."}), 400

    # Chiama Arus
    try:
        from arus_brain import ask_arus
        logger.info(f"Richiesta Arus da {ip}: {user_message[:60]}...")
        reply = ask_arus(user_message)
        return jsonify({"reply": reply}), 200
    except Exception as e:
        logger.error(f"Errore Arus: {str(e)}")
        return jsonify({"error": "Arus non è disponibile al momento."}), 500
