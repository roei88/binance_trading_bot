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
# ├── trading_plan.json  # User-defined trading plans for execution
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

# Load trading plan configuration
with open('trading_plan.json') as f:
    trading_plan = json.load(f)

# Update trading plan to include active field and full date strings for start/end times
for session in trading_plan['sessions']:
    session['active'] = True  # Default to active
    session['start_time'] = datetime.now().strftime('%Y-%m-%d') + 'T' + session['start_time']
    session['end_time'] = datetime.now().strftime('%Y-%m-%d') + 'T' + session['end_time']

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
    def __init__(self, client, historical_data, indicators, trading_plan):
        self.total_traded = 0
        self.total_traded_today = 0
        self.client = client
        self.historical_data = historical_data
        self.indicators = indicators
        self.trading_plan = trading_plan
        self.buy_times = []
        self.sell_times = []
        self.best_indicator = None
        self.complementary_indicator = None

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

        # Iterate through indicators to determine the best one based on volume and profit
        for indicator_name, indicator_data in self.indicators.items():
            total_profit = sum(item['profit'] for item in indicator_data['usage_data'])
            total_volume = sum(item['volume'] for item in indicator_data['usage_data'])
            performance = total_profit / (total_volume + 1e-5)  # Avoid division by zero

            logger.info(f"Indicator: {indicator_name}, Performance: {performance}")
            if performance > best_performance:
                best_performance = performance
                best_indicator = indicator_name

        self.best_indicator = best_indicator
        self.complementary_indicator = self.indicators[best_indicator]['complementary']
        logger.info(f"Best indicator determined: {self.best_indicator} with complementary indicator: {self.complementary_indicator}")

    def update_indicator_usage(self, profit, volume):
        date_str = datetime.now().strftime("%Y-%m-%d")
        self.indicators[self.best_indicator]['usage_data'].append({
            "date": date_str,
            "volume": volume,
            "profit": profit
        })
        with open('indicators.json', 'w') as f:
            json.dump(self.indicators, f, indent=4)

    def execute_trading_plan(self):
        logger.info("Executing user-defined trading plan.")
        for session in self.trading_plan['sessions']:
            if not session.get('active', True):
                logger.info(f"Skipping inactive trading session: {session['session_name']}")
                continue
            
            logger.info(f"Starting trading session: {session['session_name']}")
            self.analyze_best_indicator()  # Determine the best indicator before trading
            logger.info(f"Using best indicator: {self.best_indicator} and complementary indicator: {self.complementary_indicator} for trading.")
            self.update_trade_times()  # Update trade times based on market trends
            
            session_start_time = session['start_time']
            session_end_time = session['end_time']
            daily_trade_reset_time = "00:00"  # Reset daily trade limit at midnight
            
            while True:
                current_time = datetime.now().strftime("%Y-%m-%dT%H:%M")
                if current_time == session_end_time:
                    logger.info(f"Ending trading session: {session['session_name']}")
                    break
                
                profit = 0
                volume = 0
                # Check if current time is a buy time, and ensure limits are not exceeded
                if current_time in self.buy_times:
                    if self.total_traded_today < TRADE_LIMIT_DAILY and self.total_traded < TRADE_LIMIT_TOTAL:
                        self.buy(TRADE_LIMIT_DAILY)
                        self.total_traded_today += TRADE_LIMIT_DAILY
                        self.total_traded += TRADE_LIMIT_DAILY
                        volume += TRADE_LIMIT_DAILY
                        profit += random.uniform(0.01, 0.05) * TRADE_LIMIT_DAILY  # Mock profit for illustration

                # Check if current time is a sell time, and ensure there are trades to sell
                elif current_time in self.sell_times:
                    if self.total_traded_today > 0:
                        self.sell(TRADE_LIMIT_DAILY)
                        self.total_traded_today -= TRADE_LIMIT_DAILY
                        volume += TRADE_LIMIT_DAILY
                        profit -= random.uniform(0.01, 0.05) * TRADE_LIMIT_DAILY  # Mock profit for illustration
                
                # Update usage data after trading action
                if volume > 0:
                    self.update_indicator_usage(profit, volume)

                time.sleep(60)  # Pause for one minute before the next iteration

                # Reset daily traded amount at the defined reset time
                if current_time == daily_trade_reset_time:
                    self.total_traded_today = 0

    def start_trading(self):
        logger.info("Starting trading bot.")
        self.execute_trading_plan()

if __name__ == "__main__":
    # Run tests before starting the bot
    logger.info("Running tests before starting the bot.")
    result = subprocess.run([sys.executable, '-m', 'unittest', 'e2e_test.py'], capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Tests failed. Output:\n" + result.stdout + result.stderr)
        sys.exit(1)
    else:
        logger.info("All tests passed successfully. Starting the trading bot.")

    bot = TradingBot(client, historical_data, indicators, trading_plan)
    bot.start_trading()
