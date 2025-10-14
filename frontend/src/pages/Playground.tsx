import React, { useEffect, useState } from "react";
import { ChatForm } from "../components";
import type { ChatPayload } from "../components";
import { fetchProviders, sendChat } from "../services/api";
import { Icons } from "../components/ui";

const Playground: React.FC = () => {
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
    <div className="min-h-screen w-full bg-white py-8">
      <div className="w-full px-4">
        <header className="text-center mb-12">
          <div className="flex justify-center mb-6">
            <Icons.LightningFill className="text-gray-800" />
          </div>
          <h1 className="text-4xl font-light text-gray-900 mb-4">
            LLM Playground
          </h1>
          <p className="text-lg text-gray-600 font-normal">
            Experimentá con diferentes modelos y configuraciones
          </p>
        </header>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Formulario */}
          <div className="bg-gray-50 rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-medium text-gray-900 mb-6">
              Configuración del Modelo
            </h2>
            {error && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center">
                  <Icons.WarningCircle className="text-red-500 mr-2" />
                  <span className="text-red-700 font-medium">{error}</span>
                </div>
              </div>
            )}
            <ChatForm
              providers={providers}
              defaultProvider={defaultProvider}
              onSubmit={handleSubmit}
              loading={loading}
            />
          </div>

          {/* Respuesta */}
          <div className="bg-gray-50 rounded-lg border border-gray-200 p-6">
            <h2 className="text-xl font-medium text-gray-900 mb-6">
              Respuesta del Modelo
            </h2>
            <div className="bg-white rounded-lg p-6 border border-gray-200 min-h-[400px]">
              <div className="flex items-center justify-between mb-4">
                <span className="text-sm font-medium text-gray-700 bg-gray-100 px-3 py-1 rounded-full">
                  {loading ? "Procesando..." : "Resultado"}
                </span>
                {response && (
                  <span className="text-xs text-gray-500">
                    {response.length} caracteres
                  </span>
                )}
              </div>
              <pre className="whitespace-pre-wrap text-gray-800 font-mono text-sm leading-relaxed">
                {loading ? (
                  <div className="flex items-center justify-center h-32">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-600 mr-2"></div>
                    <span className="text-gray-600">Procesando...</span>
                  </div>
                ) : response || ""}
              </pre>
            </div>
          </div>
        </div>

        {/* Información adicional */}
        <div className="mt-12 bg-gray-50 rounded-lg border border-gray-200 p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-6 flex items-center">
            <Icons.Info className="mr-2" />
            Consejos para el Playground
          </h3>
          <div className="grid md:grid-cols-2 gap-6 text-sm text-gray-600">
            <div>
              <strong className="text-gray-900">Temperatura:</strong> Valores bajos (0.1-0.3) para respuestas más determinísticas, valores altos (0.7-1.0) para más creatividad.
            </div>
            <div>
              <strong className="text-gray-900">Tokens máximos:</strong> Controla la longitud de la respuesta. Valores típicos: 256-1024.
            </div>
            <div>
              <strong className="text-gray-900">Mensaje de sistema:</strong> Define el comportamiento del modelo. Ej: "Eres un asistente útil y conciso".
            </div>
            <div>
              <strong className="text-gray-900">Proveedores:</strong> Cada modelo tiene sus fortalezas. Experimentá con diferentes opciones.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Playground;
