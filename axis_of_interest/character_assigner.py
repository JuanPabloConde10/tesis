"""
Sistema de asignación de nombres a personajes en Plot Schemas.

Permite asignar nombres reales a los placeholders de personajes,
manteniendo consistencia dentro de cada AOI pero permitiendo variación entre AOIs.
"""

import random
from typing import List, Dict, Optional
from copy import deepcopy
from axis_of_interest.schemas import PlotSchema, PlotSpan, PlotAtom, list_of_aoi


class CharacterNameAssigner:
    """
    Asigna nombres reales a los personajes placeholders en un PlotSchema.
    
    Características:
    - Consistencia intra-AOI: Dentro de un mismo AOI, el mismo placeholder siempre recibe el mismo nombre
    - Variación inter-AOI: Entre diferentes AOIs, los placeholders pueden tener nombres diferentes
    - Asignación aleatoria: Los nombres se asignan aleatoriamente de una lista proporcionada
    
    Ejemplo:
        assigner = CharacterNameAssigner()
        
        schema = generate_schema(["JOURNEY", "CONFLICT"])
        names = ["Alice", "Bob", "Charlie"]
        
        schema_con_nombres = assigner.assign_names(schema, names)
        
        # Resultado posible:
        # JOURNEY: traveller="Alice" en todos los spans
        # CONFLICT: attacker="Bob", defender="Charlie" en todos los spans
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Inicializa el asignador de nombres.
        
        Args:
            seed: Semilla para el generador aleatorio (para reproducibilidad)
        """
        self.random = random.Random(seed)
    
    def assign_names(
        self,
        schema: PlotSchema,
        character_names: List[str],
        allow_reuse: bool = True
    ) -> PlotSchema:
        """
        Asigna nombres a los personajes del schema.
        
        Args:
            schema: PlotSchema con placeholders
            character_names: Lista de nombres disponibles para asignar
            allow_reuse: Si True, permite que el mismo nombre aparezca en diferentes AOIs.
                        Si False, cada nombre solo se usa una vez en todo el schema.
        
        Returns:
            Nuevo PlotSchema con nombres asignados
        
        Raises:
            ValueError: Si no hay suficientes nombres para los personajes
        """
        if not character_names:
            raise ValueError("Debe proporcionar al menos un nombre de personaje")
        
        # Crear copia profunda del schema para no modificar el original
        new_schema = deepcopy(schema)
        
        # Rastrear nombres usados globalmente (solo si allow_reuse=False)
        global_used_names = set()
        
        # Crear un diccionario de AOIs por nombre para acceso rápido
        aoi_dict = {aoi.name: aoi for aoi in list_of_aoi}
        
        # Agrupar spans por AOI
        spans_by_aoi = {}
        for span in new_schema.plots_span:
            aoi_name = span.axis_of_interest
            if aoi_name not in spans_by_aoi:
                spans_by_aoi[aoi_name] = []
            spans_by_aoi[aoi_name].append(span)
        
        # Procesar cada AOI (todos sus spans juntos)
        for aoi_name, spans in spans_by_aoi.items():
            # Obtener el objeto AOI para acceder a sus roles
            aoi = aoi_dict.get(aoi_name)
            if not aoi:
                raise ValueError(f"No se encontró el AOI: {aoi_name}")
            
            # Usar los roles del AOI directamente
            roles = aoi.roles
            available_names = [n for n in character_names if n not in global_used_names] if not allow_reuse else character_names.copy()
            
            # Verificar que hay suficientes nombres
            if len(available_names) < len(roles):
                if allow_reuse:
                    # Si permitimos reuso, simplemente ciclar los nombres
                    pass
                else:
                    raise ValueError(
                        f"No hay suficientes nombres únicos. "
                        f"Se necesitan {len(roles)} nombres únicos "
                        f"pero solo hay {len(available_names)} disponibles para el AOI {aoi_name}"
                    )
            
            # Asignar nombres aleatoriamente a cada rol
            shuffled_names = available_names.copy()
            self.random.shuffle(shuffled_names)
            
            role_to_name = {}
            for idx, role in enumerate(roles):
                # Si hay más roles que nombres, reciclar
                name_idx = idx % len(shuffled_names)
                assigned_name = shuffled_names[name_idx]
                role_to_name[role] = assigned_name
                
                if not allow_reuse:
                    global_used_names.add(assigned_name)
            
            # Aplicar el mapeo a todos los atoms de TODOS los spans de este AOI
            for span in spans:
                for atom in span.plots_atoms:
                    new_characters = {}
                    for role in atom.characters.keys():
                        # Asignar el nombre directamente al rol
                        new_characters[role] = role_to_name.get(role, role)
                    atom.characters = new_characters
        
        return new_schema
    
    def assign_names_with_mapping(
        self,
        schema: PlotSchema,
        character_names: List[str],
        custom_mapping: Optional[Dict[str, Dict[str, str]]] = None
    ) -> PlotSchema:
        """
        Asigna nombres con un mapeo personalizado por AOI.
        
        Args:
            schema: PlotSchema con placeholders
            character_names: Lista de nombres disponibles
            custom_mapping: Mapeo específico por AOI. 
                           Formato: {"AOI_NAME": {"placeholder": "nombre"}}
                           
        Ejemplo:
            custom_mapping = {
                "JOURNEY": {"Hero": "Alice"},
                "CONFLICT": {"X": "Bob", "Y": "Charlie"}
            }
        
        Returns:
            Nuevo PlotSchema con nombres asignados
        """
        new_schema = deepcopy(schema)
        custom_mapping = custom_mapping or {}
        
        for span in new_schema.plots_span:
            aoi_name = span.axis_of_interest
            aoi_mapping = custom_mapping.get(aoi_name, {})
            
            # Recolectar placeholders
            placeholders_in_aoi = set()
            for atom in span.plots_atoms:
                placeholders_in_aoi.update(atom.characters.values())
            
            # Crear mapeo completo
            placeholder_to_name = {}
            available_names = [n for n in character_names]
            self.random.shuffle(available_names)
            
            for placeholder in sorted(placeholders_in_aoi):
                if placeholder in aoi_mapping:
                    # Usar mapeo personalizado
                    placeholder_to_name[placeholder] = aoi_mapping[placeholder]
                else:
                    # Asignar aleatoriamente de los nombres disponibles
                    if available_names:
                        placeholder_to_name[placeholder] = available_names.pop(0)
                    else:
                        # Reciclar si no hay más nombres
                        placeholder_to_name[placeholder] = self.random.choice(character_names)
            
            # Aplicar mapeo
            for atom in span.plots_atoms:
                new_characters = {}
                for role, placeholder in atom.characters.items():
                    new_characters[role] = placeholder_to_name[placeholder]
                atom.characters = new_characters
        
        return new_schema
    
    def get_character_summary(self, schema: PlotSchema) -> Dict[str, Dict[str, set]]:
        """
        Obtiene un resumen de qué personajes aparecen en cada AOI.
        
        Args:
            schema: PlotSchema a analizar
        
        Returns:
            Diccionario con formato:
            {
                "AOI_NAME": {
                    "role1": {"Alice", "Bob"},  # nombres que aparecen en ese rol
                    "role2": {"Charlie"}
                }
            }
        """
        summary = {}
        
        for span in schema.plots_span:
            aoi_name = span.axis_of_interest
            if aoi_name not in summary:
                summary[aoi_name] = {}
            
            for atom in span.plots_atoms:
                for role, character_name in atom.characters.items():
                    if role not in summary[aoi_name]:
                        summary[aoi_name][role] = set()
                    summary[aoi_name][role].add(character_name)
        
        # Convertir sets a listas para mejor visualización
        return {
            aoi: {role: sorted(list(names)) for role, names in roles.items()}
            for aoi, roles in summary.items()
        }


def assign_character_names(
    schema: PlotSchema,
    names: List[str],
    allow_reuse: bool = True,
    seed: Optional[int] = None
) -> PlotSchema:
    """
    Función de conveniencia para asignar nombres rápidamente.
    
    Args:
        schema: PlotSchema con placeholders
        names: Lista de nombres de personajes
        allow_reuse: Permitir que el mismo nombre aparezca en diferentes AOIs
        seed: Semilla para reproducibilidad
    
    Returns:
        PlotSchema con nombres asignados
    
    Ejemplo:
        schema = create_plot_schema("My Story", ["JOURNEY", "CONFLICT"])
        schema_con_nombres = assign_character_names(
            schema, 
            ["Alice", "Bob", "Charlie"],
            allow_reuse=True
        )
    """
    assigner = CharacterNameAssigner(seed=seed)
    return assigner.assign_names(schema, names, allow_reuse=allow_reuse)
