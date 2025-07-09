import { useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import MarketOverview from "./pages/MarketOverview";
import { useAuthStore } from "./stores/authStore";

function App() {
  const root = window.document.documentElement;
  root.classList.add("dark");

  const accessToken = useAuthStore((s) => s.accessToken);
  const fetchUser = useAuthStore((s) => s.fetchUser);

  useEffect(() => {
    if (accessToken) {
      fetchUser();
    }
  }, [accessToken, fetchUser]);
  
  return (
    <>
      <Header />
      <MarketOverview />
    </>
  );
}

export default App;
