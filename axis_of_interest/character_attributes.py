"""
Sistema de atributos de personalidad para personajes.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class CharacterAttributes(BaseModel):
    """Atributos de personalidad de un personaje."""
    
    valentia: int = Field(ge=1, le=5, description="Valentía (1-5)")
    bondad: int = Field(ge=1, le=5, description="Bondad (1-5)")
    astucia: int = Field(ge=1, le=5, description="Astucia (1-5)")
    maldad: int = Field(ge=1, le=5, description="Maldad (1-5)")
    carisma: int = Field(ge=1, le=5, description="Carisma (1-5)")


class Character(BaseModel):
    """Personaje con nombre y atributos."""
    
    name: str
    attributes: CharacterAttributes
    description: Optional[str] = None
    
    def __str__(self):
        description = f", Descripción:{self.description}" if self.description else ""
        return (
            f"{self.name} (Valentía:{self.attributes.valentia}, "
            f"Bondad:{self.attributes.bondad}, Astucia:{self.attributes.astucia}, "
            f"Maldad:{self.attributes.maldad}, Carisma:{self.attributes.carisma}{description})"
        )


# Perfiles predefinidos basados en roles típicos
ROLE_ATTRIBUTE_PROFILES: Dict[str, CharacterAttributes] = {
    # Roles heroicos
    "hero": CharacterAttributes(valentia=5, bondad=4, astucia=3, maldad=1, carisma=5),
    "protagonist": CharacterAttributes(valentia=4, bondad=4, astucia=3, maldad=1, carisma=4),
    "tested": CharacterAttributes(valentia=4, bondad=4, astucia=3, maldad=1, carisma=4),
    "traveller": CharacterAttributes(valentia=4, bondad=3, astucia=3, maldad=1, carisma=4),
    "rescuer": CharacterAttributes(valentia=5, bondad=5, astucia=3, maldad=1, carisma=5),
    
    # Roles antagónicos
    "villain": CharacterAttributes(valentia=4, bondad=1, astucia=4, maldad=5, carisma=4),
    "attacker": CharacterAttributes(valentia=4, bondad=1, astucia=3, maldad=4, carisma=4),
    "defender": CharacterAttributes(valentia=4, bondad=3, astucia=3, maldad=2, carisma=4),
    "kidnapper": CharacterAttributes(valentia=3, bondad=1, astucia=4, maldad=5, carisma=4),
    "abductor": CharacterAttributes(valentia=3, bondad=1, astucia=4, maldad=5, carisma=4),
    
    # Roles de víctima
    "victim": CharacterAttributes(valentia=2, bondad=4, astucia=2, maldad=1, carisma=2),
    "abducted": CharacterAttributes(valentia=2, bondad=4, astucia=2, maldad=1, carisma=2),
    
    # Roles de mentor/donante
    "donor": CharacterAttributes(valentia=3, bondad=5, astucia=4, maldad=1, carisma=5),
    "tester": CharacterAttributes(valentia=3, bondad=4, astucia=5, maldad=1, carisma=5),
    "helper": CharacterAttributes(valentia=3, bondad=5, astucia=3, maldad=1, carisma=4),
    
    # Roles neutrales/otros
    "caller": CharacterAttributes(valentia=3, bondad=3, astucia=3, maldad=2, carisma=3),
    "sender": CharacterAttributes(valentia=3, bondad=3, astucia=3, maldad=2, carisma=3),
    "interdicter": CharacterAttributes(valentia=3, bondad=4, astucia=3, maldad=1, carisma=4),
    
    # Roles de guardián
    "guardian": CharacterAttributes(valentia=4, bondad=3, astucia=3, maldad=2, carisma=4),
    "unrelenting_guardian": CharacterAttributes(valentia=4, bondad=2, astucia=4, maldad=3, carisma=5),
    "relenting_guardian": CharacterAttributes(valentia=3, bondad=4, astucia=3, maldad=1, carisma=4),
}


def calculate_attribute_distance(char_attrs: CharacterAttributes, role_attrs: CharacterAttributes) -> float:
    """
    Calcula la distancia euclidiana entre los atributos de un personaje y un rol.
    Menor distancia = mejor match.
    """
    distance = (
        (char_attrs.valentia - role_attrs.valentia) ** 2 +
        (char_attrs.bondad - role_attrs.bondad) ** 2 +
        (char_attrs.astucia - role_attrs.astucia) ** 2 +
        (char_attrs.maldad - role_attrs.maldad) ** 2 +
        (char_attrs.carisma - role_attrs.carisma) ** 2
    ) ** 0.5
    return distance


def get_best_character_for_role(
    role: str,
    available_characters: List[Character],
    used_characters: set = None
) -> Character:
    """
    Encuentra el mejor personaje para un rol basándose en la distancia de atributos.
    
    Args:
        role: Nombre del rol (ej: "hero", "villain")
        available_characters: Lista de personajes disponibles
        used_characters: Set de nombres ya usados (para evitar duplicados)
    
    Returns:
        El personaje que mejor encaja con el rol
    """
    if used_characters is None:
        used_characters = set()
    
    # Obtener perfil ideal para el rol (lowercase para matching)
    role_profile = ROLE_ATTRIBUTE_PROFILES.get(
        role.lower(),
        CharacterAttributes(valentia=3, bondad=3, astucia=3, maldad=3, carisma=3)  # neutral por defecto
    )
    
    # Filtrar personajes no usados
    candidates = [c for c in available_characters if c.name not in used_characters]
    
    if not candidates:
        # Si no hay candidatos, permitir reuso
        candidates = available_characters
    
    # Encontrar el mejor match
    best_char = min(
        candidates,
        key=lambda c: calculate_attribute_distance(c.attributes, role_profile)
    )
    
    return best_char
