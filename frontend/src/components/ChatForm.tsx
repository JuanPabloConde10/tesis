import React, { useState, useEffect } from "react";
import ProviderSelect from "./ProviderSelect";
import { Button, Label, TextArea, Input } from "./ui";

export interface ChatPayload {
  provider: string;
  system: string;
  prompt: string;
  temperature: string;
  max_tokens: string;
}

interface ChatFormProps {
  providers: string[];
  defaultProvider: string;
  onSubmit: (payload: ChatPayload) => Promise<void>;
  loading: boolean;
}

const ChatForm: React.FC<ChatFormProps> = ({ providers, defaultProvider, onSubmit, loading }) => {
  const [provider, setProvider] = useState<string>("");
  const [system, setSystem] = useState<string>("");
  const [prompt, setPrompt] = useState<string>("");
  const [temperature, setTemperature] = useState<string>("");
  const [max_tokens, setMaxTokens] = useState<string>("");

  useEffect(() => {
    if (defaultProvider && !provider) {
      setProvider(defaultProvider);
    }
  }, [defaultProvider, provider]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!provider || !prompt.trim()) {
      return;
    }
    await onSubmit({
      provider,
      prompt,
      system,
      temperature,
      max_tokens,
    });
  };

  const handleReset = () => {
    setProvider(defaultProvider || "");
    setSystem("");
    setPrompt("");
    setTemperature("");
    setMaxTokens("");
  };

  const canSend = provider && prompt.trim() && !loading;

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow flex flex-col gap-4">
      <ProviderSelect providers={providers} value={provider} onChange={setProvider} />
      
      <div className="flex gap-4">
        <div className="flex flex-col gap-1 w-[80%]">
          <Label htmlFor="system">Mensaje de sistema (opcional)</Label>
          <TextArea id="system" name="system" rows={2} value={system} onChange={e => setSystem(e.target.value)} placeholder="Actuá como..." />
        </div>
        <div className="flex gap-6 w-[20%]">
          <div className="flex flex-col gap-1 w-[50%]">
            <Label htmlFor="temperature">Temperatura</Label>
            <Input id="temperature" name="temperature" type="number" step="0.1" min="0" max="2" value={temperature} onChange={e => setTemperature(e.target.value)} placeholder="ej. 0.7" className="w-full" />
          </div>
          <div className="flex flex-col gap-1 w-[50%]">
            <Label htmlFor="max_tokens">Max tokens</Label>
            <Input id="max_tokens" name="max_tokens" type="number" min="1" value={max_tokens} onChange={e => setMaxTokens(e.target.value)} placeholder="ej. 256" className="w-full" />
          </div>
        </div>
      </div>
      
      <div className="flex flex-col gap-1">
        <Label htmlFor="prompt">Prompt</Label>
        <TextArea id="prompt" name="prompt" rows={5} value={prompt} onChange={e => setPrompt(e.target.value)} placeholder="Escribí tu consulta..." required />
      </div>
      <div className="flex gap-2 justify-end">
        <Button
          type="submit"
          disabled={loading || !canSend}
          variant={canSend && !loading ? "primary" : "outlined"}
          size="lg"
          isLoading={loading}
          className={
            canSend && !loading 
              ? "bg-gray-100 text-gray-900"
              : "bg-gray-100 text-gray-300 hover:bg-gray-800"
          }
        >
          {loading ? "Procesando..." : "Enviar"}
        </Button>
        <Button 
          type="button" 
          onClick={handleReset} 
          variant="secondary"
          size="lg"
          className="bg-gray-100 text-gray-700 hover:bg-gray-200"
        >
          Limpiar
        </Button>
      </div>
      
      
    </form>
  );
};

export default ChatForm;
