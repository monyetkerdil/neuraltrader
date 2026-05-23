"""
NeuralTrader - AI-Powered Trading System
Main engine coordinating 6 specialized agents.
"""

__version__ = "1.0.0"

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("neuraltrader")


class Signal(Enum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell"
    STRONG_SELL = "strong_sell"


class AssetType(Enum):
    STOCK = "stock"
    CRYPTO = "crypto"
    FOREX = "forex"
    COMMODITY = "commodity"


@dataclass
class Trade:
    id: str
    symbol: str
    side: str  # buy/sell
    price: float
    quantity: float
    timestamp: datetime
    strategy: str
    pnl: float = 0.0
    status: str = "open"


@dataclass
class MarketData:
    symbol: str
    price: float
    volume: float
    change_24h: float
    high_24h: float
    low_24h: float
    timestamp: datetime


@dataclass
class SignalResult:
    symbol: str
    signal: Signal
    confidence: float
    strategy: str
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward: float


class NeuralTraderEngine:
    """Core trading engine coordinating all agents."""
    
    def __init__(self):
        self.agents: Dict[str, 'BaseAgent'] = {}
        self.trades: List[Trade] = []
        self.signals: List[SignalResult] = []
        self.running = False
        self.portfolio_value = 100000.0
        self.positions: Dict[str, float] = {}
    
    def register_agent(self, name: str, agent: 'BaseAgent'):
        self.agents[name] = agent
        logger.info(f"Agent registered: {name}")
    
    async def start(self, agents: Optional[List[str]] = None):
        self.running = True
        targets = agents or list(self.agents.keys())
        tasks = [self._run_agent(name) for name in targets if name in self.agents]
        await asyncio.gather(*tasks)
    
    async def _run_agent(self, name: str):
        agent = self.agents[name]
        try:
            await agent.run()
        except Exception as e:
            logger.error(f"Agent {name} error: {e}")
    
    async def stop(self):
        self.running = False
    
    def add_trade(self, trade: Trade):
        self.trades.append(trade)
    
    def get_performance(self) -> Dict[str, Any]:
        winning = [t for t in self.trades if t.pnl > 0]
        losing = [t for t in self.trades if t.pnl < 0]
        total_pnl = sum(t.pnl for t in self.trades)
        
        return {
            "total_trades": len(self.trades),
            "winning_trades": len(winning),
            "losing_trades": len(losing),
            "win_rate": len(winning) / len(self.trades) if self.trades else 0,
            "total_pnl": total_pnl,
            "portfolio_value": self.portfolio_value,
            "positions": self.positions
        }


class BaseAgent:
    def __init__(self, name: str, engine: NeuralTraderEngine):
        self.name = name
        self.engine = engine
    
    async def run(self):
        while self.engine.running:
            await self.process()
            await asyncio.sleep(1)
    
    async def process(self):
        raise NotImplementedError


__all__ = ["NeuralTraderEngine", "BaseAgent", "Trade", "Signal", "SignalResult", "MarketData"]
