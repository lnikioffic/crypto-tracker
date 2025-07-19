import { api_rs } from "./api";
import type { CryptoData } from "@/models/cryptoData";
import { useCurrencyStore } from "./currencyStore";

// Получить список всех криптовалют
export async function fetchCryptoList(): Promise<CryptoData[]> {
  const { currency } = useCurrencyStore.getState();

  const response = await api_rs.get<CryptoData[]>("/coins/", {
    params: {
      vs_currency: currency.toLowerCase(),
    },
  });
  return response.data;
}
