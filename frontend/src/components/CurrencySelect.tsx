import { useCurrencyStore, Currency } from "@/stores/currencyStore";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { useLocation, useNavigate } from "react-router-dom";
import { useTransition } from "react";

function CurrencySelect() {
  const { currency, setCurrency } = useCurrencyStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [isPending, startTransition] = useTransition();

  // Получаем массив валют из объекта Currency
  const currencies = Object.keys(Currency) as Currency[];

  const handleCurrencyChange = (value: Currency) => {
    setCurrency(value);

    // Обновляем URL с новым параметром валюты
    const searchParams = new URLSearchParams(location.search);
    searchParams.set("vs_currency", value.toLowerCase());

    startTransition(() => {
      navigate(
        {
          pathname: location.pathname,
          search: searchParams.toString(),
        },
        { replace: true } // Заменяем текущую запись в истории
      );
    });
    window.location.reload();
  };

  return (
    <Select
      value={currency}
      onValueChange={handleCurrencyChange}
      disabled={isPending}
    >
      <SelectTrigger className="w-[120px]">
        <SelectValue placeholder="Валюта" />
      </SelectTrigger>
      <SelectContent>
        {currencies.map((curr) => (
          <SelectItem key={curr} value={curr}>
            {curr}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
}

export default CurrencySelect;
