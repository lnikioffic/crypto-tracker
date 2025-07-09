import { Card } from "./ui/card";
import React from "react";
import type { CryptoData } from "@/models/cryptoData";

type CryptocurrencyCardProps = {
  data: CryptoData;
};

const CryptocurrencyCard: React.FC<CryptocurrencyCardProps> = ({ data }) => {
  const { symbol, name, image, current_price, price_change_percentage_24h } =
    data;
  const isPositive = price_change_percentage_24h >= 0;

  return (
    <Card className="p-4 flex flex-col gap-2 shadow-md min-w-[220px]">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          <img
            src={image}
            alt={name}
            className="w-8 h-8 rounded-full bg-white"
          />
          <span className="font-bold text-lg">{name}</span>
        </div>
        <span className="uppercase text-gray-500">{symbol}</span>
      </div>
      <div className="text-2xl font-semibold">
        ${current_price.toLocaleString(undefined, { maximumFractionDigits: 8 })}
      </div>
      <div
        className={`text-sm font-medium ${
          isPositive ? "text-green-600" : "text-red-600"
        }`}
      >
        {isPositive ? "+" : ""}
        {price_change_percentage_24h.toFixed(2)}%
      </div>
    </Card>
  );
};

export default CryptocurrencyCard;
