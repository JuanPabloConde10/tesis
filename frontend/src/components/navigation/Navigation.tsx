import React from "react";
import { Link, useLocation } from "react-router-dom";
import { Icons } from "./../ui";

const Navigation: React.FC = () => {
  const location = useLocation();

  const navItems = [
    { path: "/", label: "Home", icon: Icons.House },
    { path: "/playground", label: "Playground", icon: Icons.LightningFill },
    { path: "/chat", label: "Chat", icon: Icons.ChatCircleDots },
    { path: "/about", label: "Sobre el Proyecto", icon: Icons.Info },
  ];

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="w-full px-6">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link 
            to="/" 
            className="flex items-center space-x-3 text-lg font-medium text-gray-900 hover:text-gray-700 transition-colors"
          >
            <Icons.SparkleFill className="text-gray-800" />
            <span>LLM Playground</span>
          </Link>

          {/* Navigation Links */}
          <div className="flex space-x-1">
            {navItems.map((item) => {
              const isActive = location.pathname === item.path;
              const IconComponent = item.icon;
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-md font-medium transition-all duration-200 ${
                    isActive
                      ? "bg-gray-100 text-gray-900"
                      : "text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                  }`}
                >
                  <IconComponent />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
