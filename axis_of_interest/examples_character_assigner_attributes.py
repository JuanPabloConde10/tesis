"""
Casos de prueba manuales para asignación de personajes por atributos.

Ejecutar:
    python axis_of_interest/examples_character_assigner_attributes.py
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from axis_of_interest.schema_generator import PlotSchemaGenerator
from axis_of_interest.character_assigner import assign_character_names_by_attributes
from axis_of_interest.character_attributes import Character, CharacterAttributes


def _validate_span_consistency(schema):
    """Valida que un mismo rol mantenga el mismo personaje dentro del span,
    y que no se repitan personajes dentro del mismo span.
    """
    for span in schema.plots_span:
        role_to_name = {}
        for atom in span.plots_atoms:
            for role, name in atom.characters.items():
                if role in role_to_name and role_to_name[role] != name:
                    raise AssertionError(
                        f"Rol inconsistente en span {span.axis_of_interest}/{span.name}: "
                        f"{role_to_name[role]} vs {name}"
                    )
                role_to_name[role] = name

        names = list(role_to_name.values())
        if len(set(names)) != len(names):
            raise AssertionError(
                f"Personajes repetidos en span {span.axis_of_interest}/{span.name}: "
                f"{names}"
            )


def _print_assignments(schema, title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    for span in schema.plots_span:
        role_to_name = {}
        for atom in span.plots_atoms:
            for role, name in atom.characters.items():
                role_to_name.setdefault(role, name)
        roles_str = ", ".join(f"{r}={n}" for r, n in role_to_name.items())
        print(f"- {span.axis_of_interest}/{span.name}: {roles_str}")


def caso_1_conflict_basico():
    generator = PlotSchemaGenerator()
    schema = generator.generate_schema(
        schema_name="Test CONFLICT",
        aoi_names=["CONFLICT"],
        interleaving_strategy="sequential",
    )

    characters = [
        Character(
            name="Maria",
            attributes=CharacterAttributes(valentia=5, bondad=4, astucia=3, maldad=1, carisma=5),
        ),
        Character(
            name="Jorge",
            attributes=CharacterAttributes(valentia=4, bondad=1, astucia=4, maldad=5, carisma=4),
        ),
    ]

    schema_named = assign_character_names_by_attributes(schema, characters, allow_reuse=True)
    _validate_span_consistency(schema_named)
    _print_assignments(schema_named, "Caso 1: CONFLICT básico (2 personajes)")


def caso_2_donor_conflict():
    generator = PlotSchemaGenerator()
    schema = generator.generate_schema(
        schema_name="Test DONOR + CONFLICT",
        aoi_names=["DONOR", "CONFLICT"],
        interleaving_strategy="sequential",
    )

    characters = [
        Character(
            name="Alice",
            attributes=CharacterAttributes(valentia=4, bondad=5, astucia=3, maldad=1, carisma=4),
        ),
        Character(
            name="Bob",
            attributes=CharacterAttributes(valentia=3, bondad=4, astucia=5, maldad=1, carisma=5),
        ),
        Character(
            name="Carmen",
            attributes=CharacterAttributes(valentia=4, bondad=2, astucia=4, maldad=4, carisma=4),
        ),
        Character(
            name="Diego",
            attributes=CharacterAttributes(valentia=2, bondad=4, astucia=2, maldad=1, carisma=2),
        ),
    ]

    schema_named = assign_character_names_by_attributes(schema, characters, allow_reuse=True)
    _validate_span_consistency(schema_named)
    _print_assignments(schema_named, "Caso 2: DONOR + CONFLICT (4 personajes)")


def caso_3_journey_task_conflict():
    generator = PlotSchemaGenerator()
    schema = generator.generate_schema(
        schema_name="Test JOURNEY + TASK + CONFLICT",
        aoi_names=["JOURNEY", "TASK", "CONFLICT"],
        interleaving_strategy="parallel",
    )

    characters = [
        Character(
            name="Luna",
            attributes=CharacterAttributes(valentia=5, bondad=4, astucia=3, maldad=1, carisma=5),
        ),
        Character(
            name="Nico",
            attributes=CharacterAttributes(valentia=4, bondad=3, astucia=4, maldad=2, carisma=4),
        ),
        Character(
            name="Omar",
            attributes=CharacterAttributes(valentia=3, bondad=1, astucia=4, maldad=5, carisma=4),
        ),
        Character(
            name="Paula",
            attributes=CharacterAttributes(valentia=3, bondad=5, astucia=3, maldad=1, carisma=4),
        ),
        Character(
            name="Quin",
            attributes=CharacterAttributes(valentia=2, bondad=4, astucia=2, maldad=1, carisma=2),
        ),
    ]

    schema_named = assign_character_names_by_attributes(schema, characters, allow_reuse=True)
    _validate_span_consistency(schema_named)
    _print_assignments(schema_named, "Caso 3: JOURNEY + TASK + CONFLICT (5 personajes)")


def main():
    caso_1_conflict_basico()
    caso_2_donor_conflict()
    caso_3_journey_task_conflict()
    print("\n✅ Todos los casos pasaron validación.")


if __name__ == "__main__":
    main()
