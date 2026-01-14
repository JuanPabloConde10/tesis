from infrastructure.api.global_schemas import StoryRequest

def create_prompt_mode0(data: StoryRequest) -> tuple[str, str]:
    system_prompt = "Eres un escritor que crea cuentos breves en español, con tono claro y atractivo."
    user_parts = [f"Trama: {data.trama}"]
    if data.genero:
        user_parts.append(f"Género: {data.genero}")
    if data.arco:
        user_parts.append(f"Arco narrativo: {data.arco}")
    if data.personajes:
        user_parts.append("Personajes: " + ", ".join(data.personajes))
    if data.experiment_id:
        user_parts.append(f"Identificador de experimento: {data.experiment_id}")
    user_prompt = "\n".join(user_parts)
    return system_prompt, user_prompt