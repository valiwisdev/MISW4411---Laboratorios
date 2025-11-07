import asyncio
from mcp.client.stdio import stdio_client
from config import SERVER_PARAMS
from mcp import ClientSession
from model import ask_gemini  # Tu función ya adaptada para session=None o session activa

# Historial del chat como lista de tuplas (rol, mensaje)
messages: list[tuple[str, str]] = []

async def run_chat():
    print("🤖 Asistente Gemini con MCP listo para conversar.")
    print("Escribe 'salir' para terminar.\n")

    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            while True:
                # Manejo de la entrada del usuario y la finalización del chat
                user_input = input("👤 Tú: ").strip()
                if user_input.lower() in {"salir", "exit", "quit"}:
                    print("👋 Hasta luego.")
                    break

                # Agregamos el mensaje del usuario al historial
                messages.append(("user", user_input))

                # Construimos el prompt como historial (puedes usar solo los últimos N si prefieres)
                prompt = ""
                for role, content in messages:
                    prefix = "Usuario" if role == "user" else "Asistente"
                    prompt += f"{prefix}: {content}\n"

                print("🔄 Procesando...", end="", flush=True)

                # Obtenemos respuesta del modelo usando la sesión (usa herramientas si es necesario)
                response = await ask_gemini(prompt, session)
                print(f"\r🤖 Asistente: {response}\n")

                # Agregamos la respuesta al historial
                messages.append(("assistant", response))

if __name__ == "__main__":
    asyncio.run(run_chat())