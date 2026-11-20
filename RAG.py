from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()  # carga GROQ_API_KEY desde el archivo .env

# Documento sobre el que el modelo va a responder.
DOCUMENTO = Path(__file__).parent / "resumen_langchain_langgraph.md"

# ---------------------------------------------------------------------------
# 1. Preparación (se hace una sola vez)
# ---------------------------------------------------------------------------

# Partir el texto en fragmentos chicos, con un poco de solapamiento.
texto = DOCUMENTO.read_text(encoding="utf-8")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
fragmentos = splitter.create_documents([texto])

# Modelo de embeddings local
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# Base vectorial en memoria: guarda cada fragmento junto con su embedding.
base = InMemoryVectorStore.from_documents(fragmentos, embeddings)

# Retriever: dada una pregunta, devuelve los 3 fragmentos más parecidos.
retriever = base.as_retriever(search_kwargs={"k": 3})

# ---------------------------------------------------------------------------
# 2. La cadena RAG (se ejecuta en cada pregunta)
# ---------------------------------------------------------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    reasoning_effort="low",
    temperature=0,
    max_tokens=500,
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Respondé en español, de forma breve, usando solo el contexto. "
            "Si el contexto no tiene la respuesta, decí que el documento no incluye "
            "esa información.\n\n"
            "Contexto:\n{contexto}",
        ),
        ("human", "{pregunta}"),
    ]
)


# El retriever devuelve una lista de Document, pero el prompt espera un solo
# texto en {contexto}. Esta función junta el contenido de los fragmentos
# recuperados, separados por una línea en blanco. Se descartan los metadatos.
def unir_fragmentos(documentos) -> str:
    return "\n\n".join(doc.page_content for doc in documentos)


# La pregunta va al retriever (para buscar el contexto) y también al prompt.
chain = (
    {"contexto": retriever | unir_fragmentos, "pregunta": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


preguntas = [
        "¿Cuál es la diferencia principal entre LangChain y LangGraph?",
        "¿Cuántos empleados tiene Stefanini?",  # no está en el documento
    ]
for pregunta in preguntas:
        print(f"\nPregunta: {pregunta}")
        print("Fragmentos recuperados (similitud coseno, más alto = más parecido):")
        for doc, score in base.similarity_search_with_score(pregunta, k=3):
            print(f"  - [{score:.4f}] {doc.page_content[:80].strip()!r}...")
        print(f"Respuesta: {chain.invoke(pregunta)}")
