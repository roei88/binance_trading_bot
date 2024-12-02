import unittest
from unittest.mock import Mock
import pandas as pd
from trading_bot import TradingBot

class TestTradingBot(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        # Load historical data from the CSV file
        self.historical_data = pd.read_csv('data/XRP_11_24_data.csv', sep=';')
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
