"""
Arus AI - Modulo standalone per PythonAnywhere
Chiama l'API REST di Google Gemini direttamente con requests.
Zero dipendenze pesanti: niente LangChain, niente ChromaDB, niente SDK Google.
"""
import os
import time
import json
import requests as http_requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()

# Modelli in ordine di preferenza — il primo disponibile viene usato
GEMINI_MODELS = [
    os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
]

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
- Se la domanda è fuori tema rispondi ESATTAMENTE: "Sono qui solo per parlarti di Simon e del suo portfolio! Hai qualche domanda su di lui o sui suoi progetti?"
- Non rivelare MAI dati privati: nessuna password, nessun indirizzo fisico, nessun numero di telefono.
- Parla di Simon sempre in terza persona, con tono amichevole e professionale.
- Risposte brevi e dirette: massimo 3-4 frasi.
- Indirizza sempre verso il sito ufficiale: simonkolaaa.github.io

{SIMON_CONTEXT}
"""

BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"


def _call_model(model: str, user_message: str) -> tuple[int, str]:
    """
    Chiama un singolo modello Gemini.
    Restituisce (status_code, testo_risposta).
    """
    url = f"{BASE_URL}/{model}:generateContent?key={GOOGLE_API_KEY}"
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

    response = http_requests.post(url, json=payload, timeout=45)
    if response.status_code == 200:
        data = response.json()
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            text = "".join(p.get("text", "") for p in parts).strip()
            return 200, text
        return 200, ""
    return response.status_code, response.text


def ask_arus(user_message: str) -> str:
    """
    Chiama Gemini con fallback automatico tra modelli.
    Compatibile con PythonAnywhere WSGI (niente streaming).
    """
    if not GOOGLE_API_KEY:
        return "Arus non è disponibile al momento (configurazione mancante)."

    for model in GEMINI_MODELS:
        try:
            status, text = _call_model(model, user_message)

            if status == 200:
                return text if text else "Non ho capito la domanda. Puoi ripetere?"

            if status == 503:
                # Modello sovraccarico: aspetta e riprova una volta
                time.sleep(2)
                status, text = _call_model(model, user_message)
                if status == 200:
                    return text if text else "Non ho capito la domanda. Puoi ripetere?"
                # Se ancora 503, prova il prossimo modello
                continue

            if status == 429:
                # Quota esaurita su questo modello: prova il prossimo
                continue

            # Qualsiasi altro errore: prova il prossimo modello
            continue

        except http_requests.exceptions.Timeout:
            continue
        except Exception:
            continue

    return "Arus non è disponibile al momento. Riprova tra qualche istante!"
