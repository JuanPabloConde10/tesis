from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom
donor_aoi = AxisOfInterest(
    id="aoi_donor",
    name="DONOR",
    description="Secuencia del Donante (Propp): prueba del héroe, reacción y provisión/uso del agente mágico.",
    protagonist_role="tested",
    roles=["tested", "tester", "user", "gift"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="DONOR",
            name="Tested",
            description="El protagonista (tested=X) es puesto a prueba por el donante (tester=Y).",
            plots_atoms=[
                PlotAtom(
                    name="Tested",
                    description="El protagonista (tested=X) es puesto a prueba por el donante (tester=Y).",
                    characters={"tested": "X", "tester": "Y"},
                    objects={},
                ),
                PlotAtom(
                    name="Character'sReaction",
                    description="Reacción del protagonista ante la prueba.",
                    characters={"tested": "X", "tester": "Y"},
                    objects={},
                ),
                PlotAtom(
                    name="ProvisionOfAMagicalAgent",
                    description="El donante otorga un agente mágico si la prueba es superada.",
                    characters={"tested": "X", "tester": "Y"},
                    objects={"gift": "Z"},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="DONOR",
            name="UseOfAMagicalAgent",
            description="El usuario (user=X) utiliza el agente mágico (gift=Z).",
            plots_atoms=[
                PlotAtom(
                    name="UseOfAMagicalAgent",
                    description="El usuario (user=X) utiliza el agente mágico (gift=Z).",
                    characters={"user": "X"},
                    objects={"gift": "Z"},
                ),
            ],
        ),
    ],
)
