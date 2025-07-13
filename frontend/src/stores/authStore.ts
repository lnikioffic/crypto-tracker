import { create } from "zustand";
import type { TokenResponse, AuthStore, User } from "../models/auth";
import { api } from "./api";
import qs from "qs";

export const useAuthStore = create<AuthStore>()((set, get) => ({
  user: null,
  isLoading: false,
  error: null,

  register: async (username, email, password) => {
    set({ isLoading: true, error: null });
    try {
      await api.post<TokenResponse>("/auth/register", {
        username,
        email,
        password,
      });

      await get().fetchUser();
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Login failed",
        isLoading: false,
      });
      throw error;
    }
  },

  login: async (username, password) => {
    set({ isLoading: true, error: null });
    try {
      await api.post<TokenResponse>(
        `/auth/login`,
        qs.stringify({ username, password }),
        { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
      );

      await get().fetchUser();
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Login failed",
        isLoading: false,
      });
      throw error;
    }
  },

  logout: async () => {
    try {
      await api.post("/auth/logout");
    } finally {
      set({ user: null, error: null });
    }
  },

  refreshAccessToken: async () => {
    try {
      await api.post<TokenResponse>(`/auth/refresh`);
    } catch (error) {
      get().logout();
      throw error;
    }
  },

  fetchUser: async () => {
    set({ isLoading: true });
    try {
      const { data } = await api.get<User>(`/user/me`);
      set({ user: data, isLoading: false });
    } catch (error) {
      set({ error: "Failed to fetch user", isLoading: false });
      throw error;
    }
  },
}));
// useAuthStore.subscribe(console.log);
