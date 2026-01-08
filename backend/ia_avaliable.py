import google.generativeai as genai
from dotenv import load_dotenv
import os

# Carrega a chave de API do arquivo .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Substitua pela sua chave de API
genai.configure(api_key=api_key)

def listar_modelos():
    models = genai.list_models()
    for model in models:
        print(f"Name: {model.name} | Description: {model.description}")

if __name__ == "__main__":
    listar_modelos()