# Binance Trading Bot

## Overview
The Binance Trading Bot is an automated Python-based bot that interacts with Binance API to execute trades on the XRP/USDT pair based on technical analysis and market indicators. The bot uses historical data and advanced algorithms to determine optimal trading times and manages trades automatically.

## Directory Structure
```
binance_trading_bot/
├── trading_bot.py        # Main bot logic
├── settings.json         # JSON settings file for bot configuration
├── Dockerfile            # Docker configuration
├── e2e_test.py           # End-to-end testing with mock data
├── utils.py              # Utility functions
├── data/
│   └── XRP_11_24_data.csv  # Historical XRP/USDT data
├── indicators.json       # Technical indicators configuration
└── README.md             # Project documentation
```

## Features
- **Automated Trading**: Uses Binance API to perform buy and sell orders.
- **Technical Analysis**: Implements trend analysis, such as Linear Regression and Moving Average Crossover.
- **Configurable**: Settings can be adjusted via `settings.json`.
- **Indicator Analysis**: Evaluates different indicators to determine the most suitable for trading.
- **Logging**: Logs all trading activities for debugging and analysis.

## Setup
### Prerequisites
- Python 3.9 or above
- Binance API Key and Secret
- Docker (optional, for containerization)

### Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/binance_trading_bot.git
   cd binance_trading_bot
   ```

2. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

3. **Set Up `settings.json`**:
   Edit the `settings.json` file to add your Binance API Key, Secret, and other configurations:
   ```json
   {
       "BINANCE_API_KEY": "YOUR_BINANCE_API_KEY",
       "BINANCE_API_SECRET": "YOUR_BINANCE_API_SECRET",
       "DATA_PATH": "data/XRP_11_24_data.csv",
       "BASE_CURRENCY": "XRP",
       "TARGET_CURRENCY": "USDT",
       "TRADE_LIMIT": { "total": 10, "daily": 10 },
       "TRADE_VALUE_CURRENCY": "USD",
       "TRADING_CYCLE_LIMIT": true,
       "TRADING_CYCLE_AMOUNT": 500,
       "LOG_PATH": "logs/trading_bot.log"
   }
   ```

### Running the Bot
1. **Run End-to-End Tests** (optional but recommended):
   ```sh
   python -m unittest e2e_test.py
   ```

2. **Run the Trading Bot**:
   ```sh
   python trading_bot.py
   ```

### Using Docker
1. **Build Docker Image**:
   ```sh
   docker build -t binance_trading_bot .
   ```

2. **Run Docker Container**:
   ```sh
   docker run -d binance_trading_bot
   ```

## Configuration
- **`settings.json`**: Contains all the configurable parameters including API keys, trade limits, logging paths, etc.
- **`indicators.json`**: Stores the information regarding different technical indicators used in analysis.

## Technical Indicators
- **Moving Average Crossover**: Identifies trends by comparing short and long-term averages.
- **Relative Strength Index (RSI)**: Signals overbought or oversold conditions.
- **Bollinger Bands**: Captures market volatility.
- **MACD**: Highlights momentum and crossover signals.

## Testing
The `e2e_test.py` script provides an end-to-end testing setup using mock data to validate the functionality of the trading bot. This helps ensure the bot performs correctly before connecting to a live trading environment.

## Logging
All trading activities, including buy/sell orders and errors, are logged to the file specified in `settings.json`. This ensures that the trading activities can be reviewed and analyzed.

## Disclaimer
This trading bot is for educational purposes only. Use it at your own risk. Trading cryptocurrencies involves significant risk, and you should not trade with money that you cannot afford to lose.

## License
This project is licensed under the MIT License.

## Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue to suggest improvements.
