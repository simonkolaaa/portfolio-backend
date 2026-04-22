"""
Arus AI - Modulo standalone per PythonAnywhere
Chiama l'API REST di Google Gemini direttamente con requests.
Zero dipendenze pesanti: niente LangChain, niente ChromaDB, niente SDK Google.
"""
import os
import json
import requests as http_requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# --- CONTESTO SU SIMON (solo info pubbliche) ---
SIMON_CONTEXT = """
INFORMAZIONI PUBBLICHE SU SIMON KOLA:
- Studente di informatica presso ISISS "P. Gobetti - A. De Gasperi".
- Competenze principali: Python, Flask, HTML/CSS, JavaScript, SQL.
- Soft skills: Collaborazione, Creatività, Problem Solving, Adattabilità.
- Profilo GitHub: github.com/simonkolaaa
- Sito portfolio ufficiale: simonkolaaa.github.io
- Progetti principali: portfolio-backend (questo sito), checkfeed-bot, jarvis, board-games-app.
- Appassionato di sviluppo web e backend, interessato a DevOps e AI.

SEZIONI DEL PORTFOLIO (per guidare la navigazione):
- Home: presentazione e competenze
- Progetti: elenco dei progetti con descrizioni e link GitHub
- Contatti: form per inviare un messaggio a Simon
- GitHub: github.com/simonkolaaa per vedere tutto il codice
"""

# --- SYSTEM PROMPT FOCALIZZATO ---
ARUS_SYSTEM_PROMPT = f"""Sei Arus, l'assistente AI del portfolio personale di Simon Kola.
Il tuo unico scopo è aiutare i visitatori a:
1. Conoscere Simon: le sue competenze, i suoi progetti e il suo percorso di studio.
2. Navigare il portfolio: indicare le sezioni disponibili (Home, Progetti, Contatti, GitHub).
3. Rispondere a domande sui progetti di Simon o sul suo stack tecnologico.

REGOLE ASSOLUTE:
- Rispondi SOLO a domande che riguardano Simon Kola, il suo portfolio o i suoi progetti.
- Se la domanda è fuori tema (matematica, politica, cucina, ecc.) rispondi ESATTAMENTE: "Sono qui solo per parlarti di Simon e del suo portfolio! Hai qualche domanda su di lui o sui suoi progetti?"
- Non rivelare MAI dati privati: nessuna password, nessun indirizzo fisico, nessun numero di telefono.
- Parla di Simon sempre in terza persona, con tono amichevole e professionale.
- Risposte brevi e dirette: massimo 3-4 frasi.
- Indirizza sempre verso il sito ufficiale: simonkolaaa.github.io

{SIMON_CONTEXT}
"""

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def ask_arus(user_message: str) -> str:
    """
    Chiama Gemini generateContent (non streaming).
    Compatibile con PythonAnywhere WSGI.
    Restituisce la risposta come stringa o un messaggio di errore.
    """
    if not GOOGLE_API_KEY:
        return "Arus non è disponibile al momento (chiave API mancante)."

    url = f"{BASE_URL}/{GEMINI_MODEL}:generateContent?key={GOOGLE_API_KEY}"

    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_message}]
            }
        ],
        "systemInstruction": {
            "parts": [{"text": ARUS_SYSTEM_PROMPT}]
        },
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 300,
        }
    }

    try:
        response = http_requests.post(url, json=payload, timeout=30)
        if response.status_code != 200:
            return f"Arus non è disponibile al momento. Riprova tra poco!"

        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            return "Non ho trovato una risposta. Prova a riformulare la domanda!"

        parts = candidates[0].get("content", {}).get("parts", [])
        text = "".join(p.get("text", "") for p in parts).strip()
        return text if text else "Non ho capito la domanda. Puoi ripetere?"

    except http_requests.exceptions.Timeout:
        return "La risposta sta tardando troppo. Riprova tra qualche secondo!"
    except Exception:
        return "Si è verificato un errore imprevisto. Riprova!"
