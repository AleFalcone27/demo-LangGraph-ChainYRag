from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

load_dotenv() 

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    reasoning_effort="low",
    temperature=0,
    max_tokens=60
)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Sos un analista de empresas. Respondé en español, de forma breve "
        ),
        ("human", "Explicá {topic} en dos oraciones."),
    ]
)

chain = prompt | llm | StrOutputParser() | 

print(chain.invoke({"topic": "Stefanini"}))
