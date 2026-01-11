from pydantic import BaseModel
from axis_of_interest.all_aoi.call_to_action_reward import call_to_action_reward_aoi
from axis_of_interest.all_aoi.conflict import conflict_aoi
from axis_of_interest.all_aoi.donor import donor_aoi
from axis_of_interest.all_aoi.interdiction_violated import interdiction_violated_aoi
from axis_of_interest.all_aoi.journey import journey_aoi
from axis_of_interest.all_aoi.kidnapping import kidnapping_aoi
from axis_of_interest.all_aoi.kidnapping_punishment import kidnapping_punishment_aoi
from axis_of_interest.all_aoi.pursuit import pursuit_aoi
from axis_of_interest.all_aoi.rags2_riches import rags2_riches_aoi
from axis_of_interest.all_aoi.relenting_guardian import relenting_guardian_aoi
from axis_of_interest.all_aoi.repentance import repentance_aoi
from axis_of_interest.all_aoi.rivalry import rivalry_aoi
from axis_of_interest.all_aoi.shifting_love import shifting_love_aoi
from axis_of_interest.all_aoi.task import task_aoi
from axis_of_interest.all_aoi.unrelenting_guardian import unrelenting_guardian_aoi


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


list_of_aoi = [
    call_to_action_reward_aoi,
    conflict_aoi,
    donor_aoi,
    interdiction_violated_aoi,
    journey_aoi,
    kidnapping_aoi,
    kidnapping_punishment_aoi,
    pursuit_aoi,
    rags2_riches_aoi,
    relenting_guardian_aoi,
    repentance_aoi,
    rivalry_aoi,
    shifting_love_aoi,
    task_aoi,
    unrelenting_guardian_aoi,
]
indice_aoi = {a.name: i for i, a in enumerate(list_of_aoi)}
