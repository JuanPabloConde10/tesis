from pydantic import BaseModel
import importlib
import pkgutil


class PlotAtom(BaseModel):
    name: str
    characters: dict[str, str]
    objects: dict[str, str]
    description: str


class PlotSpan(BaseModel):
    axis_of_interest: str
    name: str
    description: str
    plots_atoms: list[PlotAtom]


class PlotSchema(BaseModel):
    id: str
    name: str
    description: str
    plots_span: list[PlotSpan]


class AxisOfInterest(BaseModel):
    id: str
    name: str
    protagonist_role: str
    description: str
    roles: list[str]
    plot_spans: list[PlotSpan]


list_of_aoi = []

# Primero, añadir cualquier AOI definido localmente en este módulo
for local in ("donor_aoi", "conflict_aoi"):
    if local in globals():
        list_of_aoi.append(globals()[local])

try:
    import axis_of_interest.all_aoi as _all_aoi_pkg

    for _finder, _name, _ispkg in pkgutil.iter_modules(_all_aoi_pkg.__path__):
        mod = importlib.import_module(f"axis_of_interest.all_aoi.{_name}")
        # recoger atributos que terminen en `_aoi`
        for attr in dir(mod):
            if attr.endswith("_aoi"):
                obj = getattr(mod, attr)
                if obj not in list_of_aoi:
                    list_of_aoi.append(obj)
except Exception:
    # Si ocurre algún error, list_of_aoi seguirá con los AOIs locales (mínimo)
    pass

indice_aoi = {a.name: i for i, a in enumerate(list_of_aoi)}
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

conflict_aoi = AxisOfInterest(
    id="aoi_conflict",
    name="CONFLICT",
    description="Conflicto: lucha y resolución (victoria) entre atacante y defensor.",
    protagonist_role="attacker",
    roles=["attacker", "defender", "winner", "looser"],
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
                    description="El vencedor (winner=X) y el vencido (looser=Y).",
                    characters={"winner": "X", "looser": "Y"},
                    objects={},
                ),
            ],
        ),
    ],
)
