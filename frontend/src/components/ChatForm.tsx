import React, { useState } from "react";
import ProviderSelect from "./ProviderSelect";

export interface ChatPayload {
  provider: string;
  system: string;
  prompt: string;
  temperature: string;
  maxTokens: string;
}

interface ChatFormProps {
  providers: string[];
  defaultProvider: string;
  onSubmit: (payload: ChatPayload) => Promise<void>;
  loading: boolean;
  error: string | null;
}

const ChatForm: React.FC<ChatFormProps> = ({ providers, defaultProvider, onSubmit, loading, error }) => {
  const [provider, setProvider] = useState<string>(defaultProvider);
  const [system, setSystem] = useState<string>("");
  const [prompt, setPrompt] = useState<string>("");
  const [temperature, setTemperature] = useState<string>("");
  const [maxTokens, setMaxTokens] = useState<string>("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onSubmit({ provider, system, prompt, temperature, maxTokens });
  };

  const handleReset = () => {
    setProvider(defaultProvider);
    setSystem("");
    setPrompt("");
    setTemperature("");
    setMaxTokens("");
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow flex flex-col gap-4">
      <ProviderSelect providers={providers} value={provider} onChange={setProvider} />
      <div className="flex flex-col gap-1">
        <label htmlFor="system" className="font-medium">Mensaje de sistema (opcional)</label>
        <textarea id="system" name="system" rows={2} value={system} onChange={e => setSystem(e.target.value)} placeholder="Actuá como..." className="border rounded px-2 py-1" />
      </div>
      <div className="flex flex-col gap-1">
        <label htmlFor="prompt" className="font-medium">Prompt</label>
        <textarea id="prompt" name="prompt" rows={5} value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Escribí tu consulta..." required className="border rounded px-2 py-1" />
      </div>
      <div className="flex gap-4">
        <div className="flex flex-col gap-1">
          <label htmlFor="temperature" className="font-medium">Temperatura</label>
          <input id="temperature" name="temperature" type="number" step="0.1" min="0" max="2" value={temperature} onChange={e => setTemperature(e.target.value)} placeholder="ej. 0.7" className="border rounded px-2 py-1" />
        </div>
        <div className="flex flex-col gap-1">
          <label htmlFor="maxTokens" className="font-medium">Max tokens</label>
          <input id="maxTokens" name="maxTokens" type="number" min="1" value={maxTokens} onChange={e => setMaxTokens(e.target.value)} placeholder="ej. 256" className="border rounded px-2 py-1" />
        </div>
      </div>
      <div className="flex gap-2">
        <button type="submit" disabled={loading} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
          {loading ? "Enviando..." : "Enviar"}
        </button>
        <button type="button" onClick={handleReset} className="bg-gray-300 text-gray-800 px-4 py-2 rounded hover:bg-gray-400 transition">
          Limpiar
        </button>
      </div>
      {error && <div className="text-red-600 font-semibold">{error}</div>}
    </form>
  );
};

export default ChatForm;
