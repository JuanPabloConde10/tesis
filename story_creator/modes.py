from global_schemas import StoryRequest

def get_modes() -> list:
    return [
        {"id": "0", "name": "Modo 0", "description": "Generación a pelo."},
        {"id": "1", "name": "Modo 1", "description": "Utilizando el Plot Schema en el prompt"},
        {"id": "2", "name": "Modo 2", "description": "Creamos el Plot Schema y chunks para cada escena. Luego le pedimos al LLM que hile estas escenas en un unico cuento"}
     ]

def generate_the_story(data : StoryRequest) -> str:
    return "puto el que lo lee"