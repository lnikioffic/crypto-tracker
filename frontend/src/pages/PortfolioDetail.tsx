import { usePortfolioStore } from "@/stores/portfolioStore";
import { useEffect } from "react";
import { useParams } from "react-router-dom";

function PortfolioDetail() {
  const { id } = useParams<{ id: string }>();
  const { portfolio, loading, error, fetchPortfolioById } = usePortfolioStore();

  useEffect(() => {
    if (id) {
      fetchPortfolioById(parseInt(id));
    }
  }, [id, fetchPortfolioById]);
}

export default PortfolioDetail;
