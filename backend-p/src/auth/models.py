from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.mixin import TimeStampMixin
from src.models import Base
from src.portfolio.models import Portfolio


class User(TimeStampMixin, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    portfolios: Mapped[list['Portfolio']] = relationship(back_populates='user')
