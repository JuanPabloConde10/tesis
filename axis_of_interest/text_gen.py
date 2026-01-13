

from axis_of_interest.gramatica_aoi import oracionDosSujetos, oracionUnicoSujeto,oracionMultipleSujetos
from axis_of_interest.schemas import PlotSchema


def generate_text(schema: PlotSchema) -> str:
    text = ""
    for i in schema.plots_span:
        for j in i.plots_atoms:
            
            if len(j.characters) == 1:
                text += oracionUnicoSujeto(i.axis_of_interest, i.name, j.name, list(j.characters.values())[0]) + "\n"
            else:
                if len(j.characters) == 2:
                    text += oracionDosSujetos(i.axis_of_interest, i.name, j.name, list(j.characters.values())[0], list(j.characters.values())[1]) + "\n"
                else:
                    text += oracionMultipleSujetos(i.axis_of_interest, i.name, j.name, list(j.characters.values())[0], list(j.characters.values())[1], list(j.characters.values())[2]) + "\n"
    return text