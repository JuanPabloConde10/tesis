import React, { useEffect, useState } from "react";
import { ChatForm } from "./components";
import type { ChatPayload } from "./components";
import { fetchProviders, sendChat } from "./services/api";

import "./index.css";

function App() {
  const [providers, setProviders] = useState<string[]>([]);
  const [defaultProvider, setDefaultProvider] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [response, setResponse] = useState<string>("");

  useEffect(() => {
    fetchProviders()
      .then(data => {
        setProviders(data.providers);
        setDefaultProvider(data.default);
      })
      .catch(err => {
        setProviders([]);
        setDefaultProvider("");
        setError(err.message);
      });
  }, []);

  const handleSubmit = async (payload: ChatPayload) => {
    setLoading(true);
    setError(null);
    setResponse("");
    try {
      const res = await sendChat(payload);
      setResponse(res.response || "Sin respuesta");
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("Error desconocido");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
  <div className="min-h-screen fixed inset-0 flex items-center justify-center py-8 bg-gradient-to-br from-purple-100 via-yellow-50 to-gray-100">
      <div className="w-full max-w-lg mx-auto bg-white rounded-3xl shadow-2xl p-10 flex flex-col gap-10 border-2 border-purple-300">
        <header className="text-center mb-2">
          <h1 className="text-5xl font-extrabold text-purple-700 mb-3 drop-shadow-lg">LLM Playground</h1>
          <p className="text-xl text-gray-600 font-medium">Probá distintos modelos desde una interfaz unificada.</p>
        </header>
        <div className="flex flex-col gap-6">
          <ChatForm
            providers={providers}
            defaultProvider={defaultProvider}
            onSubmit={handleSubmit}
            loading={loading}
            error={error}
          />
          <section className="bg-yellow-50 rounded-xl shadow-inner p-6 border border-yellow-300 flex flex-col items-start">
            <h2 className="font-bold mb-2 text-yellow-700 text-lg">Respuesta</h2>
            <pre className="whitespace-pre-wrap text-gray-800 min-h-[80px] w-full font-mono text-base">{response || ""}</pre>
          </section>
        </div>
      </div>
    </div>
  );
}

export default App;
