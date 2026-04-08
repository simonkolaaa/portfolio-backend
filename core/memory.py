from pathlib import Path
from typing import Optional, List

# Cerchiamo di importare langchain, ma rendiamo il modulo resiliente se manca
try:
    from langchain_community.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_chroma import Chroma
    from langchain_ollama import OllamaEmbeddings
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

import config

def load_documents_from_paths(paths: List[Path]) -> list:
    if not LANGCHAIN_AVAILABLE: return []
    documents = []
    for folder in paths:
        if not folder or not folder.exists(): continue
        supported_files = []
        for ext in ["*.txt", "*.pdf", "*.docx", "*.md"]:
            supported_files.extend(folder.glob(ext))
        for file_path in supported_files:
            try:
                suffix = file_path.suffix.lower()
                if suffix in [".txt", ".md"]:
                    loader = TextLoader(str(file_path), encoding="utf-8")
                elif suffix == ".pdf":
                    loader = PyPDFLoader(str(file_path))
                elif suffix == ".docx":
                    loader = Docx2txtLoader(str(file_path))
                else:
                    continue
                docs = loader.load()
                documents.extend(docs)
            except Exception:
                continue
    return documents

def split_documents(documents: list) -> list:
    if not LANGCHAIN_AVAILABLE or not documents: return []
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)

def get_vectorstore(persist_dir: Path, chunks: list = None) -> Optional['Chroma']:
    if not LANGCHAIN_AVAILABLE: return None
    embeddings = OllamaEmbeddings(model=config.EMBEDDING_MODEL)
    str_persist_dir = str(persist_dir)
    if chunks:
        try:
            return Chroma.from_documents(
                documents=chunks,
                embedding=embeddings,
                persist_directory=str_persist_dir,
                collection_name="rag_memory",
            )
        except Exception:
            return None
    if persist_dir.exists() and any(persist_dir.iterdir()):
        try:
            return Chroma(
                persist_directory=str_persist_dir,
                embedding_function=embeddings,
                collection_name="rag_memory",
            )
        except Exception:
            pass
    return None

def get_relevant_context(query: str, vectorstore: 'Chroma', top_k: int = 4) -> str:
    if not LANGCHAIN_AVAILABLE or vectorstore is None: return ""
    try:
        retriever = vectorstore.as_retriever(search_kwargs={"k": top_k})
        docs = retriever.invoke(query)
        if not docs: return ""
        parts = [f"[- {Path(d.metadata.get('source', '')).name}]\n{d.page_content}" for d in docs]
        return "\n\n".join(parts)
    except Exception:
        return ""
