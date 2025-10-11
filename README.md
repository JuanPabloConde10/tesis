## Entorno para interactuar con múltiples LLMs

Este proyecto provee una estructura mínima en Python para conectarse rápidamente a distintos proveedores de modelos de lenguaje (OpenAI, Anthropic, Google Gemini y Hugging Face).

- Python 3.10 o superior<br>
- Gestión de dependencias con `venv` + `pip` (se puede adaptar a Poetry/uv si preferís)
- Configuración de variables por archivo `.env`

### 1. Crear entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar credenciales

1. Copiá el archivo de ejemplo:
   ```bash
   cp .env.example .env
   ```
2. Completá los valores con tus claves reales. Cada proveedor requiere su propia API key; podés completar solo las que vayas a usar.
3. Ajustá si querés los modelos por defecto (`OPENAI_MODEL`, `ANTHROPIC_MODEL`, etc.) y el proveedor principal (`LLM_PROVIDER`).

> Nota: el proyecto usa `python-dotenv`, por lo que cualquier script que importe `config.py` cargará automáticamente el `.env`.

### 4. Ejecutar prompts

```bash
python main.py "Explicá el algoritmo A*" --provider openai
```

Parámetros útiles:

- `--provider`: `openai`, `anthropic`, `google`, `huggingface`. Si se omite se usa `LLM_PROVIDER`.
- `--system`: mensaje de sistema opcional.
- `--stream`: activa streaming si el cliente lo soporta.
- `--temperature` y `--max-tokens`: afinan la generación cuando la API lo permite.

### 5. Probar el frontend web

```bash
uvicorn app:app --reload
```

Abrí <http://localhost:8000> para acceder a una interfaz web simple donde podés:

- Elegir el proveedor (se usa por defecto el definido en `LLM_PROVIDER`).
- Ajustar mensaje de sistema, temperatura y límite de tokens.
- Ver la respuesta en formato texto.

El backend reutiliza la fábrica de clientes, por lo que respeta las mismas credenciales y modelos configurados en `.env`.

### 6. Extender el entorno

- Agregá nuevos proveedores creando un módulo en `llm_clients/` que implemente la interfaz `LLMClient`.
- Centralizá lógica transversal (logging, manejo de errores, cache) en nuevos módulos dentro del paquete o crea servicios separados.
- Para pruebas podés mockear cada cliente dado que exponen métodos `generate` y `stream`.

### Scripts o integraciones futuras

Podés construir capas superiores (servicios web, pipelines, notebooks) reutilizando `build_client`. Al mantener todo abstraído por la clase base vas a poder intercambiar modelos sin tocar el resto del código.
