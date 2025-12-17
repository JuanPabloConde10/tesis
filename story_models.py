from typing import Optional

from pydantic import BaseModel, Field

# Etiquetas legibles para los arcos narrativos disponibles en el frontend.
ARC_LABELS = {
    "viaje_del_heroe": "Viaje del héroe",
    "maduracion": "Historia de maduración",
    "busqueda": "Búsqueda",
    "venganza": "Venganza",
    "comedia_de_enredos": "Comedia de enredos",
    "tragedia": "Tragedia",
}


class StoryRequest(BaseModel):
    trama: str = Field(..., min_length=5)
    genero: Optional[str] = None
    arco: Optional[str] = None
    personajes: list[str] = Field(default_factory=list)
    temperature: Optional[float] = Field(default=None, ge=0, le=2)
    max_tokens: Optional[int] = Field(default=None, gt=0)
    model: Optional[str] = Field(default=None, description="Modelo LLM a usar")
    mode: Optional[str] = Field(default=None, description="Modo de creación backend")
    experiment_id: Optional[str] = Field(default=None, description="Identificador de experimento opcional")
