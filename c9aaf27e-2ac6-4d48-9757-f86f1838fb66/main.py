from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the assets to trade
        self.tickers = ["AAPL"]

    @property
    def interval(self):
        # Set the data fetch interval
        return "1day"

    @property
    def assets(self):
        # Return the assets list
        return self.tickers

    def run(self, data):
        # Implement the strategy logic
        short_term_sma = SMA(self.tickers[0], data["ohlcv"], 10)  # 10-day SMA
        long_term_sma = SMA(self.tickers[0], data["ohlcv"], 30)  # 30-day SMA
        
        # Check if we have enough data points
        if short_term_sma is None or long_term_sma is None or len(short_term_sma) < 2:
            return TargetAllocation({self.tickers[0]: 0})
        
        # Buy signal (short SMA crosses above long SMA)
        if short_term_sma[-2] < long_term_sma[-2] and short_term_sma[-1] > long_term_sma[-1]:
            log("Buy signal detected.")
            allocation = 1.0  # 100% allocation
        # Sell signal (short SMA crosses below long SMA)
        elif short_term_sma[-2] > long_term_sma[-2] and short_term_sma[-1] < long_term_sma[-1]:
            log("Sell signal detected. Exiting position.")
            allocation = 0.0  # 0% allocation, exit position
        else:
            # Hold current position if no crossover
            log("No crossover detected. Holding position.")
            allocation = None  # Assign None to indicate no change in allocation

        # Define the target allocation
        if allocation is not None:
            return TargetAllocation({self.tickers[0]: allocation})
        else:
            return TargetAllocation({})  # Return an empty allocation if holding position