import { useEffect, useState } from "react";
import { fetchCryptoList } from "@/stores/cryptoStore";
import type { CryptoData } from "@/models/cryptoData";
import CryptocurrencyCard from "@/components/CryptocurrencyCard";
import { Skeleton } from "@/components/ui/skeleton";

// Skeleton-заглушка для карточки с использованием ui/Skeleton
function CardSkeleton() {
  return (
    <div className="p-4 flex flex-col gap-2 shadow-md min-w-[220px]">
      <div className="flex items-center justify-between">
        <Skeleton className="h-6 w-24" />
        <Skeleton className="h-4 w-10" />
      </div>
      <Skeleton className="h-8 w-32 my-2" />
      <Skeleton className="h-4 w-16" />
    </div>
  );
}

function MarketOverview() {
  const [cryptos, setCryptos] = useState<CryptoData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchCryptoList()
      .then((data) => {
        setCryptos(data);
        setError(null);
      })
      .catch(() => {
        setError("Ошибка загрузки данных");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Обзор рынка</h1>
      {error && <div className="text-red-600 mb-4">{error}</div>}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {loading
          ? Array.from({ length: 8 }).map((_, i) => <CardSkeleton key={i} />)
          : cryptos.map((crypto) => (
              <CryptocurrencyCard key={crypto.id} data={crypto} />
            ))}
      </div>
    </div>
  );
}

export default MarketOverview;
