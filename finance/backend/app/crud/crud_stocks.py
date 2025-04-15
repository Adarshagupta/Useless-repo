from typing import List, Optional, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.crud.base import CRUDBase
from app.models.stock import Stock
from app.schemas.stock import StockCreate, StockUpdate, ChartDataPoint

import random  # For demo data - will be replaced with actual data source


class CRUDStock(CRUDBase[Stock, StockCreate, StockUpdate]):
    def get_by_symbol(self, db: Session, *, symbol: str) -> Optional[Stock]:
        """
        Get a stock by its symbol.
        """
        # In a real app, this would fetch from the database
        # For demo, we're generating a stock with the given symbol
        
        # Check if it exists in the database
        db_stock = db.query(self.model).filter(func.lower(self.model.symbol) == symbol.lower()).first()
        
        if db_stock:
            return db_stock
            
        # For demo purposes, create a mock stock object with details
        # In production, you'd return None or raise an exception
        mock_stock = self._create_mock_stock(symbol)
        return mock_stock
    
    def search(self, db: Session, *, query: str, limit: int = 10) -> List[Stock]:
        """
        Search for stocks by name or symbol.
        """
        # In a real app, do a database search
        # For demo, generate some mock results
        search_query = f"%{query}%"
        stocks = db.query(self.model).filter(
            (func.lower(self.model.symbol).like(search_query.lower())) | 
            (func.lower(self.model.name).like(search_query.lower()))
        ).limit(limit).all()
        
        # If no results in DB, generate some mock stocks for demo purposes
        if not stocks:
            mock_symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
            mock_names = ['Apple Inc.', 'Microsoft Corporation', 'Alphabet Inc.', 'Amazon.com Inc.', 'Tesla, Inc.']
            
            mock_stocks = []
            for i, (symbol, name) in enumerate(zip(mock_symbols, mock_names)):
                if query.lower() in symbol.lower() or query.lower() in name.lower():
                    stock = Stock(
                        id=i+1,
                        symbol=symbol,
                        name=name,
                        current_price=round(random.uniform(50, 3000), 2),
                        change_percent=round(random.uniform(-5, 5), 2),
                        is_positive=random.random() > 0.5,
                        currency="USD"
                    )
                    mock_stocks.append(stock)
            
            return mock_stocks[:limit]
            
        return stocks
    
    def get_chart_data(
        self, db: Session, *, stock_id: int, period: str = "1y", interval: str = "1d"
    ) -> List[ChartDataPoint]:
        """
        Get chart data for a stock.
        """
        # In a real app, fetch from database or external API
        # For demo, generate random chart data
        from datetime import datetime, timedelta
        
        # Determine number of data points based on period and interval
        days = {
            "1d": 1,
            "1w": 7,
            "1m": 30,
            "3m": 90,
            "6m": 180,
            "1y": 365,
            "5y": 1825
        }.get(period, 365)
        
        # For demo, we'll just use days as data points regardless of interval
        # In a real implementation, you'd account for the interval too
        data_points = min(days, 100)  # Cap at 100 points for demo
        
        # Generate mock chart data
        end_date = datetime.now()
        
        # Start with a base price between $50 and $1000
        base_price = random.uniform(50, 1000)
        
        chart_data = []
        for i in range(data_points):
            # Go backwards in time from now
            point_date = end_date - timedelta(days=days * (data_points - i) / data_points)
            # Add some random movement to the price
            price = base_price * (1 + 0.02 * random.uniform(-1, 1) * (i / data_points))
            # Ensure price doesn't go negative
            price = max(price, 1.0)
            
            chart_data.append(ChartDataPoint(
                date=point_date.strftime("%Y-%m-%d"),
                price=round(price, 2)
            ))
            
            # Update base price for next iteration
            base_price = price
        
        return chart_data
    
    def get_top_gainers(self, db: Session, *, limit: int = 5) -> List[Stock]:
        """
        Get top gaining stocks.
        """
        # In a real app, fetch from database ordered by change_percent
        # For demo, generate random top gainers
        stocks = db.query(self.model).filter(
            self.model.is_positive == True
        ).order_by(desc(self.model.change_percent)).limit(limit).all()
        
        # If no results in DB, generate mock data
        if not stocks:
            mock_symbols = ['TSLA', 'NVDA', 'AMD', 'PLTR', 'COIN']
            mock_names = ['Tesla, Inc.', 'NVIDIA Corporation', 'Advanced Micro Devices, Inc.',
                         'Palantir Technologies Inc.', 'Coinbase Global, Inc.']
            
            mock_stocks = []
            for i, (symbol, name) in enumerate(zip(mock_symbols, mock_names)):
                stock = Stock(
                    id=i+1,
                    symbol=symbol,
                    name=name,
                    current_price=round(random.uniform(50, 500), 2),
                    change_percent=round(random.uniform(2, 10), 2),  # Always positive for gainers
                    is_positive=True,
                    currency="USD"
                )
                mock_stocks.append(stock)
            
            return mock_stocks[:limit]
            
        return stocks
    
    def get_top_losers(self, db: Session, *, limit: int = 5) -> List[Stock]:
        """
        Get top losing stocks.
        """
        # In a real app, fetch from database ordered by change_percent
        # For demo, generate random top losers
        stocks = db.query(self.model).filter(
            self.model.is_positive == False
        ).order_by(self.model.change_percent).limit(limit).all()
        
        # If no results in DB, generate mock data
        if not stocks:
            mock_symbols = ['GME', 'AMC', 'BABA', 'NIO', 'HOOD']
            mock_names = ['GameStop Corp.', 'AMC Entertainment Holdings', 'Alibaba Group Holding Ltd.',
                         'NIO Inc.', 'Robinhood Markets, Inc.']
            
            mock_stocks = []
            for i, (symbol, name) in enumerate(zip(mock_symbols, mock_names)):
                stock = Stock(
                    id=i+1,
                    symbol=symbol,
                    name=name,
                    current_price=round(random.uniform(20, 200), 2),
                    change_percent=round(random.uniform(-10, -2), 2),  # Always negative for losers
                    is_positive=False,
                    currency="USD"
                )
                mock_stocks.append(stock)
            
            return mock_stocks[:limit]
            
        return stocks
    
    def get_most_active(self, db: Session, *, limit: int = 5) -> List[Stock]:
        """
        Get most active stocks (by volume).
        """
        # In a real app, fetch from database ordered by volume
        # For demo, generate random most active
        stocks = db.query(self.model).order_by(desc(self.model.volume)).limit(limit).all()
        
        # If no results in DB, generate mock data
        if not stocks:
            mock_symbols = ['AAPL', 'MSFT', 'TSLA', 'AMZN', 'GOOGL']
            mock_names = ['Apple Inc.', 'Microsoft Corporation', 'Tesla, Inc.',
                         'Amazon.com Inc.', 'Alphabet Inc.']
            
            mock_stocks = []
            for i, (symbol, name) in enumerate(zip(mock_symbols, mock_names)):
                change = round(random.uniform(-5, 5), 2)
                stock = Stock(
                    id=i+1,
                    symbol=symbol,
                    name=name,
                    current_price=round(random.uniform(100, 3000), 2),
                    change_percent=change,
                    is_positive=change > 0,
                    currency="USD",
                    volume=random.randint(5000000, 100000000)
                )
                mock_stocks.append(stock)
            
            # Sort by volume (for demonstration)
            mock_stocks.sort(key=lambda x: x.volume, reverse=True)
            
            return mock_stocks[:limit]
            
        return stocks
    
    def _create_mock_stock(self, symbol: str) -> Stock:
        """
        Create a mock stock for demonstration purposes.
        """
        # Map common symbols to company names for a better demo
        symbol_name_map = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation', 
            'GOOGL': 'Alphabet Inc.', 
            'GOOG': 'Alphabet Inc.', 
            'AMZN': 'Amazon.com Inc.', 
            'TSLA': 'Tesla, Inc.',
            'FB': 'Meta Platforms, Inc.',
            'META': 'Meta Platforms, Inc.',
            'NVDA': 'NVIDIA Corporation',
            'NFLX': 'Netflix, Inc.'
        }
        
        name = symbol_name_map.get(symbol.upper(), f"{symbol.upper()} Corporation")
        
        # Generate a plausible price based on the first letter of the symbol
        # (just for demo variety)
        price_base = ord(symbol[0].upper()) - 64  # A=1, B=2, etc.
        price = round(price_base * random.uniform(5, 20), 2)
        
        # Random change percentage
        change = round(random.uniform(-5, 5), 2)
        
        # Create the mock stock
        stock = Stock(
            id=random.randint(1000, 9999),
            symbol=symbol.upper(),
            name=name,
            current_price=price,
            change_percent=change,
            is_positive=change > 0,
            currency="USD",
            market_cap=price * random.randint(10000000, 10000000000),
            volume=random.randint(1000000, 100000000),
            avg_volume=random.randint(1000000, 100000000),
            pe_ratio=round(random.uniform(10, 40), 2),
            dividend_yield=round(random.uniform(0, 3), 2),
            high_52w=price * (1 + random.uniform(0.1, 0.5)),
            low_52w=price * (1 - random.uniform(0.1, 0.5)),
            high=price * (1 + random.uniform(0.01, 0.05)),
            low=price * (1 - random.uniform(0.01, 0.05)),
            open=price * (1 - random.uniform(-0.02, 0.02)),
            previous_close=price * (1 - random.uniform(-0.02, 0.02)),
        )
        
        return stock


stock = CRUDStock(Stock) 