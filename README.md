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
