from pydantic import BaseModel, Field
from typing import Optional, List

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
    aoi_names: Optional[List[str]] = None
    strategy: Optional[str] = None
