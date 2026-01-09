"""
Test de la gramática: genera una oración por cada plot span de cada AOI.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from axis_of_interest.schemas import list_of_aoi
from axis_of_interest.gramatica_aoi import oracionUnicoSujeto, oracionDosSujetos, oracionMultipleSujetos


def test_all_spans():
    """Genera una oración de ejemplo para cada plot span de cada AOI."""
    
    print("="*80)
    print("TEST DE GRAMÁTICA - Generando oraciones para todos los AOIs y Spans")
    print("="*80)
    print()
    
    for aoi in list_of_aoi:
        print(f"\n{'─'*80}")
        print(f"AOI: {aoi.name}")
        print(f"{'─'*80}")
        
        for span in aoi.plot_spans:
            # Determinar cuántos personajes necesitamos
            # Miramos el primer atom del span para saber cuántos roles hay
            if span.plots_atoms:
                first_atom = span.plots_atoms[0]
                num_chars = len(first_atom.characters)
                atom_name = first_atom.name
                
                if num_chars == 1:
                    oracion = oracionUnicoSujeto(aoi.name, span.name, atom_name, "Ana")
                else :
                    if num_chars == 2:
                        oracion = oracionDosSujetos(aoi.name, span.name, atom_name, "Ana", "Luis")
                    else :
                        oracion = oracionMultipleSujetos(aoi.name, span.name, atom_name, "Ana", "Luis", "María")
                
                print(f"  [{span.name}] {oracion}")
            else:
                print(f"  [{span.name}] (sin atoms)")
        
        print()


if __name__ == "__main__":
    test_all_spans()
