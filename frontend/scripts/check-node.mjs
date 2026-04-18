import crypto from "node:crypto";

if (typeof crypto.hash !== "function") {
  console.error(
    "Node.js demasiado antiguo para Vite 7. Necesitás 20.19+ o 22.12+.",
    `\nActual: ${process.version}`,
    "\n\nCon nvm, en esta carpeta: nvm use && npm run dev",
    "\n(o: nvm install 22 && nvm use 22)",
  );
  process.exit(1);
}
