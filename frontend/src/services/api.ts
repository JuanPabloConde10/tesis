export async function fetchProviders() {
  const res = await fetch("/api/providers");
  if (!res.ok) throw new Error("No se pudo cargar la lista de proveedores.");
  return res.json();
}

import type { ChatPayload } from "../components/ChatForm";

export async function sendChat(payload: ChatPayload) {
  // Convertir strings a números cuando sea necesario
  const backendPayload = {
    provider: payload.provider,
    prompt: payload.prompt,
    system: payload.system || null,
    temperature: payload.temperature ? parseFloat(payload.temperature) : null,
    max_tokens: payload.max_tokens ? parseInt(payload.max_tokens) : null,
  };

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(backendPayload),
  });
  
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Error ${res.status}: ${res.statusText}`);
  }
  
  return res.json();
}

// Nueva función para chat con formato de mensajes nativo
export async function sendChatWithMessages(payload: {
  provider: string;
  messages: Array<{ role: string; content: string }>;
  temperature?: number | null;
  max_tokens?: number | null;
}) {
  const backendPayload = {
    provider: payload.provider,
    messages: payload.messages,
    temperature: payload.temperature || null,
    max_tokens: payload.max_tokens || null,
  };

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(backendPayload),
  });
  
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || `Error ${res.status}: ${res.statusText}`);
  }
  
  return res.json();
}
