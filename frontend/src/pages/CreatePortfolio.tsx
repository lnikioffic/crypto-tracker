import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { CryptoData } from "@/models/cryptoData";
import type { CoinCreate } from "@/models/portfolio";
import { useAuthStore } from "@/stores/authStore";
import { fetchCryptoList } from "@/stores/cryptoStore";
import { usePortfolioStore } from "@/stores/portfolioStore";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const EmptyState = () => {
  return (
    <div className="text-center py-12 space-y-4">
      <p className="text-muted-foreground">
        Авторизуйтесь для создания портфеля
      </p>
    </div>
  );
};

function CreatePortfolio() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [cryptoList, setCryptoList] = useState<CryptoData[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCoin, setSelectedCoin] = useState<CryptoData | null>(null);
  const [amount, setAmount] = useState("");
  const [coins, setCoins] = useState<CoinCreate[]>([]);
  const [loading, setLoading] = useState(false);
  const { createPortfolio } = usePortfolioStore();
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = !!user;

  // Загрузка списка криптовалют
  useEffect(() => {
    async function loadCryptoList() {
      try {
        const data = await fetchCryptoList();
        setCryptoList(data);
      } catch (error) {
        console.error("Failed to load crypto list:", error);
      }
    }
    loadCryptoList();
  }, []);

  const filteredCrypto = cryptoList.filter(
    (crypto) =>
      crypto.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      crypto.symbol.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAddCoin = () => {
    if (!selectedCoin || !amount) return;

    if (parseFloat(amount) < 0) return;

    const isDuplicate = coins.some((coin) => coin.coin_id === selectedCoin.id);

    if (isDuplicate) {
      alert("Эта монета уже добавлена!");
      return;
    }
    const newCoin = {
      coin_id: selectedCoin.id,
      amount: Number(parseFloat(amount).toFixed(8)),
    };

    setCoins([...coins, newCoin]);
    setSelectedCoin(null);
    setAmount("");
    setSearchTerm("");
  };

  const handleRemoveCoin = (index: number) => {
    setCoins(coins.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const id = await createPortfolio(name, coins);
      console.log(id);
      navigate(`/portfolios/${id}`);
    } catch (error) {
      console.error("Failed to create portfolio:", error);
      alert("Ошибка при создании портфеля");
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) return <EmptyState />;
  console.log(isAuthenticated);
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Создать новый портфель</h1>

      <form onSubmit={handleSubmit} className="space-y-6 max-w-lg">
        <div className="space-y-2">
          <label htmlFor="name">Название портфеля</label>
          <Input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Мой инвестиционный портфель"
            required
          />
        </div>

        <div className="space-y-4">
          <h2 className="text-lg font-medium">Добавить криптовалюты</h2>

          <div className="flex gap-2">
            <div className="flex-1 space-y-2">
              <label
                htmlFor="searchTerm"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >
                Поиск криптовалюты
              </label>
              <Input
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Bitcoin, BTC..."
              />
              {searchTerm && (
                <ul className="border rounded-md max-h-60 overflow-auto">
                  {filteredCrypto.map((crypto) => (
                    <li
                      key={crypto.id}
                      className="p-2 hover:bg-gray-100 cursor-pointer"
                      onClick={() => {
                        setSelectedCoin(crypto);
                        setSearchTerm(
                          `${crypto.name} (${crypto.symbol.toUpperCase()})`
                        );
                      }}
                    >
                      {crypto.name} ({crypto.symbol.toUpperCase()})
                    </li>
                  ))}
                </ul>
              )}
            </div>

            <div className="space-y-2">
              <label
                htmlFor="amount"
                className="block text-sm font-medium text-gray-700 dark:text-gray-300"
              >
                Количество
              </label>
              <Input
                type="number"
                step="0.000001"
                min="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="0.00"
              />
            </div>
          </div>

          <Button
            type="button"
            onClick={handleAddCoin}
            disabled={!selectedCoin || !amount}
          >
            Добавить
          </Button>
        </div>

        {coins.length > 0 && (
          <div className="space-y-2">
            <h3 className="font-medium">Добавленные монеты:</h3>
            <ul className="space-y-2">
              {coins.map((coin, index) => {
                const crypto = cryptoList.find((c) => c.id === coin.coin_id);
                return (
                  <li
                    key={index}
                    className="flex justify-between items-center p-2 border rounded"
                  >
                    <span>
                      {crypto?.name || coin.coin_id} - {coin.amount}
                    </span>
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveCoin(index)}
                    >
                      Удалить
                    </Button>
                  </li>
                );
              })}
            </ul>
          </div>
        )}

        <div className="flex gap-4">
          <Button
            type="submit"
            disabled={loading || !name || coins.length === 0}
          >
            {loading ? "Создание..." : "Создать портфель"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate("/portfolios")}
          >
            Отмена
          </Button>
        </div>
      </form>
    </div>
  );
}

export default CreatePortfolio;
