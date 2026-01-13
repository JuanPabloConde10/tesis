import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Navigation } from "./components";
import Home from "./pages/Home";
import Playground from "./pages/Playground";
import Chat from "./pages/Chat";
import About from "./pages/About";
import "./index.css";

function App() {
  return (
    <Router>
        <div className="min-h-screen w-full bg-white">
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/playground" element={<Playground />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
