import unittest
from unittest.mock import Mock
from trading_bot import TradingBot
import pandas as pd

class TestTradingBot(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.historical_data = pd.DataFrame({
            'timeOpen': ['2024-11-30T00:00:00.000Z'],
            'timeClose': ['2024-11-30T23:59:59.999Z'],
            'open': [1.7967153281],
            'close': [1.9441209163]
        })
        self.indicators = {
            "Moving_Average_Crossover": {
                "usage_data": [{"date": "", "volume": 10, "profit": 100}]
            }
        }
        self.bot = TradingBot(self.mock_client, self.historical_data, self.indicators)

    def test_buy_function(self):
        # Mock response for buy function
        self.mock_client.order_market_buy.return_value = {"status": "FILLED"}
        self.bot.buy(1)
        self.mock_client.order_market_buy.assert_called_once_with(symbol=self.bot.TRADE_PAIR, quantity=1)

    def test_sell_function(self):
        # Mock response for sell function
        self.mock_client.order_market_sell.return_value = {"status": "FILLED"}
        self.bot.sell(1)
        self.mock_client.order_market_sell.assert_called_once_with(symbol=self.bot.TRADE_PAIR, quantity=1)

if __name__ == '__main__':
    unittest.main()
