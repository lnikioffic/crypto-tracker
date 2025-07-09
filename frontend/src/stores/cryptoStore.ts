import { api } from "./api";
import type { CryptoData } from "@/models/cryptoData";

// Получить список всех криптовалют
export async function fetchCryptoList(): Promise<CryptoData[]> {
  const response = await api.get<CryptoData[]>("/coins");
  return response.data;
}
