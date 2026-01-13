"""
Ejemplos de uso del PlotSchemaGenerator.
Demuestra cómo combinar diferentes Axis of Interest para crear plot schemas.
"""

from axis_of_interest.schema_generator import PlotSchemaGenerator, create_plot_schema
from axis_of_interest.utils import render_plot_schema_md


def ejemplo_1_sequential():
    """Ejemplo 1: Combinar JOURNEY, TASK y CONFLICT secuencialmente"""
    print("="*80)
    print("EJEMPLO 1: Estrategia Sequential")
    print("="*80)
    
    schema = create_plot_schema(
        schema_name="Hero's Epic Adventure",
        aoi_names=["JOURNEY", "TASK", "CONFLICT"],
        strategy="sequential",
        description="Un héroe viaja, recibe una tarea difícil y lucha contra un enemigo"
    )
    
    print(render_plot_schema_md(schema))
    print("\n\n")


def ejemplo_2_round_robin():
    """Ejemplo 2: Intercalar JOURNEY y CONFLICT en round-robin"""
    print("="*80)
    print("EJEMPLO 2: Estrategia Round Robin")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    
    schema = generator.generate_schema(
        schema_name="Journey with Constant Conflict",
        aoi_names=["JOURNEY", "CONFLICT"],
        interleaving_strategy="round_robin",
        schema_description="Viaje con conflictos intercalados"
    )
    
    print(render_plot_schema_md(schema))
    print("\n\n")


def ejemplo_3_parallel():
    """Ejemplo 3: Combinar múltiples AOIs en paralelo"""
    print("="*80)
    print("EJEMPLO 3: Estrategia Parallel")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    
    schema = generator.generate_schema(
        schema_name="Complex Multi-Thread Story",
        aoi_names=["JOURNEY", "RIVALRY", "SHIFTING_LOVE"],
        interleaving_strategy="parallel",
        schema_description="Historia con múltiples hilos paralelos"
    )
    
    print(render_plot_schema_md(schema))
    print("\n\n")


def ejemplo_4_custom():
    """Ejemplo 4: Crear schema personalizado seleccionando spans específicos"""
    print("="*80)
    print("EJEMPLO 4: Schema Personalizado")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    
    # Obtener AOIs
    journey = generator.get_aoi_by_name("JOURNEY")
    conflict = generator.get_aoi_by_name("CONFLICT")
    task = generator.get_aoi_by_name("TASK")
    
    # Seleccionar spans específicos manualmente
    custom_spans = [
        journey.plot_spans[0],      # Out (Departure)
        task.plot_spans[0],         # TaskSet
        conflict.plot_spans[0],     # Struggle
        conflict.plot_spans[1],     # Victory
        task.plot_spans[1],         # TaskSolved
        journey.plot_spans[1],      # Back (Return)
    ]
    
    schema = generator.generate_custom_schema(
        schema_name="Custom Hero's Journey",
        plot_spans=custom_spans,
        schema_description="Viaje con tarea y conflicto intercalados de forma personalizada"
    )
    
    print(render_plot_schema_md(schema))
    print("\n\n")


def ejemplo_5_listar_aois():
    """Ejemplo 5: Explorar AOIs disponibles"""
    print("="*80)
    print("EJEMPLO 5: Explorar AOIs Disponibles")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    
    print("AOIs disponibles:")
    print("-" * 40)
    for aoi_name in generator.list_available_aois():
        info = generator.get_aoi_info(aoi_name)
        print(f"\n📖 {info['name']}")
        print(f"   Descripción: {info['description']}")
        print(f"   Protagonista: {info['protagonist_role']}")
        print(f"   Roles: {', '.join(info['roles'])}")
        print(f"   Plot Spans ({info['num_plot_spans']}): {', '.join(info['plot_span_names'])}")
    
    print("\n\n")


def ejemplo_6_todos_los_aois():
    """Ejemplo 6: Crear un schema con TODOS los AOIs disponibles"""
    print("="*80)
    print("EJEMPLO 6: Schema con TODOS los AOIs")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    all_aoi_names = generator.list_available_aois()
    
    schema = generator.generate_schema(
        schema_name="The Ultimate Epic Story",
        aoi_names=all_aoi_names,
        interleaving_strategy="round_robin",
        schema_description="Una historia épica que combina todos los axis of interest disponibles"
    )
    
    print(f"Schema con {len(schema.plots_span)} plot spans combinados")
    print(f"De {len(all_aoi_names)} AOIs diferentes\n")
    print(render_plot_schema_md(schema))
    print("\n\n")


if __name__ == "__main__":
    print("\n🎭 EJEMPLOS DE PLOT SCHEMA GENERATOR 🎭\n")
    
    # Ejecutar todos los ejemplos
    ejemplo_1_sequential()
    ejemplo_2_round_robin()
    ejemplo_3_parallel()
    ejemplo_4_custom()
    ejemplo_5_listar_aois()
    
    # Descomentar para ver el schema gigante con todos los AOIs
    # ejemplo_6_todos_los_aois()
    
    print("="*80)
    print("✅ Ejemplos completados!")
    print("="*80)
