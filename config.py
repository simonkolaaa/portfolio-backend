import os
from pathlib import Path

# --- CONFIGURAZIONE CORE (Jarvis-2) ---
# Modalità di default: "online" (Gemini) o "offline" (Ollama)
MODE = "online"

# Modelli
OFFLINE_MODEL = "mistral"
ONLINE_MODEL = "gemini-2.0-flash"
EMBEDDING_MODEL = "nomic-embed-text"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "inserisci_tua_chiave_qui")

# Percorsi Memory (RAG)
BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
CHROMA_DIR = INSTANCE_DIR / "chroma"

CHROMA_JARVIS_DIR = CHROMA_DIR / "jarvis_db"
CHROMA_LINDA_DIR = CHROMA_DIR / "linda_db"

DATA_PUBLIC_DIR = BASE_DIR / "data" / "public"
DATA_PRIVATE_DIR = BASE_DIR / "data" / "private"
SCUOLA_PATH = None
LINDA_EXTRA_PATHS = []

# RAG Settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
JARVIS_RAG_TOP_K = 4

# PROMPTS
JARVIS_PROMPT = """Sei Jarvis, un assistente AI avanzato. 
Usa il seguente contesto per rispondere: 
{context}
"""

LINDA_PROMPT = """Sei Linda, l'assistente privata di Simon.
Contesto: {context}
"""

ARUS_PROMPT = """Sei Arus, l'assistente AI ufficiale del Portfolio di Simon Kola.
Parla di Simon in terza persona. Indirizza sempre a simonkolaaa.github.io.
Contesto: {context}
"""

# --- CONFIGURAZIONE DATABASE SQLITE (Form Contatti) ---
DATABASE = os.path.join(INSTANCE_DIR, 'portfolio.sqlite')
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
