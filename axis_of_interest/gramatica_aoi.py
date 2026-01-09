"""
Gramática para generar oraciones a partir de Axis of Interest y Plot Spans.
"""

def oracionUnicoSujeto(aoi: str, span: str, atom: str, hero: str) -> str:
    """Genera una oración con un único sujeto."""
    partes = [
        sujeto(hero),
        predicado(aoi, span, atom)
    ]
    return " ".join(partes) + "."

def oracionDosSujetos(aoi: str, span: str, atom: str, hero: str, sujeto2: str) -> str:
    """Genera una oración con dos sujetos."""
    partes = [
        sujeto(hero),
        predicado(aoi, span, atom, sujeto2)
    ]
    return " ".join(partes) + "."

def oracionMultipleSujetos(aoi: str, span: str, atom: str, hero: str, sujeto2: str, sujeto3: str) -> str:
    """Genera una oración con múltiples sujetos."""
    partes = [
        hero,
        "y", sujeto2,
        predicado(aoi, span, atom, sujeto3)
    ]
    return " ".join(partes) + "."


def sujeto(hero: str) -> str:
    """Retorna el sujeto de la oración."""
    return f"{hero}"

def predicado(aoi: str, span: str, atom: str, complemento: str = None) -> str:
    """Genera el predicado de la oración."""
    partes = [verbo(aoi, span, atom)]
    
    obj = objeto(aoi, span, atom)
    if obj:
        partes.append(obj)
    
    if complemento:
        partes.append(f"{complemento}")
    
    return " ".join(partes)

def verbo(aoi: str, span: str, atom: str) -> str:
    """Retorna el verbo según el AOI, span y atom."""
    verbos = {
        # JOURNEY
        ("JOURNEY", "Out", "Departure"): "parte",
        ("JOURNEY", "Back", "Return"): "regresa",
        
        # CONFLICT
        ("CONFLICT", "Struggle", "Struggle"): "lucha",
        ("CONFLICT", "Victory", "Victory"): "vence",
        
        # TASK
        ("TASK", "TaskSet", "DifficultTask"): "recibe",
        ("TASK", "TaskSolved", "Solution"): "completa",
        
        # DONOR
        ("DONOR", "Tested", "Tested"): "es probado",
        ("DONOR", "Tested", "Character'sReaction"): "reacciona ante",
        ("DONOR", "Tested", "ProvisionOfAMagicalAgent"): "recibe",
        ("DONOR", "UseOfAMagicalAgent", "UseOfAMagicalAgent"): "usa",
        
        # CALL TO ACTION REWARD
        ("CALL TO ACTION REWARD", "Call", "CallToAction"): "recibe",
        ("CALL TO ACTION REWARD", "Reward", "Reward"): "es recompensado",
        
        # RIVALRY
        ("RIVALRY", "RivalryDeclared", "Rivalry"): "declara una rivalidad",
        ("RIVALRY", "Cooperation", "Cooperation"): "coopera",
        ("RIVALRY", "Reconciliation", "Reconciliation"): "se reconcilia",
        
        # PURSUIT
        ("PURSUIT", "Chase", "Pursuit"): "es perseguido",
        ("PURSUIT", "Escape", "RescueFromPursuit"): "escapa",
        
        # KIDNAPPING
        ("KIDNAPPING", "Abduction", "Abduction"): "es secuestrado",
        ("KIDNAPPING", "Rescue", "Rescue"): "es rescado",
        
        # KIDNAPPING PUNISHMENT
        ("KIDNAPPING PUNISHMENT", "Kidnapping", "Abduction"): "es secuestrado",
        ("KIDNAPPING PUNISHMENT", "Rescue", "Rescue"): "rescata",
        ("KIDNAPPING PUNISHMENT", "Punishment", "Punishment"): "es castigado",
        
        # INTERDICTION VIOLATED
        ("INTERDICTION VIOLATED", "Interdiction", "Interdiction"): "es advertido",
        ("INTERDICTION VIOLATED", "Absentation", "Interdiction"): "se ausenta",
        ("INTERDICTION VIOLATED", "InterdictionViolated", "Interdiction"): "viola la prohibición",
        
        # REPENTANCE
        ("REPENTANCE", "Transformation", "Transformation"): "se transforma",
        ("REPENTANCE", "Repentance", "Repentance"): "se arrepiente",
        ("REPENTANCE", "RepentanceRewarded", "RepentanceRewarded"): "es perdonado",
        
        # RELENTING GUARDIAN
        ("RELENTING GUARDIAN", "DesireToJoin", "CoupleWantsToMarry"): "desea casarse",
        ("RELENTING GUARDIAN", "Obstacle", "UnrelentingGuardian"): "son impedidos",
        ("RELENTING GUARDIAN", "Solution", "RelentingGuardian"): "logran convencer",
        ("RELENTING GUARDIAN", "Joining", "Wedding"): "se casa",
        
        # UNRELENTING GUARDIAN
        ("UNRELENTING GUARDIAN", "DesireToJoin", "CoupleWantsToMarry"): "desea casarse",
        ("UNRELENTING GUARDIAN", "Obstacle", "UnrelentingGuardian"): "son impedidos",
        ("UNRELENTING GUARDIAN", "Solution", "HighStatusRevealed"): "intentan convencer",
        ("UNRELENTING GUARDIAN", "Joining", "Wedding"): "fracasan en casarse",
        
        # SHIFTING LOVE
        ("SHIFTING LOVE", "FirstMeeting", "BoyMeetsGirl"): "conoce",
        ("SHIFTING LOVE", "LoveShift", "LoveShift"): "cambia de amor",
        ("SHIFTING LOVE", "Reconciliation", "Reconciliation"): "se reconcilia",
        
        # RAGS 2 RICHES
        ("RAGS 2 RICHES", "Rags", "Poverty"): "vive en pobreza",
        ("RAGS 2 RICHES", "Aspiration", "Aspiration"): "aspira a más",
        ("RAGS 2 RICHES", "Transformation", "Transformation"): "se transforma",
        ("RAGS 2 RICHES", "Riches", "Reward"): "alcanza la riqueza",
    }
    return verbos.get((aoi, span, atom), verbos.get((aoi, span), "realiza una acción en"))

