from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

unrelenting_guardian_aoi = AxisOfInterest(
    id="aoi_unrelenting_guardian",
    name="UNRELENTING GUARDIAN",
    description="Eje narrativo 'Unrelenting Guardian' articulado en Desire To Join, Obstacle, Solution y Joining.",
    protagonist_role="attacker",
    roles=["attacker", "defender", "lover", "beloved", "guardian"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="UNRELENTING GUARDIAN",
            name="DesireToJoin",
            description="Etapa 'Desire To Join' dentro del eje 'Unrelenting Guardian'.",
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
            axis_of_interest="UNRELENTING GUARDIAN",
            name="Obstacle",
            description="Etapa 'Obstacle' dentro del eje 'Unrelenting Guardian'.",
            plots_atoms=[
                PlotAtom(
                    name="UnrelentingGuardian",
                    description="Personajes: lover=Hero, beloved=Love Interest, guardian=Obstacle. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={
                        "lover": "Hero",
                        "beloved": "Love Interest",
                        "guardian": "Obstacle",
                    },
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="UNRELENTING GUARDIAN",
            name="Solution",
            description="Etapa 'Solution' dentro del eje 'Unrelenting Guardian'.",
            plots_atoms=[
                PlotAtom(
                    name="HighStatusRevealed",
                    description="Personajes: lover=Hero, beloved=Love Interest, guardian=Obstacle. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={
                        "lover": "Hero",
                        "beloved": "Love Interest",
                        "guardian": "Obstacle",
                    },
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="UNRELENTING GUARDIAN",
            name="Joining",
            description="Etapa 'Joining' dentro del eje 'Unrelenting Guardian'.",
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
