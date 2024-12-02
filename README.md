# 💻 Binance Trading Bot Project

## 📖 Table of Contents
- [✨ Overview](#-overview)
- [📂 Directory Structure](#-directory-structure)
- [📥 Installation](#-installation)
- [⚙️ Configuration Files](#️-configuration-files)
  - [🛠️ settings.json](#️-settingsjson)
  - [📊 indicators.json](#-indicatorsjson)
  - [📜 trading_plan.json](#-trading_planjson)
- [📈 Technical Indicators](#-technical-indicators)
- [🚀 Running the Bot](#-running-the-bot)
- [🐳 Docker Support](#-docker-support)
- [🔄 Pre-Trade and Post-Trade Actions](#-pre-trade-and-post-trade-actions)
- [🧪 Testing](#-testing)
- [📝 Logging](#-logging)
- [⚠️ Disclaimer](#️-disclaimer)
- [📜 License](#-license)

---

## ✨ Overview
The **Binance Trading Bot** is designed to interact with Binance's API to conduct **automated trading** of cryptocurrency pairs. Equipped with **technical indicators**, the bot makes informed decisions about buying and selling, aiming to maximize profits while managing risk effectively.

---

## 📂 Directory Structure
```plaintext
binance_trading_bot/
├── trading_bot.py        # Main bot logic
├── settings.json         # JSON settings file for bot configuration
├── Dockerfile            # Docker configuration
├── e2e_test.py           # End-to-end testing with mock data
├── utils.py              # Utility functions
├── data/
│   └── XRP_11_24_data.csv  # Historical XRP/USDT data
├── indicators.json       # Technical indicators configuration
├── trading_plan.json     # User-defined trading plans for execution
├── README.md             # Comprehensive project documentation
├── pre_trade.py          # Pre-trade actions including setup and analysis
├── post_trade.py         # Post-trade actions including updating indicators and logging
```

---

## 📥 Installation
1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/binance_trading_bot.git
   cd binance_trading_bot
   ```

2. **Install required Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up configuration files**:
   - Edit `settings.json`, `indicators.json`, and `trading_plan.json` as needed.

4. **Start the bot**:
   ```bash
   python trading_bot.py
   ```

---

## ⚙️ Configuration Files

### 🛠️ settings.json
Stores configuration settings for the bot, including:
- Binance API Key and Secret
- Data paths
- Currency pairs
- Trade limits
- Log paths

### 📊 indicators.json
Defines the technical indicators and their parameters. This file helps the bot make informed buy/sell decisions.

### 📜 trading_plan.json
Contains user-defined trading plans, including session start and end times.

---

## 📈 Technical Indicators
The bot uses the following technical indicators to determine optimal trading points:

1. **📉 Moving Average Crossover**: Identifies trends by comparing short-term and long-term moving averages. Effective in trending markets.
2. **📊 Relative Strength Index (RSI)**: Highlights overbought/oversold conditions for market entry/exit points.
3. **📈 Bollinger Bands**: Tracks market volatility and identifies reversal opportunities in volatile markets.
4. **📊 MACD**: Highlights momentum and crossover signals for trend identification.
5. **📏 Support/Resistance Levels**: Identifies critical price levels where reversals or breakouts are likely.

---

## 🚀 Running the Bot
1. **Ensure configuration files are properly set up**.
2. **Run the bot**:
   ```bash
   python trading_bot.py
   ```

3. **Automated tests** (`e2e_test.py`) will validate configurations before trading begins.

---

## 🐳 Docker Support
Run the bot in an isolated Docker container for easy deployment:
1. **Build the Docker image**:
   ```bash
   docker build -t binance_trading_bot .
   ```

2. **Run the container**:
   ```bash
   docker run -d binance_trading_bot
   ```

---

## 🔄 Pre-Trade and Post-Trade Actions
- **Pre-Trade Actions (pre_trade.py)**:
  - Sets up necessary analyses before trading, such as selecting the best indicator.
- **Post-Trade Actions (post_trade.py)**:
  - Updates indicator usage and logs important information after each trade.

---

## 🧪 Testing
Run end-to-end tests with mock data to ensure everything is functioning correctly:
```bash
python -m unittest e2e_test.py
```

---

## 📝 Logging
Logs are saved in the path specified in `settings.json`. They include:
- Detailed trade records
- Selected indicators
- Any errors encountered during execution

---

## ⚠️ Disclaimer
This bot is for **educational purposes only**. Use it at your own risk. Cryptocurrency trading involves significant risk, and losses can occur.

---

## 📜 License
This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.
