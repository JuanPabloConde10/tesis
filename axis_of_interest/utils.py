def render_aoi_md(aoi: dict) -> str:
    """
    Espera un dict con esta forma mínima:
    {
      "axis": "DONOR",
      "protagonist": "tested",
      "roles": ["tested","tester","user","gift"],
      "plot_spans": [
        {"name":"Tested","events":[
          {"label":"Tested", "characters":{"tested":"X","tester":"Y"}},
          {"label":"Character’sReaction", "characters":{"tested":"X","tester":"Y"}},
          {"label":"ProvisionOfAMagicalAgent",
           "characters":{"tested":"X","tester":"Y"},
           "objects":{"gift":"Z"}}
        ]},
        {"name":"UseOfAMagicalAgent","events":[
          {"label":"UseOfAMagicalAgent","characters":{"user":"X"},"objects":{"gift":"Z"}}
        ]}
      ]
    }
    """
    def sep():
        return "\n" + ("─" * 64) + "\n"

    def fmt_block(characters=None, objects=None) -> str:
        parts = []
        if characters:
            inner = ",".join(f"{k}={v}" for k, v in characters.items())
            parts.append(f"characters({inner})")
        if objects:
            inner = ",".join(f"{k}={v}" for k, v in objects.items())
            parts.append(f"objects({inner})")
        return "  ".join(parts)

    # encabezado
    lines = []
    lines.append(f"AXISofINTEREST =  {aoi.get('axis','')}")
    lines.append(f"AXISofINTEREST PROTAGONIST =  {aoi.get('protagonist','')}")
    roles = " ".join(aoi.get("roles", []))
    lines.append(f"AXISofINTEREST ROLES =  {roles}")
    out = "\n".join(lines) + sep()

    # spans
    for ps in aoi.get("plot_spans", []):
        out += f"PLOT-SPAN-NAME =  {ps.get('name','')}\n\n"
        rows = []
        for ev in ps.get("events", []):
            right = fmt_block(ev.get("characters"), ev.get("objects"))
            rows.append((ev.get("label",""), right))

        leftw = (max((len(l) for l, _ in rows), default=0) + 2)
        for lbl, right in rows:
            out += f"{lbl.ljust(leftw)}{right}\n"
        out += sep()
    return out

from typing import Mapping

# --- utilidades pequeñas para convivir con Pydantic v1/v2 o dicts ---
def _asdict(x):
    if x is None:
        return None
    if isinstance(x, Mapping):
        return dict(x)
    if hasattr(x, "model_dump"):   # Pydantic v2
        return x.model_dump()
    if hasattr(x, "dict"):         # Pydantic v1
        return x.dict()
    return getattr(x, "__dict__", x)

def _fmt_kv(d: dict | None) -> str:
    if not d:
        return ""
    return ",".join(f"{k}={v}" for k, v in d.items())

def render_plot_schema_md(plot_schema) -> str:
    """Render lindo (Markdown/text) para un PlotSchema."""
    S = _asdict(plot_schema)

    def sep():
        return "\n" + ("─" * 64) + "\n"

    # Encabezado del PlotSchema
    header = []
    header.append(f"PLOT-SCHEMA =  {S.get('name','')}")
    if S.get("id"):
        header.append(f"ID =  {S['id']}")
    if S.get("description"):
        header.append(f"DESCRIPTION:\n{S['description']}")
    out = "\n".join(header) + sep()

    # Soporta 'plots_span' (tu esquema) y también 'plot_spans' por si acaso
    spans = S.get("plots_span") or S.get("plot_spans") or []
    for span in spans:
        SP = _asdict(span)
        out += f"AXISofINTEREST =  {SP.get('axis_of_interest','')}\n"
        out += f"PLOT-SPAN-NAME =  {SP.get('name','')}\n"
        if SP.get("description"):
            out += f"DESCRIPTION:\n{SP['description']}\n\n"

        atoms = SP.get("plots_atoms") or SP.get("plot_atoms") or []
        rows = []
        for atom in atoms:
            A = _asdict(atom)
            right_parts = []
            ch = _asdict(A.get("characters"))
            if ch:
                right_parts.append(f"characters({_fmt_kv(ch)})")
            ob = _asdict(A.get("objects"))
            if ob:
                right_parts.append(f"objects({_fmt_kv(ob)})")
            rows.append((A.get("name",""), "  ".join(right_parts), A.get("description","")))

        leftw = (max((len(name) for name, _, _ in rows), default=0) + 2)
        for name, right, desc in rows:
            out += f"{name.ljust(leftw)}{right}\n"
            if desc:
                out += f"  — {desc}\n"

        out += sep()

    return out