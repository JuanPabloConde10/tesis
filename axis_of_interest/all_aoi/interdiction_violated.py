from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

interdiction_violated_aoi = AxisOfInterest(
    id="aoi_interdiction_violated",
    name="INTERDICTION VIOLATED",
    description="Eje narrativo 'Interdiction Violated' articulado en Interdiction, Absentation y Interdiction Violated.",
    protagonist_role="interdicted",
    roles=["called", "caller", "rewarded", "interdicted", "interdicter", "absentee", "violator"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="INTERDICTION VIOLATED",
            name="Interdiction",
            description="Etapa 'Interdiction' dentro del eje 'Interdiction Violated'.",
            plots_atoms=[
                PlotAtom(
                    name="Interdiction",
                    description="Personajes: interdicted=Hero, interdicter=Sender. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"interdicted": "Hero", "interdicter": "Sender"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="INTERDICTION VIOLATED",
            name="Absentation",
            description="Etapa 'Absentation' dentro del eje 'Interdiction Violated'.",
            plots_atoms=[
                PlotAtom(
                    name="Interdiction",
                    description="Personajes: absentee=Sender. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"absentee": "Sender"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="INTERDICTION VIOLATED",
            name="InterdictionViolated",
            description="Etapa 'Interdiction Violated' dentro del eje 'Interdiction Violated'.",
            plots_atoms=[
                PlotAtom(
                    name="Interdiction",
                    description="Personajes: violator=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"violator": "Hero"},
                    objects={},
                ),
            ],
        ),
    ],
)
