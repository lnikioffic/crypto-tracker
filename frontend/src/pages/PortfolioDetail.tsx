import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { usePortfolioStore } from "@/stores/portfolioStore";
import { ArrowLeft } from "lucide-react";
import { useEffect } from "react";
import { useParams } from "react-router-dom";
import { useNavigate } from "react-router-dom";

function PortfolioDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { portfolio, loading, error, getPortfolio, deletePortfolio } =
    usePortfolioStore();

  const handleDelete = async () => {
    if (id && confirm("Вы уверены что хотите удалить этот портфель?")) {
      await deletePortfolio(parseInt(id));
      navigate("/portfolios");
    }
  };

  useEffect(() => {
    if (id) {
      getPortfolio(parseInt(id));
    }
  }, [id, getPortfolio, navigate]);

  if (loading) {
    return (
      <div className="container mx-auto py-8 space-y-4">
        <Skeleton className="h-10 w-32 mb-6" />
        <Skeleton className="h-32 w-full rounded-lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center py-12 space-y-4">
          <p className="text-destructive">{error}</p>
          <Button onClick={() => navigate(-1)} variant="outline">
            Назад
          </Button>
        </div>
      </div>
    );
  }

  if (!portfolio) {
    return (
      <div className="container mx-auto py-8">
        <div className="text-center py-12">
          <p className="text-muted-foreground">Портфель не найден</p>
        </div>
      </div>
    );
  }
  const isPositive = (price_change_percentage_24h: number | undefined) => {
    if (price_change_percentage_24h) return price_change_percentage_24h >= 0;
  };
  return (
    <div className="container mx-auto py-8 space-y-6">
      <Button
        variant="ghost"
        onClick={() => navigate("/portfolios")}
        className="flex items-center gap-2"
      >
        <ArrowLeft className="h-4 w-4" />
        Назад к списку
      </Button>

      <Card>
        <CardHeader>
          <CardTitle className="text-2xl font-bold">{portfolio.name}</CardTitle>
          <div className="text-lg font-semibold text-primary">
            {formatCurrency(portfolio.total_value)}
          </div>
        </CardHeader>

        <CardContent>
          <div className="space-y-4">
            <h3 className="font-medium text-lg">Активы:</h3>
            <ul className="space-y-3 divide-y">
              {portfolio.coins.map((coin) => (
                <li
                  key={coin.id}
                  className="pt-3 flex justify-between items-center"
                >
                  <div className="flex items-center gap-3">
                    <img
                      src={coin.coin_deatil.image}
                      alt={coin.coin_deatil.name}
                      className="w-6 h-6 rounded-full"
                      onError={(e) => {
                        (e.target as HTMLImageElement).src =
                          "/crypto-placeholder.png";
                      }}
                    />
                    <span className="font-medium">
                      {coin.coin_id.toUpperCase()}
                    </span>
                  </div>
                  <div className="text-right">
                    <div className="font-mono">
                      {formatCryptoAmount(coin.amount)}
                    </div>
                    <div className="text-muted-foreground text-sm">
                      {formatCurrency(coin.total_value)}
                    </div>
                    <div
                      className={`text-sm font-medium ${
                        isPositive(coin.coin_deatil.price_change_percentage_24h)
                          ? "text-green-600"
                          : "text-red-600"
                      }`}
                    >
                      {isPositive(coin.coin_deatil.price_change_percentage_24h)
                        ? "+"
                        : ""}
                      {coin.coin_deatil.price_change_percentage_24h.toFixed(2)}%
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </CardContent>
      </Card>

      <div className="flex gap-4">
        <Button
          variant="outline"
          onClick={() => navigate(`/portfolios/${id}/edit`)}
        >
          Редактировать
        </Button>
        <Button variant="destructive" onClick={handleDelete}>
          Удалить портфель
        </Button>
      </div>
    </div>
  );
}

export default PortfolioDetail;

function formatCurrency(value: number): string {
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

function formatCryptoAmount(amount: number): string {
  return amount.toLocaleString("en-US", {
    maximumFractionDigits: 8,
  });
}
