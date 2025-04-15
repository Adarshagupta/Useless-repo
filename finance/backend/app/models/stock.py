from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    change_percent = Column(Float, default=0.0)
    is_positive = Column(Boolean, default=True)
    currency = Column(String, default="USD")
    
    # Additional details
    market_cap = Column(Float, nullable=True)
    volume = Column(Integer, nullable=True)
    avg_volume = Column(Integer, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    dividend_yield = Column(Float, nullable=True)
    high_52w = Column(Float, nullable=True)
    low_52w = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    open = Column(Float, nullable=True)
    previous_close = Column(Float, nullable=True)
    
    # Timestamp for last update
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship to historical data (will be implemented separately)
    # historical_data = relationship("StockHistoricalData", back_populates="stock")
    
    def __repr__(self):
        return f"<Stock {self.symbol}: ${self.current_price}>" 