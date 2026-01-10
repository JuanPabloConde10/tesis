from axis_of_interest.schemas import AxisOfInterest, PlotSchema
import json

def render_aoi_md(aoi: AxisOfInterest | dict | str) -> str:
    if isinstance(aoi, str):
        aoi_dict = json.loads(aoi)
    elif isinstance(aoi, AxisOfInterest):
        aoi_dict = aoi.model_dump()
    else:
        aoi_dict = aoi

    def sep():
        return "\n" + ("─" * 64) + "\n"

    def fmt_block(name: str, characters=None, objects=None) -> str:
        parts = [name]
        if characters:
            inner = ",".join(f"{k}={v}" for k, v in characters.items())
            parts.append(f"characters({inner})")
        if objects:
            inner = ",".join(f"{k}={v}" for k, v in objects.items())
            parts.append(f"objects({inner})")
        return "  ".join(parts)

    # encabezado
    lines = []
    lines.append(f"AXISofINTEREST =  {aoi_dict.get('name','')}")
    lines.append(f"PROTAGONIST =  {aoi_dict.get('protagonist_role','')}")
    roles = " ".join(aoi_dict.get("roles", []))
    lines.append(f"ROLES =  {roles}")
    out = "\n".join(lines) + sep()

    # spans
    for ps in aoi_dict.get("plot_spans", []):
        out += f"PLOT-SPAN-NAME =  {ps.get('name','')}\n\n"
        rows = []
        for ev in ps.get("plots_atoms", []):
            right = fmt_block(name=ev.get("name",""), characters=ev.get("characters"), objects=ev.get("objects"))
            rows.append((ev.get("label",""), right))

        leftw = (max((len(l) for l, _ in rows), default=0) + 2)
        for lbl, right in rows:
            out += f"{lbl.ljust(leftw)}{right}\n"
        out += sep()
    return out


# --- utilidades pequeñas para convivir con Pydantic v1/v2 o dicts ---

def _fmt_kv(d: dict | None) -> str:
    if not d:
        return ""
    return ",".join(f"{k}={v}" for k, v in d.items())

def render_plot_schema_md(plot_schema: PlotSchema | dict | str) -> str:
    if isinstance(plot_schema, str):
        plot_schema_dict = json.loads(plot_schema)
    elif isinstance(plot_schema, PlotSchema):
        plot_schema_dict = plot_schema.model_dump()
    else:
        plot_schema_dict = plot_schema

    """Render lindo (Markdown/text) para un PlotSchema."""

    def sep():
        return "\n" + ("─" * 64) + "\n"

    # Encabezado del PlotSchema
    header = []
    header.append(f"PLOT-SCHEMA =  {plot_schema_dict.get('name','')}")
    if plot_schema_dict.get("description"):
        header.append(f"DESCRIPTION:\n{plot_schema_dict['description']}")
    out = "\n".join(header) + sep()

    # Soporta 'plots_span' (tu esquema) y también 'plot_spans' por si acaso
    spans = plot_schema_dict.get("plots_span") or plot_schema_dict.get("plot_spans") or []
    for span in spans:
        out += f"AXISofINTEREST =  {span.get('axis_of_interest','')}\n"
        out += f"PLOT-SPAN-NAME =  {span.get('name','')}\n"
        if span.get("description"):
            out += f"DESCRIPTION:\n{span['description']}\n\n"

        atoms = span.get("plots_atoms") or span.get("plot_atoms") or []
        rows = []
        for atom in atoms:
            right_parts = []
            ch = atom.get("characters")
            if ch:
                right_parts.append(f"characters({_fmt_kv(ch)})")
            ob = atom.get("objects")
            if ob:
                right_parts.append(f"objects({_fmt_kv(ob)})")
            rows.append((atom.get("name",""), "  ".join(right_parts), atom.get("description","")))

        leftw = (max((len(name) for name, _, _ in rows), default=0) + 2)
        for name, right, desc in rows:
            out += f"{name.ljust(leftw)}{right}\n"
            if desc:
                out += f"  — {desc}\n"

        out += sep()

    return out