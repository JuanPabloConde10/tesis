from axis_of_interest.schemas import AxisOfInterest, PlotSpan, PlotAtom

task_aoi = AxisOfInterest(
    id="aoi_task",
    name="TASK",
    description="Eje narrativo 'Task' articulado en Task Set y Task Solved.",
    protagonist_role="solver",
    roles=["setter", "solver"],
    plot_spans=[
        PlotSpan(
            axis_of_interest="TASK",
            name="TaskSet",
            description="Etapa 'Task Set' dentro del eje 'Task'.",
            plots_atoms=[
                PlotAtom(
                    name="DifficultTask",
                    description="Personajes: solver=Hero, setter=Dispatcher. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"solver": "Hero", "setter": "Dispatcher"},
                    objects={},
                ),
            ],
        ),
        PlotSpan(
            axis_of_interest="TASK",
            name="TaskSolved",
            description="Etapa 'Task Solved' dentro del eje 'Task'.",
            plots_atoms=[
                PlotAtom(
                    name="Solution",
                    description="Personajes: solver=Hero. Objetos: ninguno. Ubicaciones: no registradas.",
                    characters={"solver": "Hero"},
                    objects={},
                ),
            ],
        ),
    ],
)
