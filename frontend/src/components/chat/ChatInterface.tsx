import React, { useState, useEffect, useRef } from "react";
import { Button, Label, TextArea, Input } from "./../ui";
import ProviderSelect from "../provider-select/ProviderSelect";
import { fetchProviders, sendChatWithMessages } from "../../services/api";

interface Message {
  id: string;
  role: "user" | "assistant" | "system";
  content: string;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [providers, setProviders] = useState<string[]>([]);
  const [, setDefaultProvider] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // Configuración del chat
  const [provider, setProvider] = useState<string>("");
  const [system, setSystem] = useState<string>("");
  const [temperature, setTemperature] = useState<string>("");
  const [max_tokens, setMaxTokens] = useState<string>("");
  
  // Mensajes del chat
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentMessage, setCurrentMessage] = useState<string>("");
  const [showContext, setShowContext] = useState<boolean>(false);
  const [lastSystemPrompt, setLastSystemPrompt] = useState<string>("");
  
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchProviders()
      .then(data => {
        setProviders(data.providers);
        setDefaultProvider(data.default);
        if (data.default && !provider) {
          setProvider(data.default);
        }
      })
      .catch(err => {
        setProviders([]);
        setDefaultProvider("");
        setError(err.message);
      });
  }, [provider]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Detectar cambios en el mensaje de sistema
  useEffect(() => {
    if (system !== lastSystemPrompt && messages.length > 0) {
      // Si cambió el mensaje de sistema y hay mensajes, mostrar advertencia
      console.log("System prompt changed, previous conversation context may be affected");
      setLastSystemPrompt(system);
    } else if (system !== lastSystemPrompt) {
      setLastSystemPrompt(system);
    }
  }, [system, lastSystemPrompt, messages.length]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const buildChatMessages = (newUserMessage: string) => {
    const MAX_HISTORY = 20; // Limitar historial para evitar exceder tokens
    
    // Filtrar mensajes de sistema del historial (solo mantener user/assistant)
    const conversationMessages = messages.filter(m => m.role !== "system");
    
    // Solo incluir system message si:
    // 1. Hay un system prompt definido
    // 2. Es el primer mensaje de la conversación
    const shouldIncludeSystem = system.trim() && conversationMessages.length === 0;
    
    const chatMessages = [
      // Mensaje de sistema (solo al inicio)
      ...(shouldIncludeSystem ? [{ role: "system", content: system.trim() }] : []),
      
      // Historial de conversación (solo user/assistant)
      ...conversationMessages
        .slice(-MAX_HISTORY)
        .map(m => ({
          role: m.role,
          content: m.content
        })),
      
      // Nuevo mensaje del usuario
      { role: "user", content: newUserMessage },
    ];

    return chatMessages;
  };

  const handleSendMessage = async () => {
    if (!currentMessage.trim() || !provider || loading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: currentMessage.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage("");
    setLoading(true);
    setError(null);

    try {
      // Construir mensajes en formato nativo
      const chatMessages = buildChatMessages(userMessage.content);
      
      // Preparar el payload para el chat con formato correcto
      const chatPayload = {
        provider,
        messages: chatMessages,
        temperature: temperature ? parseFloat(temperature) : null,
        max_tokens: max_tokens ? parseInt(max_tokens) : null,
      };

      const response = await sendChatWithMessages(chatPayload);
      
      // Manejar diferentes formatos de respuesta del backend
      let responseContent = "Sin respuesta";
      if (typeof response === "string") {
        responseContent = response;
      } else if (response && typeof response === "object") {
        responseContent = response.response || response.message || response.content || JSON.stringify(response);
      }
      
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: responseContent,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: err instanceof Error ? err.message : "Error desconocido",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Configuración del chat */}
      <div className="border-b border-gray-200 p-4 bg-gray-50">
        {/* Indicador de memoria */}
        {messages.length > 0 && (
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">
                Chat con memoria ({messages.filter(m => m.role !== "system").length} mensajes)
              </span>
              <span className="text-xs text-gray-500">
                (Enviando últimos {Math.min(messages.filter(m => m.role !== "system").length, 20)})
              </span>
              {system.trim() && (
                <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">
                  System: {system.length > 30 ? system.substring(0, 30) + "..." : system}
                </span>
              )}
            </div>
            <Button
              onClick={() => setShowContext(!showContext)}
              variant="outlined"
              size="sm"
              className="bg-white text-gray-700 hover:bg-gray-100"
            >
              {showContext ? "Ocultar contexto" : "Ver contexto"}
            </Button>
          </div>
        )}
        
        <div className="flex gap-4 items-end">
          <div className="flex flex-col gap-1 w-[25%]">
            <ProviderSelect providers={providers} value={provider} onChange={setProvider} />
          </div>
          
          <div className="flex flex-col gap-1 w-[50%]">
            <Label htmlFor="system">Mensaje de sistema (opcional)</Label>
            <TextArea 
              id="system" 
              name="system" 
              rows={1} 
              value={system} 
              onChange={e => setSystem(e.target.value)} 
              placeholder="Actuá como..." 
            />
          </div>
          
          <div className="flex gap-4 w-[25%]">
            <div className="flex flex-col gap-1 w-[50%]">
              <Label htmlFor="temperature">Temperatura</Label>
              <Input 
                id="temperature" 
                name="temperature" 
                type="number" 
                step="0.1" 
                min="0" 
                max="2" 
                value={temperature} 
                onChange={e => setTemperature(e.target.value)} 
                placeholder="0.7" 
                className="w-full" 
              />
            </div>
            <div className="flex flex-col gap-1 w-[50%]">
              <Label htmlFor="max_tokens">Max tokens</Label>
              <Input 
                id="max_tokens" 
                name="max_tokens" 
                type="number" 
                min="1" 
                value={max_tokens} 
                onChange={e => setMaxTokens(e.target.value)} 
                placeholder="256" 
                className="w-full" 
              />
            </div>
          </div>
        </div>
        
        {error && (
          <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-center">
              <span className="text-red-500 mr-2">⚠️</span>
              <span className="text-red-700 font-medium">{error}</span>
            </div>
          </div>
        )}
        
        {/* Mostrar contexto si está habilitado */}
        {showContext && messages.length > 0 && (
          <div className="mt-4 p-3 bg-white border border-gray-200 rounded-lg">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Mensajes que se envían al LLM (formato nativo):</h4>
            <div className="text-xs text-gray-600 bg-gray-50 p-2 rounded border max-h-32 overflow-y-auto">
              <pre className="whitespace-pre-wrap">
{JSON.stringify(buildChatMessages(currentMessage || "Nuevo mensaje"), null, 2)}
              </pre>
            </div>
            <p className="text-xs text-gray-500 mt-2">
              Historial limitado a últimos 20 mensajes para evitar exceder límites de tokens
            </p>
          </div>
        )}
      </div>

      {/* Área de mensajes */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg mb-2">¡Iniciá la conversación!</p>
            <p className="text-sm">Escribí un mensaje abajo para comenzar a chatear con el LLM.</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[70%] rounded-lg p-3 ${
                  message.role === "user"
                    ? "bg-gray-900 text-white"
                    : "bg-gray-100 text-gray-900"
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className={`text-xs mt-1 ${
                  message.role === "user" ? "text-gray-300" : "text-gray-500"
                }`}>
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))
        )}
        
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-900 rounded-lg p-3 max-w-[70%]">
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-600 mr-2"></div>
                <span>Escribiendo...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input de mensaje */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex gap-2">
          <div className="flex-1">
            <TextArea
              value={currentMessage}
              onChange={e => setCurrentMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Escribí tu mensaje..."
              rows={2}
              className="resize-none"
            />
          </div>
          <div className="flex flex-col gap-2">
            <Button
              onClick={handleSendMessage}
              disabled={loading || !currentMessage.trim() || !provider}
              variant={currentMessage.trim() && provider ? "primary" : "outlined"}
              size="lg"
              className={
                currentMessage.trim() && provider && !loading
                  ? "bg-gray-900 text-grey-400 hover:bg-gray-800"
                  : "bg-gray-100 text-gray-400"
              }
            >
              Enviar
            </Button>
            <Button
              onClick={clearChat}
              variant="secondary"
              size="sm"
              className="bg-gray-100 text-gray-700 hover:bg-gray-200"
            >
              Limpiar
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
