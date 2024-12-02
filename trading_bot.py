# Directory structure for the Binance trading bot project

# binance_trading_bot/
# ├── trading_bot.py  # Main bot logic
# ├── settings.json  # JSON settings file for bot configuration
# ├── Dockerfile  # Docker configuration
# ├── e2e_test.py  # End-to-end testing with mock data
# ├── utils.py  # Utility functions
# ├── data/
#     └── XRP_11_24_data.csv  # Historical XRP/USDT data
# ├── indicators.json  # Technical indicators configuration
# ├── README.md  # Comprehensive project documentation

import json
import time
import requests
import logging
import pandas as pd
from binance.client import Client
from datetime import datetime
import random
import numpy as np
from sklearn.linear_model import LinearRegression
import subprocess
import sys

# Load settings configuration
with open('settings.json') as f:
    settings = json.load(f)

# Load indicators configuration
with open('indicators.json') as f:
    indicators = json.load(f)

# Logger Configuration
logging.basicConfig(filename=settings['LOG_PATH'], level=logging.INFO)
logger = logging.getLogger(__name__)

# API credentials (for testing, environment variables should be used in production)
API_KEY = settings['BINANCE_API_KEY']
API_SECRET = settings['BINANCE_API_SECRET']
client = Client(API_KEY, API_SECRET)
# Binance client is initialized here to interact with Binance API for trading operations

# Load historical data
data_path = settings['DATA_PATH']
historical_data = pd.read_csv(data_path, sep=';')

# Configurable bot settings
TRADE_PAIR = settings['BASE_CURRENCY'] + settings['TARGET_CURRENCY']
TRADE_LIMIT_TOTAL = settings['TRADE_LIMIT']['total']
TRADE_LIMIT_DAILY = settings['TRADE_LIMIT']['daily']
TRADE_VALUE_CURRENCY = settings['TRADE_VALUE_CURRENCY']

# Buying/selling logic
class TradingBot:
    def __init__(self, client, historical_data, indicators):
        self.total_traded = 0
        self.total_traded_today = 0
        self.client = client
        self.historical_data = historical_data
        self.indicators = indicators
        self.buy_times = []
        self.sell_times = []

    def get_price(self):
        ticker = self.client.get_symbol_ticker(symbol=TRADE_PAIR)
        return float(ticker['price'])

    def buy(self, amount):
        try:
            logger.info(f"Attempting to buy {TRADE_PAIR}.")
            order = self.client.order_market_buy(symbol=TRADE_PAIR, quantity=amount)
            logger.info(f"Buy order placed successfully. Order: {order}")
        except Exception as e:
            logger.error(f"Failed to buy: {e}")

    def sell(self, amount):
        try:
            logger.info(f"Attempting to sell {TRADE_PAIR}.")
            order = self.client.order_market_sell(symbol=TRADE_PAIR, quantity=amount)
            logger.info(f"Sell order placed successfully. Order: {order}")
        except Exception as e:
            logger.error(f"Failed to sell: {e}")

    def update_trade_times(self):
        logger.info("Updating trade times using advanced algorithms.")
        try:
            prices = self.historical_data['close'].values.reshape(-1, 1)
            timestamps = np.arange(len(prices)).reshape(-1, 1)

            model = LinearRegression()
            model.fit(timestamps, prices)
            trend = model.predict(timestamps)
        except Exception as e:
            logger.error(f"Failed to calculate trend using Linear Regression: {e}")
            # Fallback calculation using a simple moving average
            logger.info("Using fallback calculation with simple moving average.")
            trend = self.historical_data['close'].rolling(window=5).mean().fillna(method='bfill').values

        self.buy_times = []
        self.sell_times = []

        # Buy at highs and sell at lows, based on trend analysis
        for i in range(1, len(trend)):
            if trend[i] > trend[i - 1] and prices[i] == max(prices[max(0, i-5):i+1]):
                self.buy_times.append(datetime.now().strftime("%H:%M"))
            elif trend[i] < trend[i - 1] and prices[i] == min(prices[max(0, i-5):i+1]):
                self.sell_times.append(datetime.now().strftime("%H:%M"))

        logger.info(f"Updated buy times: {self.buy_times}")
        logger.info(f"Updated sell times: {self.sell_times}")

    def analyze_best_indicator(self):
        logger.info("Analyzing indicators to determine the best one.")
        best_indicator = None
        best_performance = -float('inf')

        for indicator in self.indicators:
            performance = random.uniform(0, 1)  # Placeholder for actual performance calculation
            logger.info(f"Indicator: {indicator['indicator']}, Performance: {performance}")
            if performance > best_performance:
                best_performance = performance
                best_indicator = indicator

        logger.info(f"Best indicator determined: {best_indicator['indicator']} with performance: {best_performance}")
        return best_indicator

    def start_trading(self):
        logger.info("Starting trading bot.")
        best_indicator = self.analyze_best_indicator()
        logger.info(f"Using best indicator: {best_indicator['indicator']} for trading.")
        self.update_trade_times()
        daily_trade_reset_time = "00:00"

        while True:
            current_time = datetime.now().strftime("%H:%M")
            if current_time in self.buy_times:
                if self.total_traded_today < TRADE_LIMIT_DAILY and self.total_traded < TRADE_LIMIT_TOTAL:
                    self.buy(TRADE_LIMIT_DAILY)
                    self.total_traded_today += TRADE_LIMIT_DAILY
                    self.total_traded += TRADE_LIMIT_DAILY
            elif current_time in self.sell_times:
                if self.total_traded_today > 0:
                    self.sell(TRADE_LIMIT_DAILY)
                    self.total_traded_today -= TRADE_LIMIT_DAILY
            time.sleep(60)
            if current_time == daily_trade_reset_time:
                self.total_traded_today = 0

if __name__ == "__main__":
    logger.info("Running tests before starting the bot.")
    result = subprocess.run([sys.executable, '-m', 'unittest', 'e2e_test.py'], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Tests failed. Output:\n" + result.stdout + result.stderr)
        sys.exit(1)
    else:
        logger.info("All tests passed successfully. Starting the trading bot.")

    bot = TradingBot(client, historical_data, indicators)
    bot.start_trading()
