from mcp import StdioServerParameters
from dotenv import load_dotenv
import os

# Cargar variables de entorno del archivo .env
load_dotenv()

# Cargar la clave de API en la variable usada por el SDK
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Configuración del servidor MCP a usar
SERVER_PARAMS = StdioServerParameters(
    command = "/home/valiwis/.pyenv/versions/3.12.0/envs/llms/bin/uvx",
    args = ["mcp-server-time", "--local-timezone=America/Bogota"]
)