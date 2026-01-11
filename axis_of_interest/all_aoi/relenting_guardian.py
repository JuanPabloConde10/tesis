from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

relenting_guardian_aoi = AxisOfInterest(
    id="aoi_relenting_guardian",
    name="RELENTING GUARDIAN",
    description="Eje narrativo 'Relenting Guardian' articulado en Desire To Join, Obstacle, Solution y Joining. Etiqueta original: Unrelenting Guardian.",
    protagonist_role="attacker",
    roles=["attacker", "defender", "lover", "beloved", "guardian"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="RELENTING GUARDIAN",
            name="DesireToJoin",
            description="Etapa 'Desire To Join' dentro del eje 'Relenting Guardian'.",
            plots_atoms=[
                PlotAtom(
                    name="CoupleWantsToMarry",
                    description="Personajes: lover=Hero, beloved=Love Interest. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Love Interest"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RELENTING GUARDIAN",
            name="Obstacle",
            description="Etapa 'Obstacle' dentro del eje 'Relenting Guardian'.",
            plots_atoms=[
                PlotAtom(
                    name="UnrelentingGuardian",
                    description="Personajes: lover=Hero, beloved=Love Interest, guardian=Obstacle. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Love Interest", "guardian": "Obstacle"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RELENTING GUARDIAN",
            name="Solution",
            description="Etapa 'Solution' dentro del eje 'Relenting Guardian'.",
            plots_atoms=[
                PlotAtom(
                    name="RelentingGuardian",
                    description="Personajes: lover=Hero, beloved=Love Interest, guardian=Obstacle. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Love Interest", "guardian": "Obstacle"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="RELENTING GUARDIAN",
            name="Joining",
            description="Etapa 'Joining' dentro del eje 'Relenting Guardian'.",
            plots_atoms=[
                PlotAtom(
                    name="Wedding",
                    description="Personajes: lover=Hero, beloved=Love Interest. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"lover": "Hero", "beloved": "Love Interest"},
                    objects={},
                ),
            ],
        ),
    ],
)
