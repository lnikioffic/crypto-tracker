import { useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import MarketOverview from "./pages/MarketOverview";
import { useAuthStore } from "./stores/authStore";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PortfolioPage from "./pages/Portfolio";

function App() {
  const root = window.document.documentElement;
  root.classList.add("dark");

  const fetchUser = useAuthStore((s) => s.fetchUser);

  useEffect(() => {
    fetchUser().catch(() => {});
  }, [fetchUser]);

  return (
    <>
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<MarketOverview />} />
          <Route path="/portfolio" element={<PortfolioPage />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
