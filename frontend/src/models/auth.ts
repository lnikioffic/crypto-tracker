export interface UserLogin {
  username: string;
  password: string;
}

export interface User {
  id: string;
  username: string;
  email: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string | null;
}

export interface AuthStore {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isLoading: boolean;
  error: string | null;
  register: (
    username: string,
    email: string,
    password: string
  ) => Promise<void>;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshAccessToken: () => Promise<void>;
  fetchUser: () => Promise<void>;
}
