import { api } from "./api";
import type { CryptoData } from "@/models/cryptoData";
import { useCurrencyStore } from "./currencyStore";

// Получить список всех криптовалют
export async function fetchCryptoList(): Promise<CryptoData[]> {
  const { currency } = useCurrencyStore.getState();

  const response = await api.get<CryptoData[]>("/coins", {
    params: {
      vs_currency: currency.toLowerCase(),
    },
  });
  return response.data;
}
