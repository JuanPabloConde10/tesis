from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

kidnapping_aoi = AxisOfInterest(
    id="aoi_kidnapping",
    name="KIDNAPPING",
    description="Eje narrativo 'Kidnapping' articulado en Abduction y Rescue. Etiqueta original: Abduction.",
    protagonist_role="abducted",
    roles=["abducted", "abductor", "rescuer"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="KIDNAPPING",
            name="Abduction",
            description="Etapa 'Abduction' dentro del eje 'Kidnapping'.",
            plots_atoms=[
                PlotAtom(
                    name="Abduction",
                    description="Personajes: abducted=Victim, abductor=Villain. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"abducted": "Victim", "abductor": "Villain"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="KIDNAPPING",
            name="Rescue",
            description="Etapa 'Rescue' dentro del eje 'Kidnapping'.",
            plots_atoms=[
                PlotAtom(
                    name="Rescue",
                    description="Personajes: abducted=Victim, rescuer=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"abducted": "Victim", "rescuer": "Hero"},
                    objects={},
                ),
            ],
        ),
    ],
)
