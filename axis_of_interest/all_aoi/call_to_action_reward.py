from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

call_to_action_reward_aoi = AxisOfInterest(
    id="aoi_call_to_action_reward",
    name="CALL TO ACTION REWARD",
    description="Eje narrativo 'Call To Action Reward' articulado en Call y Reward.",
    protagonist_role="called",
    roles=["called", "caller", "rewarded"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="CALL TO ACTION REWARD",
            name="Call",
            description="Etapa 'Call' dentro del eje 'Call To Action Reward'.",
            plots_atoms=[
                PlotAtom(
                    name="CallToAction",
                    description="Personajes: called=Hero, caller=Sender. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"called": "Hero", "caller": "Sender"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="CALL TO ACTION REWARD",
            name="Reward",
            description="Etapa 'Reward' dentro del eje 'Call To Action Reward'.",
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
