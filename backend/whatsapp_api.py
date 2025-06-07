from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from main_langchain_agent import agent
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse
import textwrap

app = FastAPI()


def limpiar(texto):
    texto = texto.replace("**", "").replace("*", "")
    for emoji in ["📊", "📋", "🧱", "📌", "👥", "💬", "✅", "❌"]:
        texto = texto.replace(emoji, "")
    return texto.strip()


def dividir_mensaje(texto: str, max_len=300):
    return textwrap.wrap(texto.strip(), width=max_len, break_long_words=False)[:5]


@app.post("/whatsapp-webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    print(f"📨 Mensaje de {From}: {Body}")
    twiml = MessagingResponse()

    try:
        respuesta = agent.invoke({"input": Body})
        texto = respuesta.get("output", "❌ Sin respuesta generada.")
        limpio = limpiar(texto)
        partes = dividir_mensaje(limpio)

        for parte in partes:
            twiml.message(parte)

    except Exception as e:
        print("❌ Error:", e)
        twiml.message("❌ Hubo un error procesando tu mensaje.")

    return Response(content=str(twiml), media_type="application/xml")


@app.get("/")
def root():
    return {"status": "ok", "message": "API del agente IA funcionando"}
