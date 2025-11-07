from mcp.client.stdio import stdio_client
from config import SERVER_PARAMS
from mcp import ClientSession
from model import ask_gemini 
import asyncio

# Prompt de prueba
PROMPT = "¿Qué hora es en Bogotá, Colombia?"

async def main():
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("\n" + "="*80)
            print("                             SIN HERRAMIENTAS")
            print("="*80 + "\n")

            # Llamamos a Gemini sin herramientas
            direct_response = await ask_gemini(PROMPT, None)
            print(direct_response)

            print("\n" + "="*80)
            print("                             CON HERRAMIENTAS")
            print("="*80 + "\n")

            # Usamos la función personalizada que pasa la sesión como herramienta
            response_with_tools = await ask_gemini(PROMPT, session)
            print(response_with_tools)

if __name__ == "__main__":
    asyncio.run(main())