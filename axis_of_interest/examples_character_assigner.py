"""
Ejemplos de uso del CharacterNameAssigner.
Demuestra cómo asignar nombres reales a personajes en Plot Schemas.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from axis_of_interest.schema_generator import create_plot_schema
from axis_of_interest.character_assigner import CharacterNameAssigner, assign_character_names
from axis_of_interest.utils import render_plot_schema_md


def ejemplo_1_basico():
    """Ejemplo básico: Asignar nombres a un schema"""
    print("="*80)
    print("EJEMPLO 1: Asignación Básica de Nombres")
    print("="*80)
    
    # Crear un schema con 3 AOIs
    schema = create_plot_schema(
        schema_name="Epic Adventure",
        aoi_names=["JOURNEY", "CONFLICT", "TASK"],
        strategy="random"
    )
    
    print("\n📝 ANTES (con placeholders):")
    print("─"*80)
    print(render_plot_schema_md(schema))
    
    # Asignar nombres
    nombres = ["Alice", "Bob", "Charlie", "Diana"]
    schema_con_nombres = assign_character_names(schema, nombres)
    
    print("\n✨ DESPUÉS (con nombres asignados):")
    print("─"*80)
    print(render_plot_schema_md(schema_con_nombres))
    print("\n")


def ejemplo_2_sin_reuso():
    """Ejemplo: Cada nombre se usa solo una vez en todo el schema"""
    print("="*80)
    print("EJEMPLO 2: Sin Reusar Nombres (cada nombre solo una vez)")
    print("="*80)
    
    schema = create_plot_schema(
        schema_name="Unique Characters Story",
        aoi_names=["JOURNEY", "RIVALRY"],
        strategy="parallel"
    )
    
    nombres = ["Emma", "Frank", "Grace", "Henry", "Iris"]
    assigner = CharacterNameAssigner()
    
    try:
        schema_con_nombres = assigner.assign_names(schema, nombres, allow_reuse=False)
        print("\n✨ Schema con nombres únicos:")
        print("─"*80)
        print(render_plot_schema_md(schema_con_nombres))
    except ValueError as e:
        print(f"\n❌ Error: {e}")
    
    print("\n")


def ejemplo_3_mapeo_personalizado():
    """Ejemplo: Mapeo personalizado para ciertos personajes"""
    print("="*80)
    print("EJEMPLO 3: Mapeo Personalizado")
    print("="*80)
    
    schema = create_plot_schema(
        schema_name="Custom Mapping Story",
        aoi_names=["JOURNEY", "CONFLICT"],
        strategy="sequential"
    )
    
    nombres = ["Alex", "Blake", "Casey", "Drew"]
    
    # Forzar que ciertos placeholders tengan nombres específicos
    mapeo_custom = {
        "JOURNEY": {"Hero": "Alex"},  # El Hero en JOURNEY siempre es Alex
        "CONFLICT": {"X": "Blake"}     # X en CONFLICT siempre es Blake
    }
    
    assigner = CharacterNameAssigner()
    schema_con_nombres = assigner.assign_names_with_mapping(schema, nombres, mapeo_custom)
    
    print("\n✨ Schema con mapeo personalizado:")
    print("   - JOURNEY: Hero forzado a 'Alex'")
    print("   - CONFLICT: X forzado a 'Blake'")
    print("─"*80)
    print(render_plot_schema_md(schema_con_nombres))
    print("\n")


def ejemplo_4_resumen_personajes():
    """Ejemplo: Obtener resumen de personajes asignados"""
    print("="*80)
    print("EJEMPLO 4: Resumen de Personajes")
    print("="*80)
    
    schema = create_plot_schema(
        schema_name="Character Analysis",
        aoi_names=["JOURNEY", "CONFLICT", "RIVALRY"],
        strategy="random"
    )
    
    nombres = ["Luna", "Max", "Nina", "Oscar"]
    schema_con_nombres = assign_character_names(schema, nombres)
    
    # Obtener resumen
    assigner = CharacterNameAssigner()
    resumen = assigner.get_character_summary(schema_con_nombres)
    
    print("\n📊 Resumen de personajes por AOI:")
    print("─"*80)
    for aoi_name, roles in resumen.items():
        print(f"\n{aoi_name}:")
        for role, characters in roles.items():
            print(f"  • {role}: {', '.join(characters)}")
    print("\n")


def ejemplo_5_reproducibilidad():
    """Ejemplo: Usar seed para resultados reproducibles"""
    print("="*80)
    print("EJEMPLO 5: Reproducibilidad con Seed")
    print("="*80)
    
    schema = create_plot_schema(
        schema_name="Reproducible Story",
        aoi_names=["JOURNEY", "TASK"],
        strategy="parallel"
    )
    
    nombres = ["Zoe", "Yuri", "Xander"]
    
    print("\n🎲 Ejecución 1 (seed=42):")
    schema1 = assign_character_names(schema, nombres, seed=42)
    assigner = CharacterNameAssigner()
    resumen1 = assigner.get_character_summary(schema1)
    for aoi, roles in resumen1.items():
        print(f"  {aoi}: {roles}")
    
    print("\n🎲 Ejecución 2 (seed=42 - mismo resultado):")
    schema2 = assign_character_names(schema, nombres, seed=42)
    resumen2 = assigner.get_character_summary(schema2)
    for aoi, roles in resumen2.items():
        print(f"  {aoi}: {roles}")
    
    print("\n🎲 Ejecución 3 (seed=99 - diferente resultado):")
    schema3 = assign_character_names(schema, nombres, seed=99)
    resumen3 = assigner.get_character_summary(schema3)
    for aoi, roles in resumen3.items():
        print(f"  {aoi}: {roles}")
    
    print("\n✅ Los dos primeros son idénticos (mismo seed), el tercero es diferente")
    print("\n")


def ejemplo_6_nombres_insuficientes():
    """Ejemplo: Qué pasa cuando hay menos nombres que personajes"""
    print("="*80)
    print("EJEMPLO 6: Reciclaje de Nombres (menos nombres que personajes)")
    print("="*80)
    
    schema = create_plot_schema(
        schema_name="Few Names Story",
        aoi_names=["RIVALRY"],  # RIVALRY tiene muchos roles
        strategy="sequential"
    )
    
    # Solo 2 nombres para varios personajes
    nombres = ["Tom", "Jerry"]
    schema_con_nombres = assign_character_names(schema, nombres, allow_reuse=True)
    
    print("\n✨ Schema (nombres reciclados cuando no hay suficientes):")
    print("─"*80)
    print(render_plot_schema_md(schema_con_nombres))
    print("\n")


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*18 + "🎭 EJEMPLOS DE CHARACTER NAME ASSIGNER" + " "*18 + "║")
    print("╚" + "="*78 + "╝")
    print("\n")
    
    ejemplo_1_basico()
    ejemplo_2_sin_reuso()
    ejemplo_3_mapeo_personalizado()
    ejemplo_4_resumen_personajes()
    ejemplo_5_reproducibilidad()
    ejemplo_6_nombres_insuficientes()
    
    print("="*80)
    print("✅ RESUMEN")
    print("="*80)
    print("""
El CharacterNameAssigner te permite:

1️⃣  Asignar nombres reales de una lista a los placeholders
2️⃣  Mantener consistencia dentro de cada AOI
3️⃣  Permitir variación entre diferentes AOIs
4️⃣  Controlar si los nombres se pueden reusar o no
5️⃣  Usar mapeos personalizados para ciertos personajes
6️⃣  Reproducibilidad con seeds
7️⃣  Manejar automáticamente casos con pocos nombres

¡Ahora tus historias tienen personajes con nombres reales! 🎉
    """)
    print("="*80 + "\n")
