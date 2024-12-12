import ccxt,time
from dotenv import load_dotenv
from os import getenv 

class FuturesTrader:
    def __init__(self, api_key, secret_key):
        self.exchange = ccxt.mexc({
            'apiKey': api_key,
            'secret': secret_key,
            'options': {
                'defaultType': 'future',  # Use the futures market
            },
            'enableRateLimit': True,
        })
        self.exchange.load_markets()
        print('INIT DONE')

    def get_balance(self, currency="USDT"):
        """Fetch futures account balance for a specific currency."""
        balance = self.exchange.fetch_balance({'type': 'future'})
        return balance['total'].get(currency, 0)

    def create_market_order(self, symbol, side, amount, leverage=1):
        """Place a market order."""
        self.exchange.set_leverage(leverage, symbol,{'openType': 1, 'positionType': 2})  # Set leverage for the symbol
        return self.exchange.create_order(symbol, 'market', side, amount)

    def create_limit_order(self, symbol, side, amount, price, leverage=1):
        """Place a limit order."""
        self.exchange.set_leverage(leverage, symbol)
        return self.exchange.create_order(symbol, 'limit', side, amount, price, params={'type': 'future'})

    def fetch_open_positions(self):
        """Fetch open positions."""
        return self.exchange.fetch_positions()

    def close_position(self, symbol, side, amount):
        """Close a position by placing an opposite market order."""
        return self.exchange.create_order(symbol, 'market', side, amount, params={'type': 'future'})

    def monitor_positions(self):
        """Monitor and print all open positions."""
        positions = self.fetch_open_positions()
        for position in positions:
            if position['contracts'] > 0:  # Only show active positions
                print(f"Symbol: {position['symbol']}, Amount: {position['contracts']}, PnL: {position['unrealizedPnl']}")
    def fetch_markets(self):
        with open("future_markets.txt",'a') as file:
            file.write(str(self.exchange.load_markets()))
def main():
    print('INIT')
    load_dotenv()
    api_key=getenv("API_KEY")
    secret_key=getenv("SECRET_KEY")
    trader = FuturesTrader(api_key, secret_key)
    symbol = "MEMEFI/USDT:USDT"
    leverage = 22  # Example leverage
    order_amount = 100  # Example order size

    # Get current balance
    # usdt_balance = trader.get_balance()
    # print(f"USDT Balance: {usdt_balance}")

    # Place a market buy order
    print(f"Placing a market buy order for {symbol}...")
    buy_order = trader.create_market_order(symbol, 'sell', order_amount, leverage)
    print("Buy Order: rather sell", buy_order)

    # Monitor open positions
    print("\nMonitoring open positions...")
    trader.monitor_positions()

    take_profit_price = float(buy_order['price']) * 1.02  # Example: 2% profit target
    print(f"\nPlacing a limit sell order at {take_profit_price} for {symbol}...")
    limit_sell_order = trader.create_limit_order(symbol, 'buy', order_amount, take_profit_price, leverage)
    print("Limit Sell Order:", limit_sell_order)

    # Close the position if needed (example)
    time.sleep(10)  # Simulate waiting for some time
    print("\nClosing the position...")
    close_order = trader.close_position(symbol, 'sell', order_amount)
    print("Close Order:", close_order)
    print('END')

if __name__ == "__main__":
    main()
