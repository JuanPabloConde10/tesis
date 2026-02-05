"""
Constantes de configuración para la API de generación de cuentos.

Define las estrategias de combinación de AOIs y métodos de generación de texto.
"""

STRATEGIES = [
    {
        "id": "sequential",
        "name": "Secuencial",
        "description": "Concatena todos los spans de cada AOI en orden",
    },
    {
        "id": "round_robin",
        "name": "Round Robin",
        "description": "Alterna entre AOIs circularmente",
    },
    {
        "id": "parallel",
        "name": "Paralelo",
        "description": "Agrupa spans por posición",
    },
    {
        "id": "random",
        "name": "Aleatorio",
        "description": "Selección aleatoria respetando orden interno",
    },
]

GENERATION_METHODS = [
    {
        "id": "gramatica",
        "name": "Gramática",
        "description": "Genera texto simple con gramática y luego el LLM lo transforma en cuento completo",
    },
    {
        "id": "aoi_directo",
        "name": "AOI Directo",
        "description": "Envía el Plot Schema completo (JSON) directamente al LLM para generar el cuento",
    },
]
