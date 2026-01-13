from pydantic import BaseModel


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
