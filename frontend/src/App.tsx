import { useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import MarketOverview from "./pages/MarketOverview";
import { useAuthStore } from "./stores/authStore";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PortfolioPage from "./pages/Portfolio";
import PortfolioDetail from "./pages/PortfolioDetail";
import CreatePortfolio from "./pages/CreatePortfolio";
import EditPortfolio from "./pages/EditPortfolio";

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
          <Route path="/portfolios" element={<PortfolioPage />} />
          <Route path="/portfolios/:id" element={<PortfolioDetail />} />
          <Route path="/portfolios/create" element={<CreatePortfolio />} />
          <Route path="/portfolios/:id/edit" element={<EditPortfolio />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