def objeto(aoi: str, span: str, atom: str) -> str:
    """Retorna el objeto según el AOI, span y atom."""
    objetos = {
        # JOURNEY
        ("JOURNEY", "Out", "Departure"): "hacia lo desconocido",
        ("JOURNEY", "Back", "Return"): "a casa",
        
        # CONFLICT
        ("CONFLICT", "Struggle", "Struggle"): "contra su enemigo",
        ("CONFLICT", "Victory", "Victory"): "en la batalla a",
        
        # TASK
        ("TASK", "TaskSet", "DifficultTask"): "una tarea difícil otorgada por",
        ("TASK", "TaskSolved", "Solution"): "la tarea",
        
        # DONOR
        ("DONOR", "Tested", "Tested"): "por el donante",
        ("DONOR", "Tested", "Character'sReaction"): "la prueba del donante",
        ("DONOR", "Tested", "ProvisionOfAMagicalAgent"): "un objeto mágico de",
        ("DONOR", "UseOfAMagicalAgent", "UseOfAMagicalAgent"): "el objeto mágico",
        
        # CALL TO ACTION REWARD
        ("CALL TO ACTION REWARD", "Call", "CallToAction"): "un llamado a la acción de",
        ("CALL TO ACTION REWARD", "Reward", "Reward"): "",
        
        # RIVALRY
        ("RIVALRY", "RivalryDeclared", "Rivalry"): "con",
        ("RIVALRY", "Cooperation", "Cooperation"): "con su rival",
        ("RIVALRY", "Reconciliation", "Reconciliation"): "con su rival",
        
        # PURSUIT
        ("PURSUIT", "Chase", "Pursuit"): "por",
        ("PURSUIT", "Escape", "RescueFromPursuit"): "de la persecución",
        
        # KIDNAPPING
        ("KIDNAPPING", "Abduction", "Abduction"): "por",
        ("KIDNAPPING", "Rescue", "Rescue"): "por",
        
        # KIDNAPPING PUNISHMENT
        ("KIDNAPPING PUNISHMENT", "Kidnapping", "Abduction"): "por",
        ("KIDNAPPING PUNISHMENT", "Rescue", "Rescue"): "a",
        ("KIDNAPPING PUNISHMENT", "Punishment", "Punishment"): "por el secuestro",
        
        # INTERDICTION VIOLATED
        ("INTERDICTION VIOLATED", "Interdiction", "Interdiction"): "por",
        ("INTERDICTION VIOLATED", "Absentation", "Interdiction"): "",
        ("INTERDICTION VIOLATED", "InterdictionViolated", "Interdiction"): "establecida",
        
        # REPENTANCE
        ("REPENTANCE", "Transformation", "Transformation"): "",
        ("REPENTANCE", "Repentance", "Repentance"): "",
        ("REPENTANCE", "RepentanceRewarded", "RepentanceRewarded"): "",
        
        # RELENTING GUARDIAN
        ("RELENTING GUARDIAN", "DesireToJoin", "CoupleWantsToMarry"): "con",
        ("RELENTING GUARDIAN", "Obstacle", "UnrelentingGuardian"): "por",
        ("RELENTING GUARDIAN", "Solution", "RelentingGuardian"): "a",
        ("RELENTING GUARDIAN", "Joining", "Wedding"): "con",
        
        # UNRELENTING GUARDIAN
        ("UNRELENTING GUARDIAN", "DesireToJoin", "CoupleWantsToMarry"): "con",
        ("UNRELENTING GUARDIAN", "Obstacle", "UnrelentingGuardian"): "por",
        ("UNRELENTING GUARDIAN", "Solution", "HighStatusRevealed"): "a",
        ("UNRELENTING GUARDIAN", "Joining", "Wedding"): "con",
        
        # SHIFTING LOVE
        ("SHIFTING LOVE", "FirstMeeting", "BoyMeetsGirl"): "a",
        ("SHIFTING LOVE", "LoveShift", "LoveShift"): "por",
        ("SHIFTING LOVE", "Reconciliation", "Reconciliation"): "con",
        
        # RAGS 2 RICHES
        ("RAGS 2 RICHES", "Rags", "Poverty"): "",
        ("RAGS 2 RICHES", "Aspiration", "Aspiration"): "",
        ("RAGS 2 RICHES", "Transformation", "Transformation"): "",
        ("RAGS 2 RICHES", "Riches", "Reward"): "",
        ("RAGS TO RICHES", "Richness"): "",
    }
    return objetos.get((aoi, span, atom), objetos.get((aoi, span), ""))

