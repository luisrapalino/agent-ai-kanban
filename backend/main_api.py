from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main_langchain_agent import agent  # importa tu agente ya configurado

app = FastAPI()

# Habilitar CORS para frontend local
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia al puerto de tu frontend si es diferente
    allow_methods=["*"],
    allow_headers=["*"],

)

# Modelo del mensaje recibido
class ChatInput(BaseModel):
    mensaje: str

@app.post("/chat")
async def chat_endpoint(data: ChatInput):
    try:
        respuesta = agent.invoke({"input": data.mensaje})
        return {"respuesta": respuesta["output"]}
    except Exception as e:
        return {"respuesta": f"❌ Error interno: {str(e)}"}
