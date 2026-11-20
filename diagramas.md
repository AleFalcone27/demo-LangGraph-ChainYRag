# Diagramas de los ejemplos

## Ejemplo 1: LangChain con prompt simple (langChain1.py)

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	PromptInput([PromptInput]):::first
	PromptTemplate(PromptTemplate)
	ChatGroq(ChatGroq)
	StrOutputParser(StrOutputParser)
	StrOutputParserOutput([StrOutputParserOutput]):::last
	PromptInput --> PromptTemplate;
	PromptTemplate --> ChatGroq;
	StrOutputParser --> StrOutputParserOutput;
	ChatGroq --> StrOutputParser;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

## Ejemplo 2: LangChain con rol de sistema (langChain2.py)

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	PromptInput([PromptInput]):::first
	ChatPromptTemplate(ChatPromptTemplate)
	ChatGroq(ChatGroq)
	StrOutputParser(StrOutputParser)
	StrOutputParserOutput([StrOutputParserOutput]):::last
	PromptInput --> ChatPromptTemplate;
	ChatPromptTemplate --> ChatGroq;
	StrOutputParser --> StrOutputParserOutput;
	ChatGroq --> StrOutputParser;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```

## Ejemplo 3: LangGraph con reintento (ejemplo_3_langgraph.py)

```mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
	__start__([<p>__start__</p>]):::first
	generar(generar)
	presentar(presentar)
	__end__([<p>__end__</p>]):::last
	__start__ --> generar;
	generar -.-> presentar;
	presentar --> __end__;
	generar -.-> generar;
	classDef default fill:#f2f0ff,line-height:1.2
	classDef first fill-opacity:0
	classDef last fill:#bfb6fc
```
