export async function fetchProviders() {
  const res = await fetch("/api/providers");
  if (!res.ok) throw new Error("No se pudo cargar la lista de proveedores.");
  return res.json();
}

import type { ChatPayload } from "../components/ChatForm";

export async function sendChat(payload: ChatPayload) {
  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Error en la consulta.");
  return res.json();
}
