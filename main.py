"""
NeuralTrader - Main Application
"""

import asyncio
import argparse
import logging
from datetime import datetime

from core import NeuralTraderEngine
from agents import (
    AnalystAgent, SentimentAgent, StrategyAgent,
    RiskAgent, ExecutionAgent, PortfolioAgent
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
logger = logging.getLogger("neuraltrader")


class NeuralTrader:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.engine = NeuralTraderEngine()
        self._setup_agents()
    
    def _setup_agents(self):
        self.engine.register_agent("analyst", AnalystAgent(self.engine, self.config.get("analyst", {})))
        self.engine.register_agent("sentiment", SentimentAgent(self.engine, self.config.get("sentiment", {})))
        self.engine.register_agent("strategy", StrategyAgent(self.engine, self.config.get("strategy", {})))
        self.engine.register_agent("risk", RiskAgent(self.engine, self.config.get("risk", {})))
        self.engine.register_agent("execution", ExecutionAgent(self.engine, self.config.get("execution", {})))
        self.engine.register_agent("portfolio", PortfolioAgent(self.engine, self.config.get("portfolio", {})))
    
    async def start(self, agents: list = None):
        logger.info("=" * 60)
        logger.info("NeuralTrader - AI-Powered Trading System")
        logger.info("=" * 60)
        await self.engine.start(agents)
    
    async def stop(self):
        await self.engine.stop()
    
    def performance(self):
        return self.engine.get_performance()


async def main():
    parser = argparse.ArgumentParser(description="NeuralTrader")
    parser.add_argument("action", choices=["start", "backtest", "status"])
    parser.add_argument("--strategy", default="adaptive")
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--risk", default="medium")
    
    args = parser.parse_args()
    trader = NeuralTrader()
    
    if args.action == "start":
        try:
            await trader.start()
        except KeyboardInterrupt:
            pass
        finally:
            await trader.stop()
    elif args.action == "status":
        import json
        print(json.dumps(trader.performance(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
