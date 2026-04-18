import { BrowserRouter, Route, Routes } from "react-router-dom";
import Home from "./pages/Home";
import Requerimiento from "./pages/Requerimiento";
import Evaluacion from "./pages/Evaluacion";
import Documentacion from "./pages/Documentacion";
import "./index.css";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/requerimiento" element={<Requerimiento />} />
        <Route path="/evaluacion" element={<Evaluacion />} />
        <Route path="/documentacion" element={<Documentacion />} />
      </Routes>
    </BrowserRouter>
  );
}
