import React from "react";
import { Link } from "react-router-dom";
import { Icons } from "../components/ui";

const About: React.FC = () => {
  return (
    <div className="min-h-screen w-full bg-white py-12">
      <div className="w-full px-4">
        <div className="max-w-4xl mx-auto">
          <header className="text-center mb-16">
            <div className="flex justify-center mb-6">
              <Icons.Info className="text-gray-800" />
            </div>
            <h1 className="text-4xl font-light text-gray-900 mb-4">
              Tesis: Cuentos Cortos y Creatividad con LLMs
            </h1>
            <p className="text-lg text-gray-600 max-w-4xl mx-auto">
              El objetivo de esta tesis es crear cuentos cortos utilizando modelos de lenguaje (LLMs) y compararlos para analizar su creatividad, valencia y arousal, así como su semejanza con la narrativa humana. Buscamos integrar múltiples modelos de IA para explorar cómo cada uno aborda la generación de historias y qué tan creativos pueden ser.
              <br /><br />
              Para lograr esto, empleamos un formalismo lógico llamado <b>Axis of Interest</b>, que nos permite definir y manipular ejes narrativos para crear y comparar <i>plot schemas</i> divertidos e interesantes. Así, podemos generar nuevas historias y analizar cómo los LLMs responden a diferentes desafíos creativos.
              <br /><br />
              El proyecto también busca comparar los resultados entre modelos y con narrativas humanas, evaluando la capacidad de los LLMs para producir relatos originales y emocionalmente ricos.
            </p>
          </header>

          {/* Propósito Principal */}
          <div className="bg-gray-50 rounded-lg border border-gray-200 p-8 mb-8">
            <h2 className="text-2xl font-light text-gray-900 mb-6">
              ¿Cuál es el problema que resuelve?
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Antes:</h3>
                <ul className="list-disc list-inside text-gray-600 space-y-2">
                  <li>Múltiples plataformas y APIs para cada modelo</li>
                  <li>Curva de aprendizaje alta para nuevos usuarios</li>
                  <li>Dificultad para comparar modelos de forma rápida</li>
                  <li>Falta de una interfaz intuitiva para experimentar</li>
                </ul>
              </div>
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Ahora (con LLM Playground):</h3>
                <ul className="list-disc list-inside text-gray-600 space-y-2">
                  <li>Interfaz unificada para OpenAI, Anthropic, Google, etc.</li>
                  <li>Fácil configuración y envío de prompts</li>
                  <li>Comparación visual de respuestas</li>
                  <li>Ideal para desarrolladores y entusiastas de IA</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Características */}
          <div className="bg-gray-50 rounded-lg border border-gray-200 p-8 mb-8">
            <h2 className="text-2xl font-light text-gray-900 mb-8 text-center">
              Características Principales
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <Icons.CheckCircle className="text-gray-700" />
                </div>
                <h3 className="font-medium text-gray-900 mb-2">Múltiples LLMs</h3>
                <p className="text-gray-600 text-sm">Accede a los principales proveedores</p>
              </div>
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <Icons.CheckCircle className="text-gray-700" />
                </div>
                <h3 className="font-medium text-gray-900 mb-2">Configuración Flexible</h3>
                <p className="text-gray-600 text-sm">Ajusta temperatura, tokens, etc.</p>
              </div>
              <div className="text-center">
                <div className="flex justify-center mb-4">
                  <Icons.CheckCircle className="text-gray-700" />
                </div>
                <h3 className="font-medium text-gray-900 mb-2">Comparación Sencilla</h3>
                <p className="text-gray-600 text-sm">Compara respuestas lado a lado</p>
              </div>
            </div>
          </div>

          {/* Tecnologías */}
          <div className="bg-gray-50 rounded-lg border border-gray-200 p-8 mb-8">
            <h2 className="text-2xl font-light text-gray-900 mb-6">
              Tecnologías Utilizadas
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Frontend:</h3>
                <ul className="list-disc list-inside text-gray-600 space-y-1">
                  <li>React + TypeScript</li>
                  <li>Tailwind CSS</li>
                  <li>React Router DOM</li>
                  <li>Componentes UI modernos</li>
                </ul>
              </div>
              <div>
                <h3 className="font-medium text-gray-900 mb-3">Backend:</h3>
                <ul className="list-disc list-inside text-gray-600 space-y-1">
                  <li>Python + FastAPI</li>
                  <li>Pydantic para validación</li>
                  <li>Integración con APIs de LLMs</li>
                  <li>Manejo de errores robusto</li>
                </ul>
              </div>
            </div>
          </div>

          {/* Botones de acción */}
          <div className="text-center">
            <div className="flex justify-center gap-4">
              <Link
                to="/chat"
                className="inline-flex items-center space-x-2 bg-gray-100 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-800 transition-colors"
              >
                <Icons.ChatCircleDots />
                <span>Ir al Chat</span>
              </Link>
              <Link
                to="/playground"
                className="inline-flex items-center space-x-2 bg-gray-100 text-white px-6 py-3 rounded-md font-medium hover:bg-gray-800 transition-colors"
              >
                <Icons.LightningFill />
                <span>Ir al Playground</span>
              </Link>
              <Link
                to="/"
                className="inline-flex items-center space-x-2 bg-gray-100 text-gray-800 px-6 py-3 rounded-md font-medium hover:bg-gray-200 transition-colors"
              >
                <Icons.House />
                <span>Volver al Inicio</span>
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;
