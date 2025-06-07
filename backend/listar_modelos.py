from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

models = client.models.list()

print("\n📦 Modelos disponibles con tu clave:")
for model in models.data:
    print("•", model.id)
