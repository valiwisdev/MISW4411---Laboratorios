from google import genai

# Creamos un cliente para interactuar con los modelos generativos de Gemini
client = genai.Client()

# Función principal que envía un prompt al modelo Gemini y devuelve la respuesta en texto plano
async def ask_gemini(prompt, session):
    # Construimos el parámetro 'tools' solo si se pasa una sesión
    tools = [session] if session else None

    # Hacemos una sola llamada, con o sin herramientas
    response = await client.aio.models.generate_content(
        model = "gemini-2.5-flash",
        contents = prompt, 
        config = genai.types.GenerateContentConfig(
            temperature = 1.0,
            tools = tools,  # Será None si no hay sesión, lo cual es válido
        ),
    )

    # Accedemos al historial automático de llamadas a herramientas para ver si el modelo usó alguna
    history = response.automatic_function_calling_history

    used_tool = None     
    tool_args = None     

    # Si hay historial, lo recorremos para encontrar la primera llamada a herramienta
    if history:
        for message in history:
            if not hasattr(message, "parts"):
                continue  
            for part in message.parts:
                # Verificamos si esta parte contiene una llamada a función (tool invocation)
                if hasattr(part, "function_call") and part.function_call is not None:
                    used_tool = part.function_call.name
                    tool_args = part.function_call.args
                    break
            # Salimos del bucle externo si ya encontramos una herramienta  
            if used_tool:
                break  

    # Mensajes informativos sobre el uso o no de herramientas
    if used_tool:
        print(f"\nGemini decidió usar la herramienta: {used_tool}")
        print(f"Parámetros: {tool_args}\n")
    else:
        print("\nGemini respondió directamente sin usar herramientas.\n")

    # Extraemos solo las partes que contienen texto para evitar el warning del SDK
    parts = response.candidates[0].content.parts
    text_response = "".join(
        part.text for part in parts if hasattr(part, "text") and part.text
    )

    # Retornamos el texto limpio de la respuesta del modelo
    return text_response