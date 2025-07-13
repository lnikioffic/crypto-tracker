export interface Coin {
  id: number;
  coin_id: string;
  amount: number;
  total_value: number;
}

export interface Portfolio {
  id: number;
  name: string;
  coins: Coin[];
  total_value: number;
}

export interface PortfolioStore {
  portfolios: Portfolio[];
  portfolio: Portfolio | null;
  loading: boolean;
  error: string | null;
  fetchPortfolios: () => Promise<void>;
  fetchPortfolioById: (id: number) => Promise<void>;
}
