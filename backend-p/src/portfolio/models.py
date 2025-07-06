from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.mixin import TimeStampMixin
from src.models import Base

if TYPE_CHECKING:
    from src.auth.models import User


class Portfolio(TimeStampMixin, Base):
    __tablename__ = 'portfolios'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', onupdate='CASCADE', ondelete='RESTRICT')
    )

    user: Mapped['User'] = relationship(back_populates='portfolios')
    coins: Mapped[list['PortfolioCoin']] = relationship(back_populates='portfolio')


class PortfolioCoin(TimeStampMixin, Base):
    __tablename__ = 'portfolio_coins'

    id: Mapped[int] = mapped_column(primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey('portfolios.id', onupdate='CASCADE', ondelete='CASCADE')
    )
    coin_id: Mapped[str] = mapped_column(String(50))
    amount: Mapped[float] = mapped_column(default=0.0)

    # constrein unique
    portfolio: Mapped[Portfolio] = relationship(back_populates='coins')
