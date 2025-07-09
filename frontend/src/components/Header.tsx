import { cn } from "@/lib/utils";
import { Button } from "./ui/button";
import { useState } from "react";
import { useAuthStore } from "@/stores/authStore";
import LoginModal from "./modals/Login";
import RegisterModal from "./modals/Register";

function Header() {
  const [loginOpen, setLoginOpen] = useState(false);
  const [registerOpen, setRegisterOpen] = useState(false);
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);
  const isAuthenticated = !!user;

  console.log(isAuthenticated);
  return (
    <header className="border-b-4">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-lg md:text-x1 font-bold text-foreground">
              CryptoTracker
            </h1>
          </div>

          <div className="flex space-x-4 md:space-x-8">
            <Button
              variant="ghost"
              className={cn(
                "px-3 py-2 rounded-md text-sm font-medium transition-colors"
                // currentPage === "market" && "bg-accent text-accent-foreground"
              )}
            >
              Криптовалюты
            </Button>
            <Button
              variant="ghost"
              className={cn(
                "px-3 py-2 rounded-md text-sm font-medium"
                // currentPage === "portfolio" && "bg-accent text-accent-foreground"
              )}
            >
              Портфель
            </Button>
          </div>

          <div className="flex items-center space-x-2 md:space-x-6">
            {isAuthenticated ? (
              <div className="flex items-center space-x-1 md:space-x-3">
                <Button
                  variant="ghost"
                  size="sm"
                  className="text-xs md:text-sm px-2 md:px-4"
                >
                  Профиль
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={logout}
                  className="text-xs md:text-sm px-2 md:px-4"
                >
                  Выйти
                </Button>
              </div>
            ) : (
              <>
                <Button
                  size="sm"
                  onClick={() => setLoginOpen(true)}
                  className="text-xs md:text-sm px-2 md:px-4"
                >
                  Войти
                </Button>
                <LoginModal
                  isOpen={loginOpen}
                  onClose={() => setLoginOpen(false)}
                />
                <Button
                  size="sm"
                  onClick={() => setRegisterOpen(true)}
                  className="text-xs md:text-sm px-2 md:px-4"
                >
                  Зарегистрироваться
                </Button>
                <RegisterModal
                  isOpen={registerOpen}
                  onClose={() => setRegisterOpen(false)}
                />
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
