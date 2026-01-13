import React from "react";
import { Icons } from "../components/ui";
import ChatInterface from "../components/chat/ChatInterface";

const Chat: React.FC = () => {
  return (
    <div className="min-h-screen w-full bg-white">
      <div className="w-full px-4 py-8">
        <header className="text-center mb-8">
          <div className="flex justify-center mb-6">
            <Icons.ChatCircleDots className="text-gray-800" />
          </div>
          <h1 className="text-4xl font-light text-gray-900 mb-4">
            Chat Interactivo
          </h1>
          <p className="text-lg text-gray-600">
            Conversá con los modelos de IA de manera continua
          </p>
        </header>
        
        <div className="max-w-7xl mx-auto">
          <div className="bg-gray-50 rounded-lg border border-gray-200 h-[800px] overflow-hidden">
            <ChatInterface />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
