import pandas as pd
from langchain.tools import tool
import requests

API_URL = "http://localhost:8000"

# BOARDS
@tool
def crear_tablero(name: str, description: str = "") -> str:
    """Crea un tablero nuevo con un nombre y descripción opcional"""
    res = requests.post(f"{API_URL}/boards/", json={"name": name, "description": description})
    return res.json() if res.status_code == 200 else f"Error: {res.text}"

@tool
def buscar_tablero(nombre: str) -> str:
    """Busca un tablero por nombre"""
    res = requests.get(f"{API_URL}/boards/by_name/?name={nombre}")
    return res.json() if res.status_code == 200 and res.json() else "No encontrado"

# COLUMNS
@tool
def crear_columna(name: str, board_id: int, description: str = "") -> str:
    """Crea una columna dentro de un tablero existente"""
    res = requests.post(f"{API_URL}/columns/", json={"name": name, "description": description, "board_id": board_id})
    return res.json() if res.status_code == 200 else f"Error: {res.text}"

@tool
def buscar_columna(nombre: str, board_id: int) -> str:
    """Busca una columna dentro de un tablero por nombre"""
    res = requests.get(f"{API_URL}/columns/by_name/?name={nombre}&board_id={board_id}")
    return res.json() if res.status_code == 200 and res.json() else "No encontrada"

# TASKS
@tool
def crear_tarea(title: str, status: str, column_id: int, description: str = "", start_date: str = "", end_date: str = "") -> str:
    """Crea una tarea dentro de una columna existente"""
    payload = {"title": title, "status": status, "column_id": column_id, "description": description, "start_date": start_date, "end_date": end_date}
    res = requests.post(f"{API_URL}/tasks/", json=payload)
    return res.json() if res.status_code == 200 else f"Error: {res.text}"

@tool
def tareas_por_tablero(board_id: int) -> str:
    """Devuelve las tareas asociadas a un tablero"""
    res = requests.get(f"{API_URL}/tasks/by_board/{board_id}")
    return res.json() if res.status_code == 200 else f"Error: {res.text}"
@tool
def crear_checklist(name: str, task_id: int, done: bool = False) -> str:
    """Crea un nuevo ítem de checklist para una tarea"""
    payload = {"name": name, "task_id": task_id, "done": done}
    res = requests.post(f"{API_URL}/checklists/", json=payload)
    return res.json() if res.status_code == 200 else f"Error: {res.text}"
@tool
def crear_comentario(content: str, collaborator_id: int, task_id: int) -> str:
    """Agrega un comentario a una tarea"""
    payload = {"content": content, "collaborator_id": collaborator_id, "task_id": task_id}
    res = requests.post(f"{API_URL}/comments/", json=payload)
    return res.json() if res.status_code == 200 else f"Error: {res.text}"

@tool
def comentarios_por_tarea(task_id: int) -> str:
    """Devuelve todos los comentarios de una tarea"""
    res = requests.get(f"{API_URL}/comments/by_task/{task_id}")
    return res.json() if res.status_code == 200 else f"Error: {res.text}"
@tool
def crear_colaborador(name: str, email: str) -> str:
    """Crea un colaborador nuevo"""
    payload = {"name": name, "email": email}
    res = requests.post(f"{API_URL}/collaborators/", json=payload)
    return res.json() if res.status_code == 200 else f"Error: {res.text}"

@tool
def buscar_colaborador_por_email(email: str) -> str:
    """Busca un colaborador por correo electrónico"""
    res = requests.get(f"{API_URL}/collaborators/by_email/?email=" + email)
    return res.json() if res.status_code == 200 and res.json() else "No encontrado"
@tool
def obtener_datos_kanban_df() -> str:
    """Carga todos los datos del sistema y los resume en texto plano para análisis por el modelo"""
    try:
        boards = pd.DataFrame(requests.get(f"{API_URL}/export/boards/").json())
        columns = pd.DataFrame(requests.get(f"{API_URL}/export/columns/").json())
        tasks = pd.DataFrame(requests.get(f"{API_URL}/export/tasks/").json())
        comments = pd.DataFrame(requests.get(f"{API_URL}/export/comments/").json())
        collaborators = pd.DataFrame(requests.get(f"{API_URL}/export/collaborators/").json())

        resumen = f"""📊 Estado actual del sistema Kanban:
- Tableros: {len(boards)}
- Columnas: {len(columns)}
- Tareas: {len(tasks)}
- Comentarios: {len(comments)}
- Colaboradores: {len(collaborators)}

"""

        # TABLEROS
        resumen += "\n📋 Tableros:\n"
        if not boards.empty:
            for _, row in boards.iterrows():
                resumen += f"- {row['name']} (ID: {row['id']}): {row['description'] or 'Sin descripción'}\n"
        else:
            resumen += "No hay tableros registrados.\n"

        # COLUMNAS
        resumen += "\n🧱 Columnas:\n"
        if not columns.empty:
            for _, row in columns.iterrows():
                resumen += f"- {row['name']} (ID: {row['id']}) en Tablero ID {row['board_id']}: {row['description'] or 'Sin descripción'}\n"
        else:
            resumen += "No hay columnas registradas.\n"

        # TAREAS
        resumen += "\n📌 Tareas:\n"
        if not tasks.empty:
            for _, row in tasks.iterrows():
                resumen += f"- {row['title']} (ID: {row['id']}), estado: {row['status']}, columna ID: {row['column_id']}\n"
        else:
            resumen += "No hay tareas registradas.\n"

        # COLABORADORES
        resumen += "\n👥 Colaboradores:\n"
        if not collaborators.empty:
            for _, row in collaborators.iterrows():
                resumen += f"- {row['name']} ({row['email']})\n"
        else:
            resumen += "No hay colaboradores registrados.\n"

        # COMENTARIOS
        resumen += "\n💬 Comentarios:\n"
        if not comments.empty:
            for _, row in comments.iterrows():
                resumen += f"- Comentario de colaborador ID {row['collaborator_id']} en tarea ID {row['task_id']}: {row['content'][:40]}...\n"
        else:
            resumen += "No hay comentarios registrados.\n"

        return resumen.strip()

    except Exception as e:
        return f"❌ Error al obtener los datos: {str(e)}"
