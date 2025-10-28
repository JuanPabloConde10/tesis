from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

kidnapping_punishment_aoi = AxisOfInterest(
    id="aoi_kidnapping_punishment",
    name="KIDNAPPING PUNISHMENT",
    description="Eje narrativo 'Kidnapping Punishment' articulado en Kidnapping, Rescue y Punishment. Etiqueta original: Abduction Punishment.",
    protagonist_role="abducted",
    roles=["abducted", "abductor", "rescuer", "punished"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="KIDNAPPING PUNISHMENT",
            name="Kidnapping",
            description="Etapa 'Kidnapping' dentro del eje 'Kidnapping Punishment'.",
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
            axis_of_interest="KIDNAPPING PUNISHMENT",
            name="Rescue",
            description="Etapa 'Rescue' dentro del eje 'Kidnapping Punishment'.",
            plots_atoms=[
                PlotAtom(
                    name="Rescue",
                    description="Personajes: abducted=Victim, rescuer=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"abducted": "Victim", "rescuer": "Hero"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="KIDNAPPING PUNISHMENT",
            name="Punishment",
            description="Etapa 'Punishment' dentro del eje 'Kidnapping Punishment'.",
            plots_atoms=[
                PlotAtom(
                    name="Punishment",
                    description="Personajes: punished=Villain. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"punished": "Villain"},
                    objects={},
                ),
            ],
        ),
    ],
)
