import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./index.css";
import Shell from "./Shell.jsx";

const basename = window.location.pathname.startsWith("/jee-dashboard")
  ? "/jee-dashboard"
  : "/";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter basename={basename}>
      <Routes>
        <Route path="/*" element={<Shell />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
