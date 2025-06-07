import os
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from tools import (
    crear_tablero, buscar_tablero,
    crear_columna, buscar_columna,
    crear_tarea, tareas_por_tablero,
    crear_checklist, crear_comentario, comentarios_por_tarea,
    crear_colaborador, buscar_colaborador_por_email,obtener_datos_kanban_df
)
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory


load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4" )

# Lista de herramientas disponibles
tools = [
    crear_tablero, buscar_tablero,
    crear_columna, buscar_columna,
    crear_tarea, tareas_por_tablero,
    crear_checklist, crear_comentario, comentarios_por_tarea,
    crear_colaborador, buscar_colaborador_por_email, obtener_datos_kanban_df
]

# Inicializar la memoria
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)


# Inicializar el agente con razonamiento reactivo (ReAct)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True
)

system_prompt = SystemMessage(content="""
Eres un asistente de gestión de proyectos que puede crear, modificar, consultar y analizar toda la información relacionada con tableros, columnas, tareas, comentarios, checklists y colaboradores.
Usa las herramientas que se te proporcionan para cumplir con las solicitudes.
Si no estás seguro de algo, pregunta.

Puedes acceder a todos los datos del sistema Kanban (tableros, columnas, tareas, comentarios, colaboradores).

Cuando el usuario pida un análisis, primero obtén los datos con 'obtener_datos_kanban_df'. 

El resultado te dará una vista resumida en texto plano. 
Usa esa información como contexto para responder con precisión.

Ejemplos de análisis:
- ¿Qué columna tiene más tareas?
- ¿Qué colaborador ha comentado más?
- ¿Cuántas tareas están atrasadas?
""")



# 🧪 Interacción natural
if __name__ == "__main__":
    print("\n💬 Escribe una petición (ej: crea tablero, agrega tarea, etc):\n")
    first = True
    while True:
        prompt = input("> ")
        if prompt.lower() in ["salir", "exit", "quit"]:
            break
        if first:
            memory.chat_memory.messages.insert(0, system_prompt)
            first = False
        respuesta = agent.invoke({"input": prompt})
        print("\n🤖", respuesta["output"])


