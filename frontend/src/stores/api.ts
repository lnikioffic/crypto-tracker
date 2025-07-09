import axios from "axios";
import { useAuthStore } from "@/stores/authStore";

const API_URL = "http://localhost:8000";

export const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use(async (config) => {
  const { accessToken, refreshToken } = useAuthStore.getState();

  if (config.url?.includes("/auth/refresh")) {
    if (refreshToken) {
      config.headers.Authorization = `Bearer ${refreshToken}`;
    }
  } else if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const { logout, refreshAccessToken } = useAuthStore.getState();

    // Не пытаться рефрешить токен на /auth/refresh или /auth/login
    const isAuthUrl =
      originalRequest.url?.includes("/auth/refresh") ||
      originalRequest.url?.includes("/auth/login");

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !isAuthUrl
    ) {
      originalRequest._retry = true;
      try {
        await refreshAccessToken();
        return api(originalRequest);
      } catch (refreshError) {
        logout();
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
