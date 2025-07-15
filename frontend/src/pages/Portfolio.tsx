import PortfolioCard from "@/components/PortfolioCard";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useAuthStore } from "@/stores/authStore";
import { usePortfolioStore } from "@/stores/portfolioStore";
import { useEffect } from "react";

const LoadingState = () => (
  <div className="container mx-auto py-8 space-y-4">
    {[...Array(3)].map((_, i) => (
      <Skeleton key={i} className="h-32 w-full rounded-lg" />
    ))}
  </div>
);

const EmptyState = ({ onRetry }: { onRetry: () => void }) => {
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = !!user;

  return (
    <div className="text-center py-12 space-y-4">
      <p className="text-muted-foreground">
        {isAuthenticated
          ? "У вас пока нет портфелей"
          : "Авторизуйтесь для просмотра портфелей"}
      </p>
      <Button onClick={onRetry} variant="outline">
        Обновить
      </Button>
    </div>
  );
};

const ErrorState = ({
  error,
  onRetry,
}: {
  error: string;
  onRetry: () => void;
}) => (
  <div className="text-center py-12 space-y-4">
    <p className="text-destructive">{error}</p>
    <Button onClick={onRetry} variant="outline">
      Попробовать снова
    </Button>
  </div>
);

function PortfolioPage() {
  const { portfolios, loading, error, fetchPortfolios } = usePortfolioStore();
  const user = useAuthStore((s) => s.user);
  const isAuthenticated = !!user;

  useEffect(() => {
    if (isAuthenticated) {
      fetchPortfolios();
    }
  }, [fetchPortfolios, isAuthenticated]);

  const handleRetry = () => {
    fetchPortfolios();
  };

  if (loading) return <LoadingState />;

  return (
    <div className="container mx-auto py-8 space-y-4">
      {error ? (
        <ErrorState error={error} onRetry={handleRetry} />
      ) : portfolios.length === 0 ? (
        <EmptyState onRetry={handleRetry} />
      ) : (
        <>
          <h1 className="text-3xl font-bold mb-6">Мои портфели</h1>
          <div className="space-y-4">
            {portfolios.map((portfolio) => (
              <PortfolioCard key={portfolio.id} portfolio={portfolio} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default PortfolioPage;
