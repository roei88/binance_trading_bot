from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
import logging

# Directory structure for the web UI
# binance_trading_bot/
# └── web_ui/
#     └── app.py  # Main web UI logic
#     └── templates/
#         └── index.html  # HTML Template

app = Flask(__name__)
app.secret_key = 'supersecretkey'

SETTINGS_FILE = '../settings.json'
TRADING_PLAN_FILE = '../trading_plan.json'
INDICATORS_FILE = '../indicators.json'
LOG_FILE = '../logs/trading_bot.log'

# Load JSON file
def load_json(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

# Save JSON file
def save_json(filepath, data):
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

# Home route
@app.route('/')
def index():
    settings = load_json(SETTINGS_FILE)
    trading_plan = load_json(TRADING_PLAN_FILE)
    indicators = load_json(INDICATORS_FILE)
    logs = []
    try:
        with open(LOG_FILE, 'r') as file:
            logs = file.readlines()[-50:]
    except FileNotFoundError:
        logs = ["No log file found."]
    return render_template('index.html', settings=settings, trading_plan=trading_plan, indicators=indicators, logs=logs)

# Update settings
@app.route('/update_settings', methods=['POST'])
def update_settings():
    settings = request.form.to_dict()
    try:
        save_json(SETTINGS_FILE, settings)
        flash("Settings updated successfully.", "success")
    except Exception as e:
        flash(f"Error updating settings: {e}", "danger")
    return redirect(url_for('index'))

# Update trading plan
@app.route('/update_trading_plan', methods=['POST'])
def update_trading_plan():
    trading_plan = request.form.to_dict()
    try:
        save_json(TRADING_PLAN_FILE, trading_plan)
        flash("Trading plan updated successfully.", "success")
    except Exception as e:
        flash(f"Error updating trading plan: {e}", "danger")
    return redirect(url_for('index'))

# Manage trades (Start/Stop Trading)
@app.route('/manage_trading', methods=['POST'])
def manage_trading():
    action = request.form['action']
    if action == 'start':
        flash("Trading started successfully.", "success")
    elif action == 'stop':
        flash("Trading stopped successfully.", "success")
    else:
        flash("Invalid trading action.", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
