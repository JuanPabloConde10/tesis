"""
Generador de Plot Schemas a partir de Axis of Interest.
Permite combinar e intercalar plot spans de diferentes AOIs para crear narrativas complejas.
"""

import random
from typing import List, Optional
from axis_of_interest.schemas import AxisOfInterest, PlotSchema, PlotSpan
from axis_of_interest.registry import list_of_aoi


class PlotSchemaGenerator:
    """
    Genera PlotSchemas combinando e intercalando plot spans de diferentes Axis of Interest.

    Ejemplo de uso:
        generator = PlotSchemaGenerator()

        # Generar schema intercalando AOIs
        schema = generator.generate_schema(
            schema_name="Hero's Journey with Conflict",
            aoi_names=["JOURNEY", "CONFLICT", "TASK"],
            interleaving_strategy="sequential"
        )
    """

    def __init__(self, available_aois: Optional[List[AxisOfInterest]] = None):
        """
        Inicializa el generador con una lista de AOIs disponibles.

        Args:
            available_aois: Lista de AOIs disponibles. Si no se proporciona, usa todos los AOIs definidos.
        """
        self.available_aois = available_aois or list_of_aoi
        self.aoi_index = {aoi.name: aoi for aoi in self.available_aois}

    def get_aoi_by_name(self, name: str) -> Optional[AxisOfInterest]:
        """Obtiene un AOI por su nombre."""
        return self.aoi_index.get(name)

    def generate_schema(
        self,
        schema_name: str,
        aoi_names: List[str],
        interleaving_strategy: str = "sequential",
        schema_description: Optional[str] = None,
        schema_id: Optional[str] = None,
    ) -> PlotSchema:
        """
        Genera un PlotSchema intercalando los plot spans de los AOIs especificados.

        Args:
            schema_name: Nombre del schema a generar
            aoi_names: Lista de nombres de AOIs a combinar (ej: ["JOURNEY", "CONFLICT"])
            interleaving_strategy: Estrategia de intercalado:
                - "sequential": Concatena todos los spans del primer AOI, luego del segundo, etc.
                - "round_robin": Intercala spans tomando uno de cada AOI en orden circular
                - "parallel": Agrupa spans por índice (primer span de cada AOI, luego segundo, etc.)
                - "random": Elige aleatoriamente entre los AOIs, respetando el orden interno de cada uno
            schema_description: Descripción opcional del schema
            schema_id: ID opcional del schema (se genera automáticamente si no se proporciona)

        Returns:
            PlotSchema con los plot spans intercalados

        Raises:
            ValueError: Si algún AOI no existe
        """
        # Validar que todos los AOIs existen
        selected_aois = []
        for aoi_name in aoi_names:
            aoi = self.get_aoi_by_name(aoi_name)
            if not aoi:
                raise ValueError(
                    f"AOI '{aoi_name}' no encontrado. AOIs disponibles: {list(self.aoi_index.keys())}"
                )
            selected_aois.append(aoi)

        # Intercalar plot spans según la estrategia
        if interleaving_strategy == "sequential":
            interleaved_spans = self._interleave_sequential(selected_aois)
        elif interleaving_strategy == "round_robin":
            interleaved_spans = self._interleave_round_robin(selected_aois)
        elif interleaving_strategy == "parallel":
            interleaved_spans = self._interleave_parallel(selected_aois)
        elif interleaving_strategy == "random":
            interleaved_spans = self._interleave_random(selected_aois)
        else:
            raise ValueError(
                f"Estrategia '{interleaving_strategy}' no reconocida. "
                f"Usa: 'sequential', 'round_robin', 'parallel', o 'random'"
            )

        # Generar ID si no se proporciona
        if not schema_id:
            schema_id = f"schema_{'_'.join(aoi_name.lower() for aoi_name in aoi_names)}"

        # Generar descripción si no se proporciona
        if not schema_description:
            schema_description = (
                f"Plot schema combinando {len(selected_aois)} axis of interest: "
                f"{', '.join(aoi.name for aoi in selected_aois)} "
                f"usando estrategia '{interleaving_strategy}'"
            )

        return PlotSchema(
            id=schema_id,
            name=schema_name,
            description=schema_description,
            plots_span=interleaved_spans,
        )

    def _interleave_sequential(self, aois: List[AxisOfInterest]) -> List[PlotSpan]:
        """
        Estrategia secuencial: concatena todos los spans de cada AOI en orden.

        Ejemplo: [AOI1.span1, AOI1.span2, AOI2.span1, AOI2.span2, AOI3.span1]
        """
        result = []
        for aoi in aois:
            result.extend(aoi.plot_spans)
        return result

    def _interleave_round_robin(self, aois: List[AxisOfInterest]) -> List[PlotSpan]:
        """
        Estrategia round-robin: intercala spans tomando uno de cada AOI circularmente.

        Ejemplo: [AOI1.span1, AOI2.span1, AOI3.span1, AOI1.span2, AOI2.span2]
        """
        result = []
        # Crear iteradores para cada AOI
        iterators = [iter(aoi.plot_spans) for aoi in aois]
        active_iterators = list(range(len(iterators)))

        # Mientras haya iteradores activos
        while active_iterators:
            for i in list(active_iterators):  # Copiar lista para poder modificarla
                try:
                    span = next(iterators[i])
                    result.append(span)
                except StopIteration:
                    active_iterators.remove(i)

        return result

    def _interleave_parallel(self, aois: List[AxisOfInterest]) -> List[PlotSpan]:
        """
        Estrategia paralela: agrupa spans por índice.

        Ejemplo: [AOI1.span1, AOI2.span1, AOI3.span1, AOI1.span2, AOI2.span2, AOI3.span2]
        """
        result = []
        max_spans = max(len(aoi.plot_spans) for aoi in aois) if aois else 0

        for idx in range(max_spans):
            for aoi in aois:
                if idx < len(aoi.plot_spans):
                    result.append(aoi.plot_spans[idx])

        return result

    def _interleave_random(self, aois: List[AxisOfInterest]) -> List[PlotSpan]:
        """
        Estrategia aleatoria: elige aleatoriamente entre los AOIs disponibles,
        pero respetando el orden interno de cada AOI.

        Es decir, si JOURNEY tiene [Out, Back], primero debe aparecer Out antes que Back.
        Pero el orden entre diferentes AOIs es aleatorio.

        Ejemplo posible: [AOI2.span1, AOI1.span1, AOI3.span1, AOI1.span2, AOI3.span2, AOI2.span2]
        """
        result = []
        # Mantener un índice de posición actual para cada AOI
        aoi_positions = {i: 0 for i in range(len(aois))}

        # Mientras haya spans por agregar
        while any(pos < len(aois[i].plot_spans) for i, pos in aoi_positions.items()):
            # Obtener lista de AOIs que aún tienen spans disponibles
            available_aois = [
                i for i, pos in aoi_positions.items() if pos < len(aois[i].plot_spans)
            ]

            if not available_aois:
                break

            # Elegir aleatoriamente uno de los AOIs disponibles
            chosen_aoi_idx = random.choice(available_aois)

            # Agregar el siguiente span de ese AOI
            pos = aoi_positions[chosen_aoi_idx]
            result.append(aois[chosen_aoi_idx].plot_spans[pos])

            # Incrementar la posición para ese AOI
            aoi_positions[chosen_aoi_idx] += 1

        return result

    def generate_custom_schema(
        self,
        schema_name: str,
        plot_spans: List[PlotSpan],
        schema_description: Optional[str] = None,
        schema_id: Optional[str] = None,
    ) -> PlotSchema:
        """
        Genera un PlotSchema con plot spans especificados manualmente.

        Útil cuando quieres control total sobre el orden de los spans.

        Args:
            schema_name: Nombre del schema
            plot_spans: Lista de PlotSpans en el orden deseado
            schema_description: Descripción opcional
            schema_id: ID opcional

        Returns:
            PlotSchema con los spans especificados
        """
        if not schema_id:
            schema_id = f"schema_custom_{schema_name.lower().replace(' ', '_')}"

        if not schema_description:
            schema_description = f"Custom plot schema: {schema_name}"

        return PlotSchema(
            id=schema_id,
            name=schema_name,
            description=schema_description,
            plots_span=plot_spans,
        )

    def list_available_aois(self) -> List[str]:
        """Retorna lista de nombres de todos los AOIs disponibles."""
        return list(self.aoi_index.keys())

    def get_aoi_info(self, aoi_name: str) -> Optional[dict]:
        """
        Obtiene información detallada de un AOI.

        Returns:
            Diccionario con información del AOI o None si no existe
        """
        aoi = self.get_aoi_by_name(aoi_name)
        if not aoi:
            return None

        return {
            "id": aoi.id,
            "name": aoi.name,
            "description": aoi.description,
            "protagonist_role": aoi.protagonist_role,
            "roles": aoi.roles,
            "num_plot_spans": len(aoi.plot_spans),
            "plot_span_names": [span.name for span in aoi.plot_spans],
        }


# Función de conveniencia para uso rápido
def create_plot_schema(
    schema_name: str,
    aoi_names: List[str],
    strategy: str = "sequential",
    description: Optional[str] = None,
) -> PlotSchema:
    """
    Función de conveniencia para crear un plot schema rápidamente.

    Args:
        schema_name: Nombre del schema
        aoi_names: Lista de nombres de AOIs (ej: ["JOURNEY", "CONFLICT"])
        strategy: Estrategia de intercalado ("sequential", "round_robin", "parallel")
        description: Descripción opcional

    Returns:
        PlotSchema generado

    Ejemplo:
        schema = create_plot_schema(
            "Epic Quest",
            ["JOURNEY", "TASK", "CONFLICT"],
            strategy="parallel"
        )
    """
    generator = PlotSchemaGenerator()
    return generator.generate_schema(
        schema_name=schema_name,
        aoi_names=aoi_names,
        interleaving_strategy=strategy,
        schema_description=description,
    )
