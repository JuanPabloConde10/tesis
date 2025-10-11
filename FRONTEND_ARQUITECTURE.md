Propuesta: migrar la UI a React + Vite + Tailwind (y estructura escalable)

Objetivo
- Reorganizar el repo para separar claramente backend y frontend.
- Usar React + Vite para desarrollo rápido y Hot Module Replacement.
- Usar Tailwind CSS para estilos utilitarios y consistencia.
- Mantener el backend FastAPI responsable de la API y servir la versión estática en producción.

Resumen de cambios y beneficios
- Frontend aislado en su carpeta (frontend/). Facilita CI/CD, testing y despliegues independientes.
- Backend en backend/ o en la raíz (mantener como ahora `app.py`), expone `/api/*` y sirve build estático en producción.
- Proxy del dev server (Vite) a FastAPI evita CORS y permite UX local fluida.

Estructura de carpetas propuesta

tesis/
├─ backend/                     # (opcional: mover archivos actuales aquí)
│  ├─ app.py                    # FastAPI (entrada del servidor)
│  ├─ main.py                   # CLI
│  ├─ config.py
│  ├─ requirements.txt
│  ├─ llm_clients/              # lógica de clientes LLM
│  └─ ...
├─ frontend/                    # nuevo proyecto React + Vite + Tailwind
│  ├─ package.json
│  ├─ vite.config.ts
│  ├─ tailwind.config.cjs
│  ├─ postcss.config.cjs
│  ├─ index.html
│  ├─ src/
│  │  ├─ main.tsx               # entrypoint React
│  │  ├─ App.tsx
│  │  ├─ components/
│  │  │  ├─ ChatForm.tsx
│  │  │  ├─ ProviderSelect.tsx
│  │  │  └─ ...
│  │  ├─ hooks/
│  │  ├─ services/
│  │  │  └─ api.ts              # wrapper para llamadas a /api/chat y /api/providers
│  │  └─ styles.css             # importa Tailwind base
│  └─ public/                   # assets estáticos
├─ web/                         # (actual) puede mantenerse como carpeta temporal o eliminar
│  ├─ index.html
│  └─ static/
├─ .env.example
├─ README.md
└─ FRONTEND_REACT_TAILWIND.md   # este archivo

Notas de migración
- Opción A (recomendado durante la migración): dejar el backend en la raíz y crear `frontend/` paralelo. En producción, ajustar FastAPI para servir `frontend/dist`.
- Opción B: mover todo lo relacionado al backend dentro de `backend/` (más limpio para microservicios), actualizar los imports relativos si es necesario.

Comandos para crear el frontend (Vite + React + TypeScript + Tailwind)

1) Crear proyecto con Vite
```bash
# desde la raíz del repo
cd tesis
npm create vite@latest frontend -- --template react-ts
cd frontend
```

2) Instalar Tailwind y deps recomendadas
```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
# instalar librerías útiles
npm install axios clsx
```

3) Configurar Tailwind (archivo `tailwind.config.cjs`)
- Ajustá content para que lea `src/**/*.{js,ts,jsx,tsx}`

4) Importar Tailwind en `src/styles.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```
En `src/main.tsx` importa `./styles.css`.

5) Agregar scripts útiles en `package.json`
- `dev`: `vite`
- `build`: `vite build`
- `preview`: `vite preview`

6) Configurar proxy para desarrollo (evitar CORS)
- En `vite.config.ts` agrega:
```ts
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://127.0.0.1:8000',
      changeOrigin: true,
      secure: false,
    },
  },
},
```
Así podés llamar `fetch('/api/chat')` desde React en dev y el request se pasará al backend FastAPI local.

Cómo integrar con FastAPI en producción
- Opción 1 (más simple): después de `npm run build`, copiar el contenido `frontend/dist` a `web/static` o `web/dist` y dejar `app.py` como:
  - `app.mount('/static', StaticFiles(directory='web/static'), name='static')`
  - servir `web/index.html` desde `GET /`.
- Opción 2 (más limpio): modificar `app.py` para montar `StaticFiles(directory='frontend/dist')` y leer `frontend/dist/index.html` en `serve_index()`.

Ejemplo de script para deploy local (desde la raíz):
```bash
# dentro de frontend
npm run build
# copia build a backend static folder (ajusta según tu configuración)
rm -rf web/static
mkdir -p web/static
cp -R frontend/dist/* web/static/
# luego arrancar uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
```

Consideraciones sobre rutas y base path
- Si vas a servir la app bajo `/` y la API bajo `/api`, evita usar rutas clash. Mantener `/api/*` reservado al backend es buena práctica.
- Si el frontend usa rutas con react-router (history mode), hace falta que el servidor devuelva `index.html` para rutas no encontradas (fallback). FastAPI sirve `index.html` en `/` pero conviene añadir una ruta catch-all que devuelva `index.html` para rutas del frontend en producción.

Estructura del código frontend propuesta (más detalle)

src/
├─ main.tsx             # inicializa React, ReactDOM.render
├─ App.tsx              # layout principal, rutas
├─ pages/
│  ├─ Home.tsx          # UI principal (chat)
│  └─ About.tsx
├─ components/
│  ├─ ChatForm.tsx
│  ├─ ResponseList.tsx
│  └─ ProviderSelect.tsx
├─ services/
│  └─ api.ts            # funciones: getProviders(), sendChat()
├─ hooks/
│  └─ useStreaming.ts   # si implementas streaming en el futuro
├─ styles.css
└─ types/               # tipos TypeScript para payloads, respuestas

`services/api.ts` (contrato mínimo)
- getProviders(): Promise<string[]>
- sendChat(payload): Promise<{response: string}>
- (opcional) streamChat(...) => async generator (si implementas SSE / websocket luego)

Testing y calidad
- Añadir tests unitarios y de integración del frontend con Jest + React Testing Library.
- E2E: Playwright o Cypress para flujos (abrir app, enviar prompt, ver respuesta).
- Linting/format: ESLint + Prettier + una configuración shared.

CI / CD sugerido
- Pipeline en GitHub Actions:
  - frontend: install, lint, build, test
  - backend: install deps, lint, run tests
  - artefact: subir `frontend/dist` como artefacto o desplegar en hosting estático (Netlify, Vercel) y backend en Heroku/GCP/AWS.

Mejoras futuras
- Añadir autenticación y límites de uso por usuario.
- Convertir backend en microservicio y desplegar frontend en CDN para latencia baja.
- Implementar streaming en la API (SSE o WebSockets) para experiencia en tiempo real.

Siguientes pasos que puedo tomar por vos
- Crear el scaffold inicial de `frontend/` (ejecutar `npm create vite@latest ...`) y commitearlo.
- Añadir el proxy en `vite.config.ts` y un `services/api.ts` de ejemplo que apunte a `/api`.
- Ajustar `app.py` para que sirva `frontend/dist` en producción (patch simple).

Decime qué preferís: genero el scaffold del frontend aquí mismo (instalando dependencias y creando archivos iniciales) o te dejo los pasos para que lo hagas localmente. Si querés que lo cree ahora, lo hago y luego ejecuto una build de prueba.
