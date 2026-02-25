"""
Generador interactivo de cuentos a partir de Axis of Interest.

Permite seleccionar AOIs, asignar nombres de personajes, y generar el cuento usando un LLM.
"""

import json
import sys
from pathlib import Path
from typing import List, Optional

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from axis_of_interest.registry import list_of_aoi
from axis_of_interest.schema_generator import PlotSchemaGenerator
from axis_of_interest.character_assigner import assign_character_names, assign_character_names_by_attributes
from axis_of_interest.character_attributes import Character, CharacterAttributes
from axis_of_interest.utils import render_plot_schema_md, build_client_by_provider
from axis_of_interest.prompts import (
    template_prompt_generate_cuento,
    template_prompt_generate_cuento_gramatica,
)
from axis_of_interest.text_gen import generate_text
from config import Settings



class StoryGenerator:
    """Generador interactivo de cuentos."""

    def __init__(self):
        self.settings = Settings()
        self.available_aois = {aoi.name: aoi for aoi in list_of_aoi}

    def select_aois(self) -> List[str]:
        """Permite al usuario seleccionar AOIs interactivamente."""
        print("\n" + "=" * 80)
        print("📚 AXIS OF INTEREST DISPONIBLES:")
        print("=" * 80)

        for idx, aoi_name in enumerate(sorted(self.available_aois.keys()), 1):
            aoi = self.available_aois[aoi_name]
            print(f"{idx:2d}. {aoi_name}")
            print(f"    {aoi.description}")
            print()

        print("Ingresá los números de los AOIs que querés usar (separados por coma)")
        print("Ejemplo: 1,3,5")

        while True:
            try:
                selection = input("\n> ").strip()
                indices = [int(x.strip()) for x in selection.split(",")]

                aoi_names = sorted(self.available_aois.keys())
                selected = [
                    aoi_names[i - 1] for i in indices if 1 <= i <= len(aoi_names)
                ]

                if not selected:
                    print("❌ No seleccionaste ningún AOI válido. Intentá de nuevo.")
                    continue

                print(f"\n✅ Seleccionaste: {', '.join(selected)}")
                return selected

            except (ValueError, IndexError):
                print("❌ Entrada inválida. Usá números separados por coma.")

    def select_strategy(self) -> str:
        """Permite seleccionar la estrategia de interleaving."""
        print("\n" + "=" * 80)
        print("🎲 ESTRATEGIA DE INTERLEAVING:")
        print("=" * 80)
        print("1. Sequential  - Concatena todos los spans en orden")
        print("2. Round Robin - Alterna entre AOIs circularmente")
        print("3. Parallel    - Agrupa spans por posición")
        print("4. Random      - Selección aleatoria respetando orden interno")
        print("5. LLM         - El LLM decide el orden completo")

        strategies = ["sequential", "round_robin", "parallel", "random", "llm"]

        while True:
            try:
                choice = input("\nSeleccioná estrategia (1-5): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(strategies):
                    strategy = strategies[idx]
                    print(f"✅ Estrategia: {strategy}")
                    return strategy
                else:
                    print("❌ Número inválido. Elegí entre 1 y 5.")
            except ValueError:
                print("❌ Entrada inválida. Ingresá un número entre 1 y 5.")

    def get_character_names(self) -> List[str]:
        """Permite ingresar nombres de personajes."""
        print("\n" + "=" * 80)
        print("👥 NOMBRES DE PERSONAJES:")
        print("=" * 80)
        print("Ingresá los nombres de los personajes separados por coma")
        print("Ejemplo: Alice, Bob, Charlie, Diana")

        while True:
            names_input = input("\n> ").strip()
            if not names_input:
                print("❌ Debés ingresar al menos un nombre.")
                continue

            names = [n.strip() for n in names_input.split(",") if n.strip()]
            if names:
                print(f"✅ Nombres: {', '.join(names)}")
                return names
            else:
                print("❌ No ingresaste nombres válidos.")
    
    def select_assignment_mode(self) -> int:
        """Permite seleccionar el modo de asignación de personajes."""
        print("\n" + "=" * 80)
        print("🎯 MODO DE ASIGNACIÓN DE PERSONAJES:")
        print("=" * 80)
        print("1. Aleatorio   - Los nombres se asignan aleatoriamente a los roles")
        print("2. Por atributos - Los personajes se asignan según sus características")
        
        while True:
            try:
                choice = input("\nSeleccioná modo (1-2): ").strip()
                mode = int(choice)
                if mode in [1, 2]:
                    mode_name = "Aleatorio" if mode == 1 else "Por atributos"
                    print(f"✅ Modo: {mode_name}")
                    return mode
                else:
                    print("❌ Número inválido. Elegí 1 o 2.")
            except ValueError:
                print("❌ Entrada inválida. Ingresá 1 o 2.")
    
    def get_character_attributes(self, name: str) -> CharacterAttributes:
        """Solicita los atributos de un personaje."""
        print(f"\n📊 Atributos de {name} (escala 1-5):")
        
        while True:
            try:
                valentia = int(input("  Valentía (1-5): ").strip())
                bondad = int(input("  Bondad (1-5): ").strip())
                astucia = int(input("  Astucia (1-5): ").strip())
                maldad = int(input("  Maldad (1-5): ").strip())
                carisma = int(input("  Carisma (1-5): ").strip())
                
                if all(1 <= x <= 5 for x in [valentia, bondad, astucia, maldad, carisma]):
                    return CharacterAttributes(
                        valentia=valentia,
                        bondad=bondad,
                        astucia=astucia,
                        maldad=maldad,
                        carisma=carisma
                    )
                else:
                    print("❌ Todos los valores deben estar entre 1 y 5.")
            except ValueError:
                print("❌ Por favor ingresá números válidos.")
    
    def get_characters_with_attributes(self) -> List[Character]:
        """Obtiene nombres y atributos de personajes."""
        print("\n" + "=" * 80)
        print("👥 PERSONAJES CON ATRIBUTOS:")
        print("=" * 80)
        print("Ingresá los nombres de los personajes separados por coma")
        print("Luego definirás sus atributos de personalidad")
        print("Ejemplo: Alice, Bob, Charlie")
        
        while True:
            names_input = input("\n> ").strip()
            if not names_input:
                print("❌ Debés ingresar al menos un nombre.")
                continue
            
            names = [n.strip() for n in names_input.split(",") if n.strip()]
            if names:
                break
            else:
                print("❌ No ingresaste nombres válidos.")
        
        characters = []
        for name in names:
            attrs = self.get_character_attributes(name)
            characters.append(Character(name=name, attributes=attrs))
            print(f"✅ {name} configurado")
        
        return characters

    def select_llm_provider(self) -> str:
        """Permite seleccionar el proveedor de LLM."""
        print("\n" + "=" * 80)
        print("🤖 PROVEEDOR DE LLM:")
        print("=" * 80)
        print("1. OpenAI")
        print("2. Anthropic")
        print("3. Google")
        print("4. HuggingFace")

        providers = ["openai", "anthropic", "google", "huggingface"]

        while True:
            try:
                choice = input(
                    f"\nSeleccioná proveedor (1-4) [default: {self.settings.default_provider}]: "
                ).strip()

                if not choice:
                    return self.settings.default_provider

                idx = int(choice) - 1
                if 0 <= idx < len(providers):
                    provider = providers[idx]
                    print(f"✅ Proveedor: {provider}")
                    return provider
                else:
                    print("❌ Número inválido. Elegí entre 1 y 4.")
            except ValueError:
                print("❌ Entrada inválida. Ingresá un número entre 1 y 4.")

    def generate_story(
        self,
        aoi_names: List[str],
        character_names: Optional[List[str]] = None,
        characters: Optional[List[Character]] = None,
        strategy: str = "random",
        provider: Optional[str] = None,
        seed: Optional[int] = None,
    ) -> tuple[str, str, str]:
        """
        Genera un cuento completo.
        
        Args:
            aoi_names: Nombres de los AOIs a usar
            character_names: Nombres para asignación aleatoria (Modo 1)
            characters: Personajes con atributos para asignación inteligente (Modo 2)
            strategy: Estrategia de interleaving
            provider: Proveedor de LLM
            seed: Semilla para reproducibilidad

        Returns:
            Tupla (plot_schema_markdown, cuento_gramatica, cuento_aoi)
        """
        # 1. Generar el Plot Schema
        print("\n" + "=" * 80)
        print("⚙️  GENERANDO PLOT SCHEMA...")
        print("=" * 80)

        generator = PlotSchemaGenerator()
        schema = generator.generate_schema(
            schema_name=f"Story with {', '.join(aoi_names)}",
            aoi_names=aoi_names,
            interleaving_strategy=strategy,
            llm_provider=provider,
            schema_description=f"Plot schema usando {strategy} strategy",
        )

        # 2. Asignar nombres a personajes según el modo
        print("\n✅ Schema generado. Asignando personajes...")
        
        if characters:
            # Modo 2: Asignación por atributos
            print("🎯 Usando asignación por atributos...")
            schema_with_names = assign_character_names_by_attributes(
                schema,
                characters,
                allow_reuse=True,
                seed=seed
            )
        else:
            # Modo 1: Asignación aleatoria
            print("🎲 Usando asignación aleatoria...")
            schema_with_names = assign_character_names(
                schema,
                character_names,
                allow_reuse=True,
                seed=seed
            )

        # 3. Renderizar el schema
        schema_md = render_plot_schema_md(schema_with_names.model_dump())

        print("\n📋 PLOT SCHEMA:")
        print("─" * 80)
        print(schema_md)

        # Debug: verificar duplicados
        print("\n[DEBUG] Cantidad de spans:", len(schema_with_names.plots_span))
        span_names = [
            f"{s.axis_of_interest}/{s.name}" for s in schema_with_names.plots_span
        ]
        print("[DEBUG] Spans:", span_names)

        # 3.5 Generar texto simple con gramática
        print("\n📝 TEXTO GENERADO (gramática simple):")
        print("─" * 80)
        simple_text = generate_text(schema_with_names)
        print(simple_text)
        print()

        # 4. Generar el cuento con LLM usando gramática
        print("\n" + "=" * 80)
        print("📝 GENERANDO CUENTO #1: CON GRAMÁTICA...")
        print("=" * 80)

        story_gramatica = None
        try:
            llm_client = build_client_by_provider(provider, self.settings)

            # Reemplazar el placeholder manualmente para evitar conflictos con {} del JSON
            prompt = template_prompt_generate_cuento_gramatica.replace(
                "{texto_gramatica}", simple_text
            )

            print(f"🤖 Usando: {provider or self.settings.default_provider}")

            # Generar el cuento con gramática
            story_gramatica = llm_client.generate(prompt)

            print("\n✅ Cuento con gramática generado!")

        except Exception as e:
            import traceback

            print(f"\n❌ Error al generar el cuento con gramática: {e}")
            print("\n[DEBUG] Traceback completo:")
            traceback.print_exc()

        # 5. Generar el cuento con LLM usando AOI directo (schema JSON)
        print("\n" + "=" * 80)
        print("📝 GENERANDO CUENTO #2: CON AOI DIRECTO...")
        print("=" * 80)

        story_aoi = None
        try:
            llm_client = build_client_by_provider(provider, self.settings)

            # Crear el prompt con el schema
            schema_dict = schema_with_names.model_dump()
            schema_json = json.dumps(schema_dict, indent=2, ensure_ascii=False)

            # Reemplazar el placeholder manualmente para evitar conflictos con {} del JSON
            prompt = template_prompt_generate_cuento.replace(
                "{plot_schema}", schema_json
            )
            prompt = prompt.replace("{ambiente}", "No especificado")
            prompt = prompt.replace("{genero_section}", "")
            if characters:
                lines = []
                for char in characters:
                    desc = f"Descripción: {char.description}. " if char.description else ""
                    attrs = (
                        f"Valentía {char.attributes.valentia}, "
                        f"Bondad {char.attributes.bondad}, "
                        f"Astucia {char.attributes.astucia}, "
                        f"Maldad {char.attributes.maldad}, "
                        f"Carisma {char.attributes.carisma}"
                    )
                    lines.append(f"- {char.name}. {desc}Atributos: {attrs}.")
                characters_section = "\n".join(lines)
            elif character_names:
                characters_section = "\n".join(f"- {name}" for name in character_names)
            else:
                characters_section = "No especificado"
            prompt = prompt.replace("{characters_section}", characters_section)

            print(f"🤖 Usando: {provider or self.settings.default_provider}")

            # Generar el cuento con AOI
            story_aoi = llm_client.generate(prompt)

            print("\n✅ Cuento con AOI directo generado!")

        except Exception as e:
            import traceback

            print(f"\n❌ Error al generar el cuento con AOI: {e}")
            print("\n[DEBUG] Traceback completo:")
            traceback.print_exc()

        return schema_md, story_gramatica, story_aoi

    def run_interactive(self):
        """Ejecuta el generador en modo interactivo."""
        print("\n")
        print("╔" + "=" * 78 + "╗")
        print("║" + " " * 20 + "🎭 GENERADOR DE CUENTOS 🎭" + " " * 32 + "║")
        print("╚" + "=" * 78 + "╝")

        # Selección de AOIs
        aoi_names = self.select_aois()

        # Selección de estrategia
        strategy = self.select_strategy()

        # Selección de modo de asignación
        assignment_mode = self.select_assignment_mode()
        
        # Obtener personajes según el modo
        if assignment_mode == 1:
            # Modo aleatorio
            character_names = self.get_character_names()
            characters = None
        else:
            # Modo por atributos
            characters = self.get_characters_with_attributes()
            character_names = None

        # Proveedor de LLM
        provider = self.select_llm_provider()

        # Generar
        schema_md, story_gramatica, story_aoi = self.generate_story(
            aoi_names=aoi_names,
            character_names=character_names,
            characters=characters,
            strategy=strategy,
            provider=provider,
            seed=42,  # Para reproducibilidad
        )

        # Mostrar resultados
        if story_gramatica:
            print("\n" + "=" * 80)
            print("📖 CUENTO #1 - GENERADO CON GRAMÁTICA:")
            print("=" * 80)
            print(story_gramatica)

        if story_aoi:
            print("\n" + "=" * 80)
            print("📖 CUENTO #2 - GENERADO CON AOI DIRECTO:")
            print("=" * 80)
            print(story_aoi)

        if story_gramatica or story_aoi:
            # Guardar en archivo
            save = input("\n¿Guardar los cuentos en archivos? (s/n): ").strip().lower()
            if save == "s":
                filename = (
                    input("Nombre base del archivo (sin extensión): ").strip()
                    or "cuento"
                )

                with open(f"{filename}_schema.md", "w", encoding="utf-8") as f:
                    f.write(schema_md)

                if story_gramatica:
                    with open(f"{filename}_gramatica.txt", "w", encoding="utf-8") as f:
                        f.write(story_gramatica)

                if story_aoi:
                    with open(f"{filename}_aoi.txt", "w", encoding="utf-8") as f:
                        f.write(story_aoi)

                saved_files = [f"{filename}_schema.md"]
                if story_gramatica:
                    saved_files.append(f"{filename}_gramatica.txt")
                if story_aoi:
                    saved_files.append(f"{filename}_aoi.txt")

                print(f"\n✅ Guardado en: {', '.join(saved_files)}")

        print("\n🎉 ¡Listo!")


def main():
    generator = StoryGenerator()
    generator.run_interactive()


main()
