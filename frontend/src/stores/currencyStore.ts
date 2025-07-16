import { create } from "zustand";
import { persist } from "zustand/middleware";

export const Currency = {
  USD: "usd",
  RUB: "run",
} as const;

export type Currency = keyof typeof Currency;

interface CurrencyState {
  currency: Currency;
  setCurrency: (currency: Currency) => void;
}

export const useCurrencyStore = create<CurrencyState>()(
  persist(
    (set) => ({
      currency: "USD",
      setCurrency: (currency) => set({ currency }),
    }),
    {
      name: "currency-preference",
    }
  )
);
