from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

shifting_love_aoi = AxisOfInterest(
    id="aoi_shifting_love",
    name="SHIFTING LOVE",
    description="Eje narrativo 'Shifting Love' articulado en First Meeting, Love Shift y Reconciliation.",
    protagonist_role="lover",
    roles=["lover", "beloved", "rival"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="SHIFTING LOVE",
            name="FirstMeeting",
            description="Etapa 'First Meeting' dentro del eje 'Shifting Love'.",
            plots_atoms=[
                PlotAtom(
                    name="BoyMeetsGirl",
                    description="Personajes: lover=Hero, beloved=Love Interest. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Love Interest"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="SHIFTING LOVE",
            name="LoveShift",
            description="Etapa 'Love Shift' dentro del eje 'Shifting Love'.",
            plots_atoms=[
                PlotAtom(
                    name="LoveShift",
                    description="Personajes: lover=Hero, beloved=Love Interest, rival=Shadow. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Love Interest", "rival": "Shadow"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="SHIFTING LOVE",
            name="Reconciliation",
            description="Etapa 'Reconciliation' dentro del eje 'Shifting Love'.",
            plots_atoms=[
                PlotAtom(
                    name="Reconciliation",
                    description="Personajes: lover=Hero, beloved=Love Interest. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Love Interest"},
                    objects={},
                ),
            ],
        ),
    ],
)
