from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

rags2_riches_aoi = AxisOfInterest(
    id="aoi_rags2_riches",
    name="RAGS 2 RICHES",
    description="Eje narrativo 'Rags 2 Riches' articulado en Rags, Aspiration, Transformation y Riches.",
    protagonist_role="sufferer",
    roles=["sufferer", "aspirer", "transformed", "rewarded"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="RAGS 2 RICHES",
            name="Rags",
            description="Etapa 'Rags' dentro del eje 'Rags 2 Riches'.",
            plots_atoms=[
                PlotAtom(
                    name="Poverty",
                    description="Personajes: sufferer=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"sufferer": "Hero"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RAGS 2 RICHES",
            name="Aspiration",
            description="Etapa 'Aspiration' dentro del eje 'Rags 2 Riches'.",
            plots_atoms=[
                PlotAtom(
                    name="Aspiration",
                    description="Personajes: aspirer=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"aspirer": "Hero"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RAGS 2 RICHES",
            name="Transformation",
            description="Etapa 'Transformation' dentro del eje 'Rags 2 Riches'.",
            plots_atoms=[
                PlotAtom(
                    name="Transformation",
                    description="Personajes: transformed=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"transformed": "Hero"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RAGS 2 RICHES",
            name="Riches",
            description="Etapa 'Riches' dentro del eje 'Rags 2 Riches'.",
            plots_atoms=[
                PlotAtom(
                    name="Reward",
                    description="Personajes: rewarded=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"rewarded": "Hero"},
                    objects={},
                ),
            ],
        ),
    ],
)
