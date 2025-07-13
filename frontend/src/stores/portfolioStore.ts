import type { Portfolio, PortfolioStore } from "@/models/portfolio";
import { create } from "zustand";
import { useAuthStore } from "@/stores/authStore";
import { api } from "./api";
import axios from "axios";

export const usePortfolioStore = create<PortfolioStore>((set) => ({
  portfolios: [],
  loading: false,
  error: null,

  fetchPortfolios: async () => {
    set({ loading: true, error: null });
    const { user } = useAuthStore.getState();
    const isAuthenticated = !!user;
    try {
      if (!isAuthenticated) {
        throw new Error("Not authenticated");
      }

      const { data } = await api.get<Portfolio[]>("/portfolio/", {
        params: { vs_currency: "usd" },
      });

      set({ portfolios: data, loading: false });
    } catch (error: unknown) {
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

  reset: () => set({ portfolios: [], loading: false, error: null }),
}));
