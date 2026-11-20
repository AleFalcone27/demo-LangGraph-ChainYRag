from typing import TypedDict

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-20b", reasoning_effort="low", temperature=0, )

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sos un analista de empresas. Respondé en español, de forma breve "
        ),
        ("human", "Explicá {topic} en dos oraciones."),
    ]
)

# Cada intento permite más tokens que el anterior.
LIMITES_DE_TOKENS = [60, 150, 400]


# 1. Estado compartido: todos los nodos leen y actualizan este diccionario.
class Estado(TypedDict):
    topic: str
    respuesta: str
    intentos: int


# 2. Nodos: funciones que reciben el estado y devuelven los campos que cambian.
def generar(estado: Estado) -> dict:
    intento = estado["intentos"]
    limite = LIMITES_DE_TOKENS[intento]
    print(f"Intento {intento + 1}: max_tokens={limite}")

    chain = prompt | llm.bind(max_tokens=limite) | StrOutputParser()
    respuesta = chain.invoke({"topic": estado["topic"]})
    return {"respuesta": respuesta, "intentos": intento + 1}


def presentar(estado: Estado) -> dict:
    print(f"\nRespuesta final ({estado['intentos']} intento/s):")
    print(estado["respuesta"])
    return {}


# 3. Arista condicional: decide qué nodo sigue según el estado.
def decidir(estado: Estado) -> str:
    texto = estado["respuesta"].rstrip()
    esta_completa = texto.endswith((".", "!", "?"))
    sin_intentos = estado["intentos"] >= len(LIMITES_DE_TOKENS)
    if esta_completa or sin_intentos:
        return "presentar"
    print("  -> respuesta cortada, reintento con más tokens")
    return "generar"


# 4. Armado del grafo: START -> generar -> (presentar | generar) -> END
grafo = StateGraph(Estado)
grafo.add_node("generar", generar)
grafo.add_node("presentar", presentar)
grafo.add_edge(START, "generar")
grafo.add_conditional_edges("generar", decidir, ["generar", "presentar"])
grafo.add_edge("presentar", END)

app = grafo.compile()

app.invoke({"topic": "Stefanini", "respuesta": "", "intentos": 0})

