from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

repentance_aoi = AxisOfInterest(
    id="aoi_repentance",
    name="REPENTANCE",
    description="Eje narrativo 'Repentance' articulado en Transformation, Repentance y Repentance Rewarded.",
    protagonist_role="transformed",
    roles=["transformed", "repenter", "rewarded"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="REPENTANCE",
            name="Transformation",
            description="Etapa 'Transformation' dentro del eje 'Repentance'.",
            plots_atoms=[
                PlotAtom(
                    name="Transformation",
                    description="Personajes: transformed=Villain. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"transformed": "Villain"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="REPENTANCE",
            name="Repentance",
            description="Etapa 'Repentance' dentro del eje 'Repentance'.",
            plots_atoms=[
                PlotAtom(
                    name="Repentance",
                    description="Personajes: repenter=Villain. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"repenter": "Villain"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="REPENTANCE",
            name="RepentanceRewarded",
            description="Etapa 'Repentance Rewarded' dentro del eje 'Repentance'.",
            plots_atoms=[
                PlotAtom(
                    name="RepentanceRewarded",
                    description="Personajes: rewarded=Villain. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"rewarded": "Villain"},
                    objects={},
                ),
            ],
        ),
    ],
)
