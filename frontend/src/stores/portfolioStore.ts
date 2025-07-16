import type {
  Portfolio,
  PortfolioDetail,
  PortfolioStore,
} from "@/models/portfolio";
import { create } from "zustand";
import { useAuthStore } from "@/stores/authStore";
import { api } from "./api";
import axios from "axios";
import { useCurrencyStore } from "./currencyStore";

export const usePortfolioStore = create<PortfolioStore>((set) => ({
  portfolios: [],
  portfolio: null,
  loading: false,
  error: null,

  fetchPortfolios: async () => {
    set({ loading: true, error: null });
    const { user } = useAuthStore.getState();
    const isAuthenticated = !!user;
    const { currency } = useCurrencyStore.getState();
    try {
      if (!isAuthenticated) {
        throw new Error("Not authenticated");
      }

      const { data } = await api.get<Portfolio[]>("/portfolio/", {
        params: { vs_currency: currency.toLocaleLowerCase() },
      });

      set({ portfolios: data, loading: false });
    } catch (error) {
      let errorMessage = "Failed to load portfolios";

      if (axios.isAxiosError(error)) {
        if (error.response?.status === 401) {
          errorMessage = "Session expired, please login again";
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail;
        }
      } else if (
        error instanceof Error &&
        error.message === "Not authenticated"
      ) {
        errorMessage = "Please login to view portfolios";
      }

      set({
        error: errorMessage,
        loading: false,
      });
      console.error("Error fetching portfolios:", error);
    }
  },

  getPortfolio: async (id: number) => {
    set({ loading: true, error: null });
    const { currency } = useCurrencyStore.getState();
    try {
      const { data } = await api.get<PortfolioDetail>(`/portfolio/${id}`, {
        params: { vs_currency: currency.toLocaleLowerCase() },
      });
      set({ portfolio: data, loading: false });
    } catch {
      const errorMessage = "Failed to load portfolios";
      set({
        portfolio: null,
        error: errorMessage,
        loading: false,
      });
    }
  },

  deletePortfolio: async (id: number) => {
    set({ loading: true, error: null });
    try {
      await api.delete(`/portfolio/${id}`);

      set({ loading: false });
      return true; // Успешное удаление
    } catch (error) {
      const errorMessage = axios.isAxiosError(error)
        ? error.response?.data?.detail || "Ошибка при удалении портфеля"
        : "Неизвестная ошибка";
      set({
        portfolio: null,
        error: errorMessage,
        loading: false,
      });
      return false;
    }
  },

  createPortfolio: async (name, coins) => {
    set({ loading: true, error: null });
    try {
      const { data } = await api.post("/portfolio", {
        portfolio: { name },
        coins,
      });
      console.log(data.id);
      return data.id;
    } catch {
      alert("Ошибка при создании портфеля");
    }
  },

  updatePortfolio: async (id, updateData, newCoins, updateCoins) => {
    try {
      await api.patch(`/portfolio/${id}`, {
        update_data: updateData,
        new_coins: newCoins,
        update_coins: updateCoins,
      });
    } catch (error) {
      console.error("Ошибка обновления портфеля:", error);
      throw error;
    }
  },

  deletePortfolioCoin: async (portfolioId, coinId) => {
    try {
      await api.delete(`/portfolio/${portfolioId}/${coinId}`);
    } catch (error) {
      console.error("Ошибка удаления монеты:", error);
      throw error;
    }
  },

  reset: () => set({ portfolios: [], loading: false, error: null }),
}));
