EXPERIMENTS = [
    {
        "id": "exp-botanica",
        "title": "Botánica y el faro",
        "trama": (
            "En un pueblo costero, una científica descubre que un faro abandonado emite mensajes "
            "luminosos que predicen tormentas y secretos del pasado."
        ),
        "genero": "Aventura",
        "arco": "viaje_del_heroe",
        "personajes": [
            "Lina, científica marina curiosa",
            "Eloy, farero retirado que guarda el secreto del faro",
            "Nora, niña aprendiz que descifra los códigos de luz",
        ],
        "aoi_names": ["JOURNEY", "CONFLICT", "DONOR"],
        "strategy": "sequential",
    },
    {
        "id": "exp-biblioteca",
        "title": "La biblioteca sumergida",
        "trama": (
            "Una ciudad se queda sin historias cuando su biblioteca principal se hunde. "
            "Un grupo de amigos debe recuperar los relatos perdidos para evitar que el "
            "pueblo olvide quién es."
        ),
        "genero": "Fantasía contemporánea",
        "arco": "busqueda",
        "personajes": [
            "Aria, narradora callejera",
            "Tono, buzo aficionado",
            "El bibliotecario que custodia los libros sumergidos",
        ],
        "aoi_names": ["JOURNEY", "TASK", "CONFLICT"],
        "strategy": "round_robin",
    },
]


def get_experiments() -> list[dict]:
    return EXPERIMENTS
