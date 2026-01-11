from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

conflict_aoi = AxisOfInterest(
    id="aoi_conflict",
    name="CONFLICT",
    description="Conflicto: lucha y resolución (victoria) entre atacante y defensor.",
    protagonist_role="attacker",
    roles=["attacker", "defender", "winner", "loser"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="CONFLICT",
            name="Struggle",
            description="Enfrentamiento entre el atacante y el defensor.",
            plots_atoms=[
                PlotAtom(
                    name="Struggle",
                    description="El atacante (attacker=X) se enfrenta al defensor (defender=Y).",
                    characters={"attacker": "X", "defender": "Y"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="CONFLICT",
            name="Victory",
            description="Resultado del conflicto: victoria de un participante.",
            plots_atoms=[
                PlotAtom(
                    name="Victory",
                    description="El vencedor (winner=X) y el vencido (loser=Y).",
                    characters={"winner": "X", "loser": "Y"},
                    objects={},
                ),
            ],
        ),
    ],
)