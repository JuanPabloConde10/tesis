"""
DEMO SIMPLE: Explicación visual del PlotSchemaGenerator
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from axis_of_interest.schema_generator import PlotSchemaGenerator
from axis_of_interest.utils import render_plot_schema_md


def mostrar_estructura_aoi():
    """Muestra cómo están estructurados los AOIs"""
    print("\n" + "="*80)
    print("📚 ¿QUÉ ES UN AXIS OF INTEREST (AOI)?")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    
    # Veamos algunos AOIs
    print("\n🔹 JOURNEY tiene estas etapas (plot spans):")
    journey = generator.get_aoi_by_name("JOURNEY")
    for i, span in enumerate(journey.plot_spans, 1):
        print(f"   {i}. {span.name}")
    
    print("\n🔹 CONFLICT tiene estas etapas:")
    conflict = generator.get_aoi_by_name("CONFLICT")
    for i, span in enumerate(conflict.plot_spans, 1):
        print(f"   {i}. {span.name}")
    
    print("\n🔹 TASK tiene estas etapas:")
    task = generator.get_aoi_by_name("TASK")
    for i, span in enumerate(task.plot_spans, 1):
        print(f"   {i}. {span.name}")


def demo_estrategia_sequential():
    """Muestra qué hace la estrategia SEQUENTIAL"""
    print("\n" + "="*80)
    print("📝 ESTRATEGIA SEQUENTIAL (Secuencial)")
    print("="*80)
    print("\n💡 Qué hace: Pone TODAS las etapas del primer AOI, luego TODAS del segundo, etc.")
    print("\nEjemplo con JOURNEY + CONFLICT:")
    print()
    print("   JOURNEY tiene:")
    print("      1. Out")
    print("      2. Back")
    print()
    print("   CONFLICT tiene:")
    print("      1. Struggle") 
    print("      2. Victory")
    print()
    print("   📊 Resultado SEQUENTIAL:")
    print("      1. Out        ← del JOURNEY")
    print("      2. Back       ← del JOURNEY")
    print("      3. Struggle   ← del CONFLICT")
    print("      4. Victory    ← del CONFLICT")
    
    # Generar el schema real
    generator = PlotSchemaGenerator()
    schema = generator.generate_schema(
        schema_name="Test Sequential",
        aoi_names=["JOURNEY", "CONFLICT"],
        interleaving_strategy="sequential"
    )
    
    print("\n   ✅ Schema generado con", len(schema.plots_span), "etapas:")
    for i, span in enumerate(schema.plots_span, 1):
        print(f"      {i}. {span.name} (de {span.axis_of_interest})")


def demo_estrategia_round_robin():
    """Muestra qué hace la estrategia ROUND ROBIN"""
    print("\n" + "="*80)
    print("🔄 ESTRATEGIA ROUND ROBIN (Intercalado Circular)")
    print("="*80)
    print("\n💡 Qué hace: Va tomando UNA etapa de cada AOI, rotando entre ellos")
    print("\nEjemplo con JOURNEY + CONFLICT:")
    print()
    print("   JOURNEY tiene:")
    print("      1. Out")
    print("      2. Back")
    print()
    print("   CONFLICT tiene:")
    print("      1. Struggle")
    print("      2. Victory")
    print()
    print("   📊 Resultado ROUND ROBIN:")
    print("      1. Out        ← del JOURNEY (primer turno)")
    print("      2. Struggle   ← del CONFLICT (primer turno)")
    print("      3. Back       ← del JOURNEY (segundo turno)")
    print("      4. Victory    ← del CONFLICT (segundo turno)")
    
    generator = PlotSchemaGenerator()
    schema = generator.generate_schema(
        schema_name="Test Round Robin",
        aoi_names=["JOURNEY", "CONFLICT"],
        interleaving_strategy="round_robin"
    )
    
    print("\n   ✅ Schema generado con", len(schema.plots_span), "etapas:")
    for i, span in enumerate(schema.plots_span, 1):
        print(f"      {i}. {span.name} (de {span.axis_of_interest})")


def demo_estrategia_parallel():
    """Muestra qué hace la estrategia PARALLEL"""
    print("\n" + "="*80)
    print("⚡ ESTRATEGIA PARALLEL (Paralelo)")
    print("="*80)
    print("\n💡 Qué hace: Agrupa por POSICIÓN. Primero todas las etapas #1, luego todas las #2, etc.")
    print("\nEjemplo con JOURNEY + CONFLICT + TASK:")
    print()
    print("   JOURNEY tiene:")
    print("      1. Out")
    print("      2. Back")
    print()
    print("   CONFLICT tiene:")
    print("      1. Struggle")
    print("      2. Victory")
    print()
    print("   TASK tiene:")
    print("      1. TaskSet")
    print("      2. TaskSolved")
    print()
    print("   📊 Resultado PARALLEL:")
    print("      1. Out        ← JOURNEY #1")
    print("      2. Struggle   ← CONFLICT #1")
    print("      3. TaskSet    ← TASK #1")
    print("      4. Back       ← JOURNEY #2")
    print("      5. Victory    ← CONFLICT #2")
    print("      6. TaskSolved ← TASK #2")
    
    generator = PlotSchemaGenerator()
    schema = generator.generate_schema(
        schema_name="Test Parallel",
        aoi_names=["JOURNEY", "CONFLICT", "TASK"],
        interleaving_strategy="parallel"
    )
    
    print("\n   ✅ Schema generado con", len(schema.plots_span), "etapas:")
    for i, span in enumerate(schema.plots_span, 1):
        print(f"      {i}. {span.name} (de {span.axis_of_interest})")


def demo_estrategia_random():
    """Muestra qué hace la estrategia RANDOM"""
    print("\n" + "="*80)
    print("🎲 ESTRATEGIA RANDOM (Aleatorio)")
    print("="*80)
    print("\n💡 Qué hace: Elige ALEATORIAMENTE el siguiente AOI, pero RESPETA el orden dentro de cada AOI")
    print("\nEjemplo con JOURNEY + CONFLICT + TASK:")
    print()
    print("   JOURNEY tiene:")
    print("      1. Out")
    print("      2. Back")
    print()
    print("   CONFLICT tiene:")
    print("      1. Struggle")
    print("      2. Victory")
    print()
    print("   TASK tiene:")
    print("      1. TaskSet")
    print("      2. TaskSolved")
    print()
    print("   📊 Resultado RANDOM (varía en cada ejecución):")
    print("      Posible: Out, TaskSet, Struggle, Back, Victory, TaskSolved")
    print("      O tal vez: Struggle, Out, TaskSet, Victory, Back, TaskSolved")
    print("      ⚠️  SIEMPRE Out antes de Back, Struggle antes de Victory, etc.")
    
    generator = PlotSchemaGenerator()
    
    print("\n   🎲 Generando 3 schemas aleatorios para mostrar la variación:")
    for run in range(1, 4):
        schema = generator.generate_schema(
            schema_name=f"Test Random {run}",
            aoi_names=["JOURNEY", "CONFLICT", "TASK"],
            interleaving_strategy="random"
        )
        
        print(f"\n   Ejecución {run}:")
        order = " → ".join(f"{span.name}" for span in schema.plots_span)
        print(f"      {order}")


def demo_schema_completo():
    """Muestra toda la información detallada de un schema generado"""
    print("\n" + "="*80)
    print("📄 SCHEMA COMPLETO - Toda la Información Detallada")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    
    print("\n💡 Creando un schema con estrategia RANDOM...")
    schema = generator.generate_schema(
        schema_name="Epic Adventure Story",
        aoi_names=["JOURNEY", "CONFLICT", "TASK"],
        interleaving_strategy="random",
        schema_description="Una aventura épica que combina viaje, conflicto y tareas"
    )
    
    print("\n" + "─"*80)
    print(render_plot_schema_md(schema))
    print("─"*80)


def demo_uso_basico():
    """Muestra cómo usar el generador de forma simple"""
    print("\n" + "="*80)
    print("🎯 CÓMO USAR EL GENERADOR - EJEMPLO PRÁCTICO")
    print("="*80)
    
    print("\n📋 Código:")
    print("""
    from axis_of_interest.schema_generator import create_plot_schema
    
    # Crear un schema combinando 3 AOIs
    schema = create_plot_schema(
        schema_name="Mi Historia Épica",
        aoi_names=["JOURNEY", "TASK", "CONFLICT"],
        strategy="parallel"
    )
    
    # Ahora tienes un schema con todas las etapas intercaladas!
    print(f"Schema tiene {len(schema.plots_span)} etapas")
    """)
    
    print("\n▶️ Resultado:")
    from axis_of_interest.schema_generator import create_plot_schema
    
    schema = create_plot_schema(
        schema_name="Mi Historia Épica",
        aoi_names=["JOURNEY", "TASK", "CONFLICT"],
        strategy="parallel"
    )
    
    print(f"\n   ✅ Schema '{schema.name}' creado!")
    print(f"   📝 Tiene {len(schema.plots_span)} etapas en total:")
    for i, span in enumerate(schema.plots_span, 1):
        print(f"      {i}. {span.name} (de {span.axis_of_interest})")


def demo_todos_los_aois():
    """Muestra todos los AOIs disponibles"""
    print("\n" + "="*80)
    print("📚 LISTA COMPLETA DE AOIs DISPONIBLES")
    print("="*80)
    
    generator = PlotSchemaGenerator()
    
    print(f"\n   Total: {len(generator.list_available_aois())} AOIs\n")
    
    for aoi_name in sorted(generator.list_available_aois()):
        info = generator.get_aoi_info(aoi_name)
        spans_str = ", ".join(info['plot_span_names'])
        print(f"   • {aoi_name:20} → Etapas: {spans_str}")


if __name__ == "__main__":
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "🎭 DEMO SIMPLE - PLOT SCHEMA GENERATOR" + " "*20 + "║")
    print("╚" + "="*78 + "╝")
    
    mostrar_estructura_aoi()
    demo_estrategia_sequential()
    demo_estrategia_round_robin()
    demo_estrategia_parallel()
    demo_estrategia_random()
    demo_schema_completo()
    demo_uso_basico()
    demo_todos_los_aois()
    
    print("\n" + "="*80)
    print("✅ RESUMEN")
    print("="*80)
    print("""
El PlotSchemaGenerator te permite:

1️⃣  Elegir varios AOIs (ej: JOURNEY, CONFLICT, TASK)
2️⃣  Combinar sus etapas (plot spans) de 4 formas diferentes:
    • SEQUENTIAL: uno después del otro
    • ROUND_ROBIN: intercalados circularmente
    • PARALLEL: agrupados por posición
    • RANDOM: orden aleatorio respetando secuencia interna
3️⃣  Obtener un PlotSchema completo listo para usar

¡Es como construir una historia con bloques LEGO! 🧱
Cada AOI es un set de bloques, y tú decides cómo combinarlos.
    """)
    print("="*80 + "\n")
