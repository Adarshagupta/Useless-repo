from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_stocks
from app.schemas.stock import Stock, StockDetail, ChartDataPoint, StockCreate, StockUpdate

router = APIRouter()


@router.get("/", response_model=List[Stock])
def get_stocks(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve all stocks.
    """
    stocks = crud_stocks.stock.get_multi(db, skip=skip, limit=limit)
    return stocks


@router.get("/search", response_model=List[Stock])
def search_stocks(
    *,
    db: Session = Depends(deps.get_db),
    query: str = Query(..., min_length=1, description="Search query for stock name or symbol"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results to return"),
):
    """
    Search for stocks by name or symbol.
    """
    stocks = crud_stocks.stock.search(db, query=query, limit=limit)
    return stocks


@router.get("/top-gainers", response_model=List[Stock])
def get_top_gainers(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(5, ge=1, le=100, description="Maximum number of results to return"),
):
    """
    Get top gaining stocks.
    """
    stocks = crud_stocks.stock.get_top_gainers(db, limit=limit)
    return stocks


@router.get("/top-losers", response_model=List[Stock])
def get_top_losers(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(5, ge=1, le=100, description="Maximum number of results to return"),
):
    """
    Get top losing stocks.
    """
    stocks = crud_stocks.stock.get_top_losers(db, limit=limit)
    return stocks


@router.get("/most-active", response_model=List[Stock])
def get_most_active(
    *,
    db: Session = Depends(deps.get_db),
    limit: int = Query(5, ge=1, le=100, description="Maximum number of results to return"),
):
    """
    Get most active stocks.
    """
    stocks = crud_stocks.stock.get_most_active(db, limit=limit)
    return stocks


@router.get("/{symbol}", response_model=StockDetail)
def get_stock(
    *,
    db: Session = Depends(deps.get_db),
    symbol: str,
):
    """
    Get stock by symbol.
    """
    stock = crud_stocks.stock.get_by_symbol(db, symbol=symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
    return stock


@router.get("/{symbol}/chart", response_model=List[ChartDataPoint])
def get_stock_chart(
    *,
    db: Session = Depends(deps.get_db),
    symbol: str,
    period: str = Query("1y", description="Time period (e.g., 1d, 1w, 1m, 3m, 6m, 1y, 5y)"),
    interval: str = Query("1d", description="Data interval (e.g., 1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo)"),
):
    """
    Get chart data for a specific stock.
    """
    stock = crud_stocks.stock.get_by_symbol(db, symbol=symbol)
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")
        
    chart_data = crud_stocks.stock.get_chart_data(db, stock_id=stock.id, period=period, interval=interval)
    return chart_data 