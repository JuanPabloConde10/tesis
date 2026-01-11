from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

journey_aoi = AxisOfInterest(
    id="aoi_journey",
    name="JOURNEY",
    description="Eje narrativo 'Journey' articulado en Out y Back.",
    protagonist_role="traveller",
    roles=["traveller"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="JOURNEY",
            name="Out",
            description="Etapa 'Out' dentro del eje 'Journey'.",
            plots_atoms=[
                PlotAtom(
                    name="Departure",
                    description="Personajes: traveller=Hero. Objetos: ninguno. Ubicaciones: origin=Home, destination=Elsewhere.",
                    characters={"traveller": "Hero"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="JOURNEY",
            name="Back",
            description="Etapa 'Back' dentro del eje 'Journey'.",
            plots_atoms=[
                PlotAtom(
                    name="Return",
                    description="Personajes: traveller=Hero. Objetos: ninguno. Ubicaciones: origin=Elsewhere, destination=Home.",
                    characters={"traveller": "Hero"},
                    objects={},
                ),
            ],
        ),
    ],
)
