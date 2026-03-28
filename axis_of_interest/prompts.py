prompt_contexto_axis_of_interest = """
Eres un experto en narrativa. Estas trabajando en un proyecto de escritura de cuentos siguiendo un metodo neuro-simbolico.

Este enfoque sigue la siguiente estructura:
- El plot de la historia se representa como un plot schema
- El plot schema está compuesto por plots span, los cuales representan algo parecido a una escena de la historia.
- Cada plot span está compuesto por plots atoms, los cuales representan algo parecido a un atomo de la historia.
- Cada plot atom está compuesto por un nombre y una descripción.
- A su vez, tenemos los axis of interest, los cuales representan los ejes narrativos de la historia.
- Cada plot span está asociado a un axis of interest.
- Los axis of interest nacen con el fin de manejar la coherencia narrativa de la historia y llevar relaciones de largo alcance entre los spans.

Ejemplo de Plot Schema: 

plot_schema_donor_fight = PlotSchema(
    id="plot_schema_donor_fight",
    name="DONOR-FIGHT",
    description=(
        "Trama básica que combina DONOR y CONFLICT: el héroe es probado, "
        "obtiene/usa un agente mágico y vence al villano. PROTAGONIST=hero."
    ),
    plots_span=[
        # DONOR — Tested
        PlotSpan(
            axis_of_interest="DONOR",
            name="Tested",
            description="El héroe (tested=hero) es probado por el donante (tester=donor).",
            plots_atoms=[
                PlotAtom(
                    name="Tested",
                    characters={"tested": "hero", "tester": "donor"},
                    # Incluimos gift=gift para reflejar el link de la tabla
                    objects={"gift": "gift"},
                    description="Prueba del héroe por parte del donante."
                )
            ],
        ),
        # CONFLICT — Struggle
        PlotSpan(
            axis_of_interest="CONFLICT",
            name="Struggle",
            description="Lucha entre el héroe atacante y el villano defensor.",
            plots_atoms=[
                PlotAtom(
                    name="Struggle",
                    characters={"attacker": "hero", "defender": "villain"},
                    objects={},
                    description="Enfrentamiento directo."
                )
            ],
        ),
        # DONOR — UseOfAMagicalAgent
        PlotSpan(
            axis_of_interest="DONOR",
            name="UseOfAMagicalAgent",
            description="El héroe usa el agente mágico otorgado por el donante.",
            plots_atoms=[
                PlotAtom(
                    name="UseOfAMagicalAgent",
                    characters={"user": "hero"},
                    objects={"gift": "gift"},
                    description="Uso del agente mágico por el héroe."
                )
            ],
        ),
        # CONFLICT — Victory
        PlotSpan(
            axis_of_interest="CONFLICT",
            name="Victory",
            description="Resolución del conflicto a favor del héroe.",
            plots_atoms=[
                PlotAtom(
                    name="Victory",
                    characters={"winner": "hero", "looser": "villain"},
                    objects={},
                    description="El héroe vence al villano."
                )
            ],
        ),
    ],
)
 """


template_prompt_generate_plot_schema = (
    prompt_contexto_axis_of_interest
    + """
Dado los siguientes Axis of Interest: {axis_of_interest}

Genera un Plot Schema a partir de ellos.

El Plot Schema debe ser un objeto JSON válido.

El Plot Schema debe tener los siguientes campos:
- id: str
- name: str
- description: str
- plots_span: list[PlotSpan]
"""
)

template_prompt_generate_cuento = (
    prompt_contexto_axis_of_interest
    + """
Genera un cuento a partir del siguiente Plot Schema.

El input del usuario debe usarse como una DESCRIPCIÓN GENERAL DEL AMBIENTE,
el contexto y el tono de la historia (no como la trama central).

IMPORTANTE: El cuento debe tener un MÁXIMO de 500 palabras y un MÍNIMO de 250 palabras.
No respondas con una sola línea ni con frases incompletas.

Ambiente (input del usuario): {ambiente}
{genero_section}

Personajes (si se proveen):
{characters_section}

Usá la descripción de los personajes solo como guía; NO la copies textual.

Si hay género, instanciá los Axis of Interest con elementos, conflictos y escenas coherentes con ese género, manteniendo la coherencia narrativa y las relaciones de largo alcance entre los spans.

Plot Schema: {plot_schema}

Generá el cuento completo (entre 250 y 500 palabras):
IMPORTANTE: 
- El cuento debe tener un MÁXIMO de 500 palabras
- NO incluyas las frases originales tal cual están                                   
"""
)

template_prompt_generate_cuento_gramatica = """
Sos un escritor experto. Te voy a dar un esqueleto de historia compuesto por frases cortas y simples.

Tu tarea es transformar estas frases en un cuento completo y coherente. NO copies las frases literalmente. En su lugar:
- Transformá cada acción en escenas detalladas con descripciones vívidas
- Agregá diálogos naturales entre los personajes
- Desarrollá la personalidad y motivaciones de cada personaje
- Creá atmósfera y tensión narrativa
- Conectá las escenas con transiciones fluidas

IMPORTANTE: 
- El cuento debe tener un MÁXIMO de 500 palabras
- NO incluyas las frases originales tal cual están
- Mantené la secuencia de eventos pero transformá completamente cómo se cuentan

Frases del esqueleto:

{texto_gramatica}

Generá el cuento completo (máximo 500 palabras), transformando creativamente cada frase del esqueleto:
"""

template_prompt_interleave_llm = (
        prompt_contexto_axis_of_interest
        + """
Dado el siguiente listado de PLOT SPANS (con id único), devolvé el mejor orden narrativo posible
para intercalarlos en un único Plot Schema. Debés incluir TODOS los ids exactamente una vez.

Formato de salida: un JSON ARRAY estricto de strings con los ids en el orden elegido.
No incluyas texto adicional.

Listado de spans (JSON):
<<SPANS_JSON>>

Salida esperada (ejemplo):
[
    "JOURNEY::0",
    "CONFLICT::0",
    "JOURNEY::1"
]
"""
)

tenplate_prompt_generar_axis_of_interest = (
    prompt_contexto_axis_of_interest
    + """ 
Dado las caracteristicas de esta historia {data} y los siguientes axis_of_interest {axis_of_interest}, devuelve una lista de Axis of Interest que abarquen la historia. 

La lista tiene que contener solo los nombres

"""
)
