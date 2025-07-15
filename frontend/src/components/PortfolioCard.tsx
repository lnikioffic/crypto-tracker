import type { Portfolio } from "@/models/portfolio";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Link } from "react-router-dom";

const formatCurrency = (value: number) =>
  value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });

const formatCryptoAmount = (amount: number) =>
  amount.toLocaleString("en-US", { maximumFractionDigits: 8 });

function PortfolioCard({ portfolio }: { portfolio: Portfolio }) {
  return (
    <Link to={`/portfolios/${portfolio.id}`} className="block mb-4">
      <Card>
        <CardHeader>
          <CardTitle className="text-4xl font-bold">{portfolio.name}</CardTitle>
          <div className="text-lg font-semibold">
            {formatCurrency(portfolio.total_value)}
          </div>
        </CardHeader>

        <CardContent>
          <div className="space-y-2">
            {portfolio.coins.map((coin) => (
              <li key={coin.id} className="flex items-center">
                <span className="font-medium text-base flex-1">
                  {coin.coin_id.toUpperCase()}
                </span>
                <span className="text-muted-foreground font-mono">
                  {formatCryptoAmount(coin.amount)}
                </span>
              </li>
            ))}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}

export default PortfolioCard;
