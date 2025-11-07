from mcp.server.fastmcp import FastMCP
import wikipediaapi

# Inicializa el servidor MCP
mcp = FastMCP("wikipedia")

# Crear instancia del API con idioma en español. Por políticas de uso de wikipedia 
# se debe definir un nombre para el agente que utiliza el API
wiki = wikipediaapi.Wikipedia(
    language='es',
    user_agent='mcp-research-agent/1.0'
)

# Para definir una herramientas se utiliza el decorador @mcp.tool()
@mcp.tool()
def get_summary(term: str) -> str:

    """
    Obtiene el resumen introductorio de un artículo de Wikipedia.

    Esta herramienta consulta Wikipedia utilizando el término proporcionado y devuelve
    el resumen introductorio del artículo, si está disponible.

    Args:
        term (str): Término o título del artículo a buscar en Wikipedia.

    Returns:
        str: Texto con el resumen del artículo.
             Si el artículo no existe o no tiene resumen, se devuelve un mensaje explicativo.
    """

    page = wiki.page(term)
    if not page.exists():
        return f"No se encontró ninguna página para el término '{term}'."
    
    summary = page.summary
    return summary if summary else f"No hay resumen disponible para '{term}'."

# Para definir una herramientas se utiliza el decorador @mcp.tool()
@mcp.tool()
def get_page_sections(term: str) -> str:

    """
    Lista las secciones principales de un artículo de Wikipedia.

    Esta herramienta busca una página de Wikipedia a partir del término dado y devuelve
    los títulos de las secciones principales del artículo si existe.

    Args:
        term (str): Término o título del artículo a consultar en Wikipedia.

    Returns:
        str: Lista con los títulos de las secciones encontradas en el artículo.
             Si el artículo no existe o no tiene secciones, devuelve un mensaje apropiado.
    """

    page = wiki.page(term)
    if not page.exists():
        return f"No se encontró ningún artículo para '{term}'."
    sections = [s.title for s in page.sections]
    if not sections:
        return "Este artículo no tiene secciones identificables."
    return "Secciones:\n- " + "\n- ".join(sections)

# Para definir una herramientas se utiliza el decorador @mcp.tool()
@mcp.tool()
def get_section_content(term: str, section_title: str) -> str:

    """
    Extrae el contenido de una sección específica de un artículo de Wikipedia.

    Esta herramienta busca un artículo de Wikipedia por su título y luego intenta localizar
    una sección específica (por nombre) dentro del artículo. La búsqueda de secciones
    se realiza de forma recursiva para manejar jerarquías anidadas.

    Args:
        term (str): Título del artículo de Wikipedia.
        section_title (str): Título de la sección cuyo contenido se desea extraer.

    Returns:
        str: Texto del contenido de la sección solicitada.
             Si el artículo o la sección no existen, devuelve un mensaje explicativo.
    """

    page = wiki.page(term)
    if not page.exists():
        return f"No se encontró ningún artículo para '{term}'."

    def find_section(sections):
        for s in sections:
            if s.title.lower() == section_title.lower():
                return s.text
            result = find_section(s.sections)
            if result:
                return result
        return None

    content = find_section(page.sections)
    if not content:
        return f"No se encontró la sección '{section_title}' en el artículo."
    
    return content

# Ejecución del servidor MCP
if __name__ == "__main__":
    mcp.run(transport="stdio")