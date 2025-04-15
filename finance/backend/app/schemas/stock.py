from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class ChartDataPoint(BaseModel):
    date: str
    price: float


class StockBase(BaseModel):
    symbol: str
    name: str
    current_price: float
    change_percent: float = 0.0
    is_positive: bool = True
    currency: str = "USD"


class StockCreate(StockBase):
    pass


class StockUpdate(BaseModel):
    name: Optional[str] = None
    current_price: Optional[float] = None
    change_percent: Optional[float] = None
    is_positive: Optional[bool] = None
    currency: Optional[str] = None


class Stock(StockBase):
    id: int

    class Config:
        from_attributes = True  # compatibility with SQLAlchemy ORM models


class StockDetail(Stock):
    market_cap: Optional[float] = None
    volume: Optional[int] = None
    avg_volume: Optional[int] = None
    pe_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    high_52w: Optional[float] = None
    low_52w: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    open: Optional[float] = None
    previous_close: Optional[float] = None
    historical_data: Optional[List[ChartDataPoint]] = None

    class Config:
        from_attributes = True  # compatibility with SQLAlchemy ORM models 