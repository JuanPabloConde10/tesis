import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.tsx';

if (import.meta.env.DEV) {
  console.info(
    '[frontend] UI “Taller de cuentos” · rutas: /, /requerimiento, /evaluacion, /documentacion. Si ves Chat/Playground, cerrá otras pestañas o otra carpeta del proyecto.',
  );
}

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
