import type { CryptoData } from "./cryptoData";

export interface Coin {
  id: number;
  coin_id: string;
  amount: number;
  total_value: number;
}

export interface CoinDetail extends Coin {
  coin_deatil: CryptoData;
}

export interface Portfolio {
  id: number;
  name: string;
  coins: Coin[];
  total_value: number;
}

export interface PortfolioDetail {
  id: number;
  name: string;
  coins: CoinDetail[];
  total_value: number;
}

export interface CoinCreate {
  coin_id: string;
  amount: number;
}

export interface CoinUpdate {
  id: number;
  amount: number;
}


export interface PortfolioStore {
  portfolios: Portfolio[];
  portfolio: PortfolioDetail | null;
  loading: boolean;
  error: string | null;
  fetchPortfolios: () => Promise<void>;
  getPortfolio: (id: number) => Promise<void>;
  deletePortfolio: (id: number) => Promise<boolean>;
  createPortfolio: (name: string, coins: CoinCreate[]) => Promise<number>;
  updatePortfolio: (
    id: number,
    updateData?: { name?: string },
    newCoins?: CoinCreate[],
    updateCoins?: CoinUpdate[]
  ) => Promise<void>;
  deletePortfolioCoin: (portfolioId: number, coinId: number) => Promise<void>;
}
