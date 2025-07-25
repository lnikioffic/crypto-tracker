import logging

from sqlalchemy import delete, select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.portfolio.models import Portfolio, PortfolioCoin
from src.portfolio.schemas import (
    PortfolioCoinCreate,
    PortfolioCoinUpdate,
    PortfolioCreate,
    PortfolioRead,
    PortfolioUpdate,
)

log = logging.getLogger(__name__)

async def get_portfolio(
    session: AsyncSession, portfolio_id: int, user_id: int
) -> PortfolioRead | None:
    query = (
        select(Portfolio)
        .options(joinedload(Portfolio.coins))
        .filter(Portfolio.id == portfolio_id, Portfolio.user_id == user_id)
    )
    result: Result = await session.execute(query)
    portfolio = result.unique().scalar_one_or_none()
    return portfolio


async def get_portfolios(session: AsyncSession, user_id: int) -> list[PortfolioRead]:
    query = (
        select(Portfolio)
        .options(joinedload(Portfolio.coins))
        .filter(Portfolio.user_id == user_id)
    )
    result: Result = await session.execute(query)
    portfolios = result.scalars().unique().all()
    return list(portfolios)


async def create_portfolio(
    session: AsyncSession,
    portfolio_create: PortfolioCreate,
    user_id: int,
    coins: list[PortfolioCoinCreate],
):

    portfolio = Portfolio(**portfolio_create.model_dump(), user_id=user_id)

    portfolio.coins.extend([PortfolioCoin(**coin.model_dump()) for coin in coins])

    session.add_all([portfolio])
    try:
        await session.commit()
    except Exception as ex:
        log.error(ex)
        await session.rollback()
        raise ex
    return portfolio


async def delete_portfolio(session: AsyncSession, portfolio_id: int, user_id: int):
    query = delete(Portfolio).filter(
        Portfolio.id == portfolio_id, Portfolio.user_id == user_id
    )
    result: Result = await session.execute(query)

    try:
        await session.commit()
    except Exception as ex:
        log.error(ex)
        await session.rollback()
        raise ex
    return result.rowcount


async def delete_portfolio_coin(
    session: AsyncSession, coin_id: int, portfolio_id: int, user_id: int
):
    query = delete(PortfolioCoin).filter(
        PortfolioCoin.id == coin_id,
        PortfolioCoin.portfolio_id == portfolio_id,
        PortfolioCoin.portfolio.has(user_id=user_id),
    )
    result: Result = await session.execute(query)

    try:
        await session.commit()
    except Exception as ex:
        log.error(ex)
        await session.rollback()
        raise ex
    return result.rowcount


async def update_portfolio_attributes(
    session: AsyncSession,
    portfolio_id: int,
    user_id: int,
    update_data: PortfolioUpdate,
) -> Portfolio:
    """Обновляет только атрибуты портфеля (например, название)"""
    portfolio = await _get_portfolio_with_coins(session, portfolio_id, user_id)

    for attr, value in update_data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(portfolio, attr, value)

    await _commit_changes(session)
    return portfolio


async def update_portfolio_coins(
    session: AsyncSession,
    portfolio_id: int,
    user_id: int,
    update_coins: list[PortfolioCoinUpdate],
) -> Portfolio:
    """Обновляет только существующие монеты в портфеле"""
    portfolio = await _get_portfolio_with_coins(session, portfolio_id, user_id)

    for coin_update in update_coins:
        for coin in portfolio.coins:
            if coin.id == coin_update.id:
                coin.amount = coin_update.amount

    await _commit_changes(session)
    return portfolio


async def add_portfolio_coins(
    session: AsyncSession,
    portfolio_id: int,
    user_id: int,
    new_coins: list[PortfolioCoinCreate],
) -> Portfolio:
    """Добавляет новые монеты в портфель"""
    portfolio = await _get_portfolio_with_coins(session, portfolio_id, user_id)

    portfolio.coins.extend([PortfolioCoin(**coin.model_dump()) for coin in new_coins])

    await _commit_changes(session)
    return portfolio


async def _get_portfolio_with_coins(
    session: AsyncSession,
    portfolio_id: int,
    user_id: int,
) -> Portfolio:
    """Получает портфель с монетами или вызывает исключение"""
    query = (
        select(Portfolio)
        .options(joinedload(Portfolio.coins))
        .filter(Portfolio.id == portfolio_id, Portfolio.user_id == user_id)
    )
    result: Result = await session.execute(query)
    portfolio = result.unique().scalar_one_or_none()

    if not portfolio:
        raise ValueError("Portfolio not found")

    return portfolio


async def _commit_changes(session: AsyncSession) -> None:
    """Выполняет commit с обработкой ошибок"""
    try:
        await session.commit()
    except Exception as ex:
        log.error(ex)
        await session.rollback()
        raise ex


# Update portfolio with new coins and updated coins
async def update_portfolio(
    session: AsyncSession,
    portfolio_id: int,
    user_id: int,
    update_data: PortfolioUpdate,
    new_coins: list[PortfolioCoinCreate] | None = None,
    update_coins: list[PortfolioCoinUpdate] | None = None,
):
    query = (
        select(Portfolio)
        .options(joinedload(Portfolio.coins))
        .filter(Portfolio.id == portfolio_id, Portfolio.user_id == user_id)
    )
    result: Result = await session.execute(query)

    portfolio = result.unique().scalar_one_or_none()

    if not portfolio:
        raise ValueError("Portfolio not found")

    for attr, value in update_data.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(portfolio, attr, value)

    if update_coins:
        for coin_update in update_coins:
            for coin in portfolio.coins:
                if coin.id == coin_update.id:
                    coin.amount = coin_update.amount

    # Добавляем новые монеты, если переданы
    if new_coins:
        for coin in new_coins:
            portfolio.coins.append(PortfolioCoin(**coin.model_dump()))

    try:
        await session.commit()
    except Exception as ex:
        log.error(ex)
        await session.rollback()
        raise ex
    return portfolio
