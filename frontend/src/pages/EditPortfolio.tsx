import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { CryptoData } from "@/models/cryptoData";
import type { Coin, CoinCreate } from "@/models/portfolio";
import { fetchCryptoList } from "@/stores/cryptoStore";
import { usePortfolioStore } from "@/stores/portfolioStore";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

function EditPortfolio() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [cryptoList, setCryptoList] = useState<CryptoData[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCoin, setSelectedCoin] = useState<CryptoData | null>(null);
  const [amount, setAmount] = useState("");
  const [existingCoins, setExistingCoins] = useState<Coin[]>([]);
  const [newCoins, setNewCoins] = useState<CoinCreate[]>([]);
  const {
    portfolio,
    loading,
    getPortfolio,
    updatePortfolio,
    deletePortfolioCoin,
  } = usePortfolioStore();

  // Загрузка данных портфеля и списка криптовалют
  useEffect(() => {
    async function loadData() {
      try {
        if (id) {
          await getPortfolio(parseInt(id));
        }
        const cryptoData = await fetchCryptoList();
        setCryptoList(cryptoData);
      } catch (error) {
        console.error("Ошибка загрузки данных:", error);
      }
    }
    loadData();
  }, [id, getPortfolio]);

  useEffect(() => {
    if (portfolio) {
      setName(portfolio.name);
      setExistingCoins(
        portfolio.coins.map((coin) => ({
          id: coin.id,
          coin_id: coin.coin_id,
          amount: coin.amount,
          total_value: coin.total_value,
        }))
      );
    }
  }, [portfolio]);

  const filteredCrypto = cryptoList.filter(
    (crypto) =>
      crypto.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      crypto.symbol.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAddNewCoin = () => {
    if (!selectedCoin || !amount || parseFloat(amount) <= 0) return;

    setNewCoins([
      ...newCoins,
      {
        coin_id: selectedCoin.id,
        amount: parseFloat(amount),
      },
    ]);
    setSelectedCoin(null);
    setAmount("");
    setSearchTerm("");
  };

  const handleRemoveNewCoin = (index: number) => {
    setNewCoins(newCoins.filter((_, i) => i !== index));
  };

  const handleUpdateExistingCoin = (index: number, newAmount: string) => {
    const amountValue = parseFloat(newAmount);
    if (isNaN(amountValue)) return;

    setExistingCoins((prev) =>
      prev.map((coin, i) =>
        i === index ? { ...coin, amount: amountValue } : coin
      )
    );
  };

  const handleRemoveExistingCoin = async (coinId: number, index: number) => {
    try {
      // Удаляем монету с сервера
      await deletePortfolioCoin(Number(id), coinId);
      // Обновляем локальное состояние
      setExistingCoins(existingCoins.filter((_, i) => i !== index));
    } catch (error) {
      console.error("Ошибка удаления монеты:", error);
      alert("Не удалось удалить монету");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const updateData = name ? { name } : undefined;
      const updateCoins = existingCoins.map((coin) => ({
        id: coin.id,
        amount: coin.amount,
      }));

      await updatePortfolio(Number(id), updateData, newCoins, updateCoins);

      navigate(`/portfolios/${id}`);
    } catch (error) {
      console.error("Ошибка обновления портфеля:", error);
      alert("Ошибка при обновлении портфеля");
    }
  };

  if (loading && !name) {
    return <div className="container mx-auto py-8">Загрузка...</div>;
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

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Редактировать портфель</h1>

      <form onSubmit={handleSubmit} className="space-y-6 max-w-lg">
        <div className="space-y-2">
          <label htmlFor="name">Название портфеля</label>
          <Input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Новое название портфеля"
          />
        </div>

        <div className="space-y-4">
          <h2 className="text-lg font-medium">Добавить новые монеты</h2>

          <div className="flex gap-2">
            <div className="flex-1 space-y-2">
              <label htmlFor="search">Поиск криптовалюты</label>
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
              <label htmlFor="amount">Количество</label>
              <Input
                type="number"
                step="0.000001"
                min="0.000001"
                value={amount}
                onChange={(e) => {
                  const value = e.target.value;
                  if (/^\d*\.?\d*$/.test(value) && parseFloat(value) >= 0) {
                    setAmount(value);
                  }
                }}
                placeholder="0.00"
              />
            </div>
          </div>

          <Button
            type="button"
            onClick={handleAddNewCoin}
            disabled={!selectedCoin || !amount || parseFloat(amount) <= 0}
          >
            Добавить
          </Button>

          {newCoins.length > 0 && (
            <div className="space-y-2">
              <h3 className="font-medium">Новые монеты:</h3>
              <ul className="space-y-2">
                {newCoins.map((coin, index) => {
                  const crypto = cryptoList.find((c) => c.id === coin.coin_id);
                  return (
                    <li
                      key={`new-${index}`}
                      className="flex justify-between items-center p-2 border rounded"
                    >
                      <span>
                        {crypto?.name || coin.coin_id} - {coin.amount}
                      </span>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => handleRemoveNewCoin(index)}
                      >
                        Удалить
                      </Button>
                    </li>
                  );
                })}
              </ul>
            </div>
          )}
        </div>

        {existingCoins.length > 0 && (
          <div className="space-y-4">
            <h2 className="text-lg font-medium">Существующие монеты</h2>
            <ul className="space-y-2">
              {existingCoins.map((coin, index) => {
                const crypto = cryptoList.find((c) => c.id === coin.coin_id);
                return (
                  <li
                    key={`existing-${coin.id}`}
                    className="flex flex-col gap-2 p-2 border rounded"
                  >
                    <div className="flex justify-between items-center">
                      <span className="font-medium">
                        {crypto?.name || coin.coin_id}
                      </span>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => handleRemoveExistingCoin(coin.id, index)}
                        disabled={loading}
                      >
                        {loading ? "Удаление..." : "Удалить"}
                      </Button>
                    </div>
                    <div className="flex items-center gap-2">
                      <label className="text-sm">Количество:</label>
                      <Input
                        type="number"
                        step="0.000001"
                        min="0.000001"
                        value={coin.amount}
                        onChange={(e) =>
                          handleUpdateExistingCoin(index, e.target.value)
                        }
                        className="w-32"
                      />
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>
        )}

        <div className="flex gap-4">
          <Button
            type="submit"
            disabled={
              name === "" && newCoins.length === 0 && existingCoins.length === 0
            }
          >
            {loading ? "Сохранение..." : "Сохранить изменения"}
          </Button>
          <Button
            type="button"
            variant="outline"
            onClick={() => navigate(`/portfolios/${id}`)}
          >
            Отмена
          </Button>
        </div>
      </form>
    </div>
  );
}

export default EditPortfolio;
