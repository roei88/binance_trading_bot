# Dockerfile - Configuration for containerizing the bot
FROM python:3.9-slim

# Set working directory
WORKDIR /usr/src/app

# Copy all files to working directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run trading bot
CMD ["python", "trading_bot.py"]
