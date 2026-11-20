# LangChain y LangGraph

## Diferencia principal

Si el flujo es una línea recta, alcanza con LangChain. Si hace falta reintentar, tomar decisiones o mantener un estado, se usa LangGraph.

## LangChain

Framework de Python y TypeScript para integrar IA en aplicaciones. Conecta LLMs con herramientas y datos, y permite armar procesos.

- **Chains:** son la base. Un pipeline recibe un input, el modelo lo procesa (a veces con ayuda de una herramienta), el output se limpia o normaliza y pasa al paso siguiente.
- **Piezas modulares:** los modelos, los prompts y los output parsers son intercambiables. Cambiar de modelo requiere modificar pocas líneas de código.
- **Prompt templates:** inyectan variables dentro del prompt.
- **Tools:** les dan habilidades a los agentes, como buscar, escribir, crear un PDF o llamar a una API.
- **RAG (Retrieval-Augmented Generation):** la información de nuestros archivos se guarda en una base de datos vectorial y LangChain recupera lo relevante para dárselo al modelo. Esto reduce las alucinaciones, porque el modelo responde con datos de nuestras fuentes.

## LangGraph

Framework para armar flujos con estado, modelados como un grafo. Se usa junto con LangChain: los modelos, prompts y parsers de LangChain corren dentro de sus nodos.

- **Estado:** un diccionario compartido. Cada nodo lo lee y devuelve los campos que cambia.
- **Nodos:** funciones que representan un paso del proceso.
- **Aristas:** conectan los nodos. Pueden ser fijas (`add_edge`) o condicionales (`add_conditional_edges`), donde una función mira el estado y devuelve el próximo nodo.
- **Ciclos:** permiten volver a un nodo anterior, que es lo que necesitan los reintentos.
- **Otras capacidades:** guardar el estado para retomar una ejecución, pausar el flujo para que una persona apruebe y coordinar varios agentes. No las probamos en la demo.

## Ejemplo con LangChain: resumir un texto en formato fijo

Se recibe la descripción de una empresa y se devuelve un resumen de dos oraciones en español, o un objeto con `nombre`, `rubro` y `resumen`.

Alcanza con LangChain porque son pasos en línea recta: `prompt | llm | parser`. No hay decisiones ni reintentos, así que un grafo sumaría complejidad sin beneficio.

Demo: `langChain2.py` (prompt con rol de sistema, modelo y parser).

## Ejemplo con LangGraph: agente que investiga una empresa

El agente busca información sobre una empresa, revisa si encontró lo necesario (sede, rubro, tamaño) y, si falta algo, vuelve a buscar con otra consulta.

Hace falta LangGraph porque hay un ciclo con una condición de salida: un nodo busca, otro evalúa el estado y decide si repetir la búsqueda o terminar.

Demo: `langGraph1.py` usa el mismo patrón con otro criterio. El nodo `generar` produce una respuesta, `decidir` revisa si salió cortada y, si es así, el flujo vuelve a `generar` con más tokens. Los diagramas están en `diagramas.md`.