def interactivon_oracion(aoi: str, span: str, atom: str, heroes: list[str]) -> str:
    """Genera una oración interactiva según el número de héroes."""
    if len(heroes) == 1:
        return oracionUnicoSujeto(aoi, span, atom, heroes[0])
    elif len(heroes) == 2:
        return oracionDosSujetos(aoi, span, atom, heroes[0], heroes[1])
    else:
        sujetos = ", ".join(heroes[:-1]) + " y " + heroes[-1]
        partes = [
            sujeto(sujetos),
            predicado(aoi, span, atom)
        ]
        return " ".join(partes) + "."
    
def main():
    # Ejemplos de uso
    print("Ejemplos de generación de oraciones:\n")
    
    print("1. Un sujeto:")
    print("  ", oracionUnicoSujeto("JOURNEY", "Out", "Departure", "El héroe"))
    print("  ", oracionUnicoSujeto("TASK", "TaskSolved", "Solution", "Ana"))
    print()
    
    print("2. Dos sujetos:")
    print("  ", oracionDosSujetos("CONFLICT", "Struggle", "Struggle", "El héroe", "el villano"))
    print("  ", oracionDosSujetos("RIVALRY", "Cooperation", "Cooperation", "Juan", "María"))
    print()
    
    print("3. Múltiples sujetos:")
    print("  ", interactivon_oracion("TASK", "TaskSet", "DifficultTask", ["El héroe", "El compañero", "El mentor"]))
    print("  ", interactivon_oracion("JOURNEY", "Back", "Return", ["Sofía", "JP", "Luis"]))


if __name__ == "__main__":
    main()