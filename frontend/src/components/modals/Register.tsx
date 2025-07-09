import React, { useState } from "react";
import { useAuthStore } from "@/stores/authStore";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface RegisterModalProps {
  isOpen: boolean;
  onClose: () => void;
}

function RegisterModal({ isOpen, onClose }: RegisterModalProps) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const register = useAuthStore((s) => s.register);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await register(username, email, password);
      onClose();
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else if (typeof err === "string") {
        setError(err);
      } else {
        setError("Ошибка регистрации");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="bg-background rounded-lg shadow-lg p-8 w-full max-w-md relative">
        <button
          className="absolute top-2 right-2 text-xl text-gray-400 hover:text-gray-700"
          onClick={onClose}
          aria-label="Закрыть"
        >
          ×
        </button>
        <h2 className="text-xl font-bold mb-2">Регистрация</h2>
        <p className="mb-4 text-sm text-muted-foreground">
          Введите данные для создания аккаунта
        </p>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-sm font-medium">Логин</label>
            <Input
              type="text"
              autoFocus
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
              required
            />
          </div>
          <div>
            <label className="block mb-1 text-sm font-medium">Email</label>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="email@example.com"
              required
            />
          </div>
          <div>
            <label className="block mb-1 text-sm font-medium">Пароль</label>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
            />
          </div>
          {error && <div className="text-red-600 text-sm">{error}</div>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Регистрация..." : "Зарегистрироваться"}
          </Button>
        </form>
      </div>
    </div>
  );
}

export default RegisterModal;
