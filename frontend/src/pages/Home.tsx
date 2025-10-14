import React from "react";
import { Link } from "react-router-dom";
import { Icons } from "../components/ui";

const Home: React.FC = () => {
  return (
    <div className="min-h-screen w-full bg-white py-12">
      <div className="w-full text-center px-4">
        <div className="max-w-6xl mx-auto">
          <header className="text-center mb-16">
            <div className="flex justify-center mb-6">
              <Icons.SparkleFill className="text-gray-800" />
            </div>
            <h1 className="text-5xl font-light text-gray-900 mb-6">
              LLM Playground
            </h1>
            <p className="text-xl text-gray-600 font-normal max-w-2xl mx-auto">
              Experimentá con diferentes modelos de lenguaje desde una interfaz unificada y moderna
            </p>
          </header>
        
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
            <div className="bg-gray-50 rounded-lg p-8 border border-gray-200 hover:border-gray-300 transition-colors">
              <div className="flex justify-center mb-6">
                <Icons.LightningFill className="text-gray-700" />
              </div>
              <h3 className="text-xl font-medium text-gray-900 mb-4">Playground</h3>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Probá diferentes modelos y configuraciones en tiempo real
              </p>
              <Link 
                to="/playground" 
                className="inline-block bg-gray-100 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-800 transition-colors"
              >
                Ir al Playground
              </Link>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-8 border border-gray-200 hover:border-gray-300 transition-colors">
              <div className="flex justify-center mb-6">
                <Icons.ChatCircleDots className="text-gray-700" />
              </div>
              <h3 className="text-xl font-medium text-gray-900 mb-4">Chat</h3>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Conversá con los modelos de manera interactiva
              </p>
              <Link 
                to="/chat" 
                className="inline-block bg-gray-100 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-800 transition-colors"
              >
                Ir al Chat
              </Link>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-8 border border-gray-200 hover:border-gray-300 transition-colors">
              <div className="flex justify-center mb-6">
                <Icons.CheckCircle className="text-gray-700" />
              </div>
              <h3 className="text-xl font-medium text-gray-900 mb-4">Rápido</h3>
              <p className="text-gray-600 mb-6 leading-relaxed">
                Respuestas instantáneas con múltiples proveedores
              </p>
              <Link 
                to="/playground" 
                className="inline-block bg-gray-100 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-800 transition-colors"
              >
                Comenzar
              </Link>
            </div>
          </div>
        
          <div className="bg-gray-50 rounded-lg p-8 border border-gray-200">
            <h2 className="text-2xl font-light text-gray-900 mb-8 text-center">
              ¿Qué podés hacer?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="flex items-start space-x-3">
                <Icons.CheckCircle className="text-gray-700 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Múltiples Proveedores</h3>
                  <p className="text-gray-600">Accedé a OpenAI, Anthropic, Google y Hugging Face desde una sola interfaz</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icons.CheckCircle className="text-gray-700 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Configuración Avanzada</h3>
                  <p className="text-gray-600">Ajustá temperatura, tokens máximos y mensajes de sistema</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icons.CheckCircle className="text-gray-700 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Comparación</h3>
                  <p className="text-gray-600">Probá el mismo prompt con diferentes modelos lado a lado</p>
                </div>
              </div>
              <div className="flex items-start space-x-3">
                <Icons.CheckCircle className="text-gray-700 mt-1" />
                <div>
                  <h3 className="font-medium text-gray-900 mb-2">Historial</h3>
                  <p className="text-gray-600">Guardá y reutilizá tus mejores prompts y configuraciones</p>
                </div>
              </div>
            </div>
          </div>
          
          {/* Link to About */}
          <div className="text-center mt-12">
            <p className="text-gray-600 mb-6">¿Querés saber más sobre este proyecto?</p>
            <Link 
              to="/about" 
              className="inline-flex items-center space-x-2 bg-gray-100 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-800 transition-colors"
            >
              <Icons.Info />
              <span>Conocer Más</span>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
