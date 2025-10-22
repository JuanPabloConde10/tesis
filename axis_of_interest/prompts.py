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
 """


prompt_generate_plot_schema = (prompt_contexto_axis_of_interest + """
Dado los siguientes Axis of Interest: {axis_of_interest}

Genera un Plot Schema a partir de ellos.

El Plot Schema debe ser un objeto JSON válido.

El Plot Schema debe tener los siguientes campos:
- id: str
- name: str
- description: str
- plots_span: list[PlotSpan]
""")

prompt_generate_cuento = (prompt_contexto_axis_of_interest + """
Genera un cuento a partir del siguiente Plot Schema: {plot_schema}
""")
