# Plot Schema Generator - Guía de Inicio

## 🎯 ¿Qué es esto?

Una aplicación web interactiva que te permite crear esquemas narrativos (Plot Schemas) combinando diferentes **Axis of Interest** (AOIs) con distintas estrategias.

## 📋 Requisitos Previos

1. **Python 3.12+** (ya instalado ✅)
2. **Node.js 18+** y npm (para el frontend)

### Instalar Node.js

1. Descarga Node.js desde: https://nodejs.org/
2. Instala la versión LTS
3. Verifica la instalación:
   ```bash
   node --version
   npm --version
   ```

## 🚀 Instalación y Configuración

### 1. Backend (FastAPI)

El backend ya está configurado. Solo necesitas tener las dependencias instaladas:

```bash
# Ya deberías tener esto instalado, pero por si acaso:
pip install fastapi uvicorn pydantic
```

### 2. Frontend (React + TypeScript)

```bash
cd frontend
npm install
```

## ▶️ Iniciar la Aplicación

Necesitas **2 terminales** abiertas:

### Terminal 1: Backend

```bash
# Desde la raíz del proyecto (c:\Users\sofic\Documents\tesis)
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en: http://localhost:8000

### Terminal 2: Frontend

```bash
# Desde la raíz del proyecto
cd frontend
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## 🎮 Cómo Usar

1. Abre tu navegador en http://localhost:5173
2. Ve a **"Schema Generator"** en el menú
3. Selecciona los **Axis of Interest** que quieras combinar (ej: JOURNEY, CONFLICT, TASK)
4. Elige una **estrategia**:
   - **Sequential**: Concatena todos los spans en orden
   - **Round Robin**: Intercala tomando uno de cada AOI
   - **Parallel**: Agrupa por posición
   - **Random**: Orden aleatorio respetando secuencia interna
5. (Opcional) Agrega un nombre y descripción
6. Haz clic en **"Generar Schema"**
7. ¡Verás tu esquema narrativo generado con todos los detalles!

## 📚 Estrategias Explicadas

### Sequential
```
JOURNEY → CONFLICT
Resultado: Out, Back, Struggle, Victory
```

### Round Robin
```
JOURNEY → CONFLICT
Resultado: Out, Struggle, Back, Victory
```

### Parallel
```
JOURNEY → CONFLICT → TASK
Resultado: Out, Struggle, TaskSet, Back, Victory, TaskSolved
```

### Random
```
JOURNEY → CONFLICT → TASK
Resultado posible: TaskSet, Out, Struggle, Back, Victory, TaskSolved
(Varía cada vez, pero siempre respeta el orden interno de cada AOI)
```

## 🔧 API Endpoints

### GET /api/aois
Obtiene todos los Axis of Interest disponibles

### POST /api/generate-schema
Genera un PlotSchema

**Body:**
```json
{
  "aoi_names": ["JOURNEY", "CONFLICT"],
  "strategy": "random",
  "schema_name": "Mi Historia",
  "schema_description": "Una aventura épica"
}
```

## 🎨 Características

- ✅ Interfaz interactiva para seleccionar AOIs
- ✅ 4 estrategias de intercalado diferentes
- ✅ Visualización detallada del schema generado
- ✅ Muestra todos los Plot Spans, Plot Atoms, personajes y objetos
- ✅ Diseño responsive y moderno

## 🐛 Troubleshooting

### El backend no inicia
- Verifica que tengas todas las dependencias: `pip install -r requirements.txt`
- Asegúrate de estar en el entorno virtual correcto

### El frontend no inicia
- Instala Node.js si no lo tienes
- Ejecuta `npm install` en la carpeta `frontend/`
- Si hay errores, prueba borrar `node_modules` y ejecutar `npm install` de nuevo

### Error de CORS
- El backend ya está configurado para aceptar peticiones desde localhost:5173
- Si cambias el puerto del frontend, actualiza el CORS en `app.py`

## 📝 Archivos Importantes

- `app.py` - Backend FastAPI con los endpoints
- `axis_of_interest/schema_generator.py` - Generador de schemas
- `axis_of_interest/schemas.py` - Modelos Pydantic
- `frontend/src/pages/SchemaGenerator.tsx` - Página principal de la UI
- `frontend/src/App.tsx` - Router de React

## 🎉 ¡Listo!

Ahora puedes crear esquemas narrativos complejos de forma interactiva. Experimenta combinando diferentes AOIs y estrategias para ver qué historias puedes crear! 🎭
