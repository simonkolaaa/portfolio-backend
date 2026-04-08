"""
Arus AI - Modulo standalone per PythonAnywhere
Chiama l'API REST di Google Gemini direttamente con requests.
Zero dipendenze pesanti: niente LangChain, niente ChromaDB, niente SDK Google.
"""
import os
import requests as http_requests
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# Contesto statico su Simon
SIMON_CONTEXT = """
INFORMAZIONI SU SIMON KOLA:
- Simon Kola è uno studente di informatica appassionato di sviluppo web e backend.
- Competenze principali: Python (85%), Flask (75%), HTML/CSS (90%), JavaScript (80%), SQL (70%).
- Soft skills: Collaborazione, Creatività, Empatia, Problem Solving, Adattabilità.
- Profili GitHub: github.com/simonkolaaa e github.com/SimonKolaa
- Progetti principali: portfolio-backend, checkfeed-bot, jarvis, Repo5M, Progetto_5M, board-games-app
- Sito portfolio ufficiale: simonkolaaa.github.io
- Email: simonkola21@gmail.com
- Simon è appassionato di tecnologia e vuole cambiare il mondo con il codice.
- Frequenta l'ISISS "P. Gobetti - A. De Gasperi".
- Studia Python, Flask, HTML, JS, JSON e vari strumenti DevOps.
- Ha collaborato a diversi progetti in team, sviluppando logiche backend in Python (Flask) e interfacce web responsive.
"""

ARUS_SYSTEM_PROMPT = f"""Sei Arus, l'assistente AI universale e portavoce ufficiale di Simon.
Se gli utenti ti fanno domande su Simon, tu parli di lui in terza persona esponendo le sue competenze e i suoi progetti. Indirizza sempre gli utenti al suo sito ufficiale: "simonkolaaa.github.io".
ATTENZIONE: Proteggi sempre la privacy di Simon, non esporre mai dati sensibili come password o indirizzi personali.
Oltre ad essere il suo portavoce, sei un assistente incredibilmente intelligente e puoi rispondere a QUALSIASI ALTRA DOMANDA generale.

{SIMON_CONTEXT}
"""

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:streamGenerateContent"


def stream_arus(user_message: str):
    """Genera una risposta in streaming chiamando direttamente l'API REST di Gemini."""
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
            "temperature": 0.7,
        }
    }

    response = http_requests.post(
        f"{API_URL}?alt=sse&key={GOOGLE_API_KEY}",
        json=payload,
        stream=True,
        timeout=60
    )

    if response.status_code != 200:
        yield f"Errore API Gemini ({response.status_code}): {response.text[:200]}"
        return

    import json
    for line in response.iter_lines(decode_unicode=True):
        if line and line.startswith("data: "):
            try:
                data = json.loads(line[6:])
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    for part in parts:
                        text = part.get("text", "")
                        if text:
                            yield text
            except (json.JSONDecodeError, KeyError, IndexError):
                continue
