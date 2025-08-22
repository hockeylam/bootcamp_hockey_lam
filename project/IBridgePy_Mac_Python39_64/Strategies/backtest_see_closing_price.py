from datetime import datetime
import numpy as np

def initialize(context):
    context.symbol = 'SPY'
    context.short_window = 20
    context.long_window = 50
    context.order_flag = False

def handle_data(context, data):
    # Approx. 3 years of trading days = ~756
    hist = data.history(context.symbol, 'close', context.long_window + 1, '1d')

    if len(hist) < context.long_window:
        return

    short_ma = np.mean(hist[-context.short_window:])
    long_ma = np.mean(hist[-context.long_window:])
    current_price = data.current(context.symbol, 'close')

    # Log the latest close price
    log.info(f"{context.symbol} latest close: {current_price:.2f}")
    log.info(f"Short MA: {short_ma:.2f}, Long MA: {long_ma:.2f}")

    # === Strategy Logic ===
    if short_ma > long_ma and not context.order_flag:
        order(context.symbol, 100)  # Buy signal
        context.order_flag = True
        log.info(f"BUY {context.symbol} at {current_price:.2f}")

    elif short_ma < long_ma and context.order_flag:
        order(context.symbol, -100)  # Sell signal
        context.order_flag = False
        log.info(f"SELL {context.symbol} at {current_price:.2f}")
