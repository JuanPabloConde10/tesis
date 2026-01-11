from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

pursuit_aoi = AxisOfInterest(
    id="aoi_pursuit",
    name="PURSUIT",
    description="Eje narrativo 'Pursuit' articulado en Chase y Escape.",
    protagonist_role="pursued",
    roles=["pursuer", "pursued"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="PURSUIT",
            name="Chase",
            description="Etapa 'Chase' dentro del eje 'Pursuit'.",
            plots_atoms=[
                PlotAtom(
                    name="Pursuit",
                    description="Personajes: pursued=Hero, pursuer=Villain. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"pursued": "Hero", "pursuer": "Villain"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="PURSUIT",
            name="Escape",
            description="Etapa 'Escape' dentro del eje 'Pursuit'.",
            plots_atoms=[
                PlotAtom(
                    name="RescueFromPursuit",
                    description="Personajes: pursued=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"pursued": "Hero"},
                    objects={},
                ),
            ],
        ),
    ],
)
