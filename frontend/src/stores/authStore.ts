import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { TokenResponse, AuthStore, User } from "../models/auth";
import { api } from "./api";
import qs from "qs";

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isLoading: false,
      error: null,

      register: async (username, email, password) => {
        set({ isLoading: true, error: null });
        try {
          const { data } = await api.post<TokenResponse>("/auth/register", {
            username,
            email,
            password,
          });

          set({
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
            isLoading: false,
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
          const { data } = await api.post<TokenResponse>(
            `/auth/login`,
            qs.stringify({ username, password }),
            { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
          );

          set({
            accessToken: data.access_token,
            refreshToken: data.refresh_token,
            isLoading: false,
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

      logout: () => {
        set({ user: null, accessToken: null, refreshToken: null, error: null });
      },

      refreshAccessToken: async () => {
        const { refreshToken } = get();

        if (!refreshToken) {
          get().logout();
          throw new Error("No refresh token");
        }
        try {
          const { data } = await api.post<TokenResponse>(
            `/auth/refresh`,
            {},
            { headers: { Authorization: `Bearer ${refreshToken}` } }
          );

          console.log(data.access_token);

          set({
            accessToken: data.access_token,
            refreshToken, // сохраняем старый refreshToken
          });
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
    }),
    {
      name: "auth",
      partialize: (state) => ({
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
      }),
    }
  )
);
// useAuthStore.subscribe(console.log);
