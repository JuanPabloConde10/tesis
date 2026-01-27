from pydantic import BaseModel, Field
from typing import Optional, Dict, List

class CharacterAttributesSchema(BaseModel):
    """Atributos de personalidad de un personaje (1-5)."""
    valentia: int = Field(ge=1, le=5)
    bondad: int = Field(ge=1, le=5)
    astucia: int = Field(ge=1, le=5)
    maldad: int = Field(ge=1, le=5)
    carisma: int = Field(ge=1, le=5)

class CharacterWithAttributesSchema(BaseModel):
    """Personaje con nombre y atributos."""
    name: str
    attributes: CharacterAttributesSchema
    description: Optional[str] = None


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
    aois: Optional[list[str]] = Field(default=None, description="Lista de Axis of Interest (para Modo 3 y 4)")
    interleaving_strategy: Optional[str] = Field(default=None, description="Estrategia de interleaving: sequential, round_robin, parallel, random, llm (para Modo 3 y 4)")
    character_attributes: Optional[list[CharacterWithAttributesSchema]] = Field(default=None, description="Lista de personajes con atributos (para Modo 4)")
    aoi_names: Optional[List[str]] = None
    strategy: Optional[str] = None
    generation_method: Optional[str] = Field(default=None, description="Método de generación para Modo 2: 'gramatica' o 'aoi_directo'")
