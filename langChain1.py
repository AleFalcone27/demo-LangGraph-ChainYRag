from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv() 

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    reasoning_effort="low",
    temperature=1,
    max_tokens=150,
)

prompt = PromptTemplate.from_template("Explain {topic} in two sentences.")

chain = prompt | llm | StrOutputParser()


print(chain.invoke({"topic": "Stefanini"}))
