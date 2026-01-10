# %%
import json
import sys
import re
from langchain_openai import ChatOpenAI
from pathlib import Path

# Asumiendo que tu notebook está en /Users/jpconde/Facultad/tesis/playground
repo_root = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path("/Users/jpconde/Facultad/tesis")
if str(repo_root) not in sys.path:
    sys.path.append(str(repo_root))

from axis_of_interest.schemas import donor_aoi, conflict_aoi
from axis_of_interest.prompts import prompt_generate_plot_schema
from axis_of_interest.utils import render_plot_schema_md

model1 = ChatOpenAI(
    model="gpt-5",
    temperature=0.0,
    model_kwargs={"seed": 42}
)
# model = lms.llm("deepseek-r1-distill-qwen-7b")
#model2 = lms.llm("qwq-32b@q4_k_m")

# %%
axis_of_interest_lista = [donor_aoi, conflict_aoi]

# %%
prompt_generate_plot_schema = prompt_generate_plot_schema.replace(
    "{axis_of_interest}",
    json.dumps([a.model_dump() for a in axis_of_interest_lista], indent=2)
)

result1 = model1.invoke(prompt_generate_plot_schema)
# %%
result2 = model2.respond(
    prompt_generate_plot_schema,
    config={
        "temperature": 0,
        "seed": 42  
    }
)
# %%
print(result1.content)
# %%
print(result2)
# %%
print(render_plot_schema_md(json.loads(result1.content)))
# %%
pat = re.compile(r"```json\s*([\s\S]*?)```", re.IGNORECASE)
m = pat.search(result2.content)
contenido = m.group(1) if m else None
print(render_plot_schema_md(json.loads(contenido)))

# %%
print(type(result2.content))
# %%
