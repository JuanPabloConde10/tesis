from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

rivalry_aoi = AxisOfInterest(
    id="aoi_rivalry",
    name="RIVALRY",
    description="Eje narrativo 'Rivalry' articulado en Rivalry Declared, Cooperation y Reconciliation.",
    protagonist_role="traveller",
    roles=["traveller", "rival1", "rival2", "participant1", "participant2", "lover", "beloved"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="RIVALRY",
            name="RivalryDeclared",
            description="Etapa 'Rivalry Declared' dentro del eje 'Rivalry'.",
            plots_atoms=[
                PlotAtom(
                    name="Rivalry",
                    description="Personajes: rival1=Hero, rival2=Shadow. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"rival1": "Hero", "rival2": "Shadow"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RIVALRY",
            name="Cooperation",
            description="Etapa 'Cooperation' dentro del eje 'Rivalry'.",
            plots_atoms=[
                PlotAtom(
                    name="Cooperation",
                    description="Personajes: participant1=Hero, participant2=Shadow. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"participant1": "Hero", "participant2": "Shadow"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RIVALRY",
            name="Reconciliation",
            description="Etapa 'Reconciliation' dentro del eje 'Rivalry'.",
            plots_atoms=[
                PlotAtom(
                    name="Reconciliation",
                    description="Personajes: lover=Hero, beloved=Shadow. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Shadow"},
                    objects={},
                ),
            ],
        ),
    ],
)
