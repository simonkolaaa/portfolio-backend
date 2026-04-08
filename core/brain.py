from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import config

def get_llm(mode: str = None):
    mode = mode or config.MODE
    if mode == "offline":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=config.OFFLINE_MODEL, temperature=0.7)
    elif mode == "online":
        from langchain_google_genai import ChatGoogleGenerativeAI
        import os
        os.environ["GOOGLE_API_KEY"] = config.GOOGLE_API_KEY
        return ChatGoogleGenerativeAI(model=config.ONLINE_MODEL, temperature=0.7)
    raise ValueError(f"Modalità '{mode}' non riconosciuta.")

def ask_ai(persona: str, question: str, context: str = None) -> str:
    persona = persona.lower()
    if persona == "linda":
        mode = "offline"; system_prompt = config.LINDA_PROMPT
    elif persona == "arus":
        mode = "online"; system_prompt = config.ARUS_PROMPT
    else:
        mode = config.MODE; system_prompt = config.JARVIS_PROMPT

    formatted_prompt = system_prompt.format(context=context if context else "Al momento non hai ricordi specifici.")
    try:
        llm = get_llm(mode)
        prompt = ChatPromptTemplate.from_messages([("system", formatted_prompt), ("human", "{question}")])
        chain = prompt | llm | StrOutputParser()
        return chain.invoke({"question": question})
    except Exception as e:
        return f"❌ Errore: {str(e)}"

def stream_ai(persona: str, question: str, context: str = None):
    persona = persona.lower()
    if persona == "linda":
        mode = "offline"; system_prompt = config.LINDA_PROMPT
    elif persona == "arus":
        mode = "online"; system_prompt = config.ARUS_PROMPT
    else:
        mode = config.MODE; system_prompt = config.JARVIS_PROMPT

    formatted_prompt = system_prompt.format(context=context if context else "Al momento non hai ricordi specifici.")
    try:
        llm = get_llm(mode)
        prompt = ChatPromptTemplate.from_messages([("system", formatted_prompt), ("human", "{question}")])
        chain = prompt | llm | StrOutputParser()
        for chunk in chain.stream({"question": question}):
            yield chunk
    except Exception as e:
        yield f"❌ Errore: {str(e)}"
