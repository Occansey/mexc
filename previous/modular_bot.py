import os
from ccxt import mexc
from dotenv import load_dotenv
from time import sleep, time, ctime
from decimal import Decimal
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ExchangeAPI:
    def __init__(self, api_key, secret_key):
        self.exchange = mexc({
            'apiKey': api_key,
            'secret': secret_key,
            'enableRateLimit': True,
            'options': {'recvWindow': 10000},
        })

    def get_balance(self, currency="USDT"):
        return self.exchange.fetch_balance()['free'].get(currency, 0)

    def get_price(self, symbol):
        return self.exchange.fetch_ticker(symbol)['last']

    def create_market_buy_order(self, symbol, usdt_amount):
        usdt_amount = float(self.exchange.amount_to_precision(symbol, usdt_amount))
        params = {'quoteOrderQty': usdt_amount}
        try:
            return self.exchange.create_order(symbol, 'market', 'buy', None, None, params)
        except Exception as e:
            logging.error(f"Failed to create market buy order: {e}")
            return None

    def create_limit_sell_order(self, symbol, size, price):
        if size is None or price is None:
            raise ValueError("Size or price is None; ensure they are correctly calculated.")
        if not isinstance(size, (int, float)) or not isinstance(price, (int, float)):
            raise ValueError("Size and price must be numeric.")
        
        size = float(self.exchange.amount_to_precision(symbol, size))
        price = float(self.exchange.price_to_precision(symbol, price))
        
        try:
            return self.exchange.create_limit_sell_order(symbol, size, price)
        except Exception as e:
            logging.error(f"Failed to create limit sell order: {e}")
            return None

class TradeBot:
    def __init__(self, symbols, profit_margin=1.005):
        self.symbols = symbols
        self.profit_margin = profit_margin
        self.current_symbol_index = 0
        self.exchange_api = ExchangeAPI(
            api_key=os.getenv("API_KEY"),
            secret_key=os.getenv("SECRET_KEY")
        )

    def execute_trade_cycle(self):
        while True:
            symbol = self.symbols[self.current_symbol_index]
            usdt_balance = self.exchange_api.get_balance("USDT")
            logging.info(f"Buying {symbol} with full USDT balance of {usdt_balance}")

            buy_order = self.exchange_api.create_market_buy_order(symbol, usdt_balance)
            if buy_order is None or 'filled' not in buy_order:
                logging.warning(f"Buy order for {symbol} failed or was not filled, retrying in 10 seconds...")
                sleep(10)
                continue
            
            size = buy_order['filled']
            buy_price = self.exchange_api.get_price(symbol)

            if size is None or buy_price is None:
                logging.error("Failed to get valid size or buy price; skipping this cycle.")
                sleep(10)
                continue
            
            # Calculate take profit price
            take_profit_price = Decimal(str(buy_price)) * Decimal(str(self.profit_margin))

            logging.info(f"Setting take profit for {symbol} at {take_profit_price}")

            try:
                sell_order = self.exchange_api.create_limit_sell_order(symbol, size, float(take_profit_price))
            except ValueError as e:
                logging.error(f"Error creating sell order for {symbol}: {e}")
                sleep(10)
                continue

            while True:
                try:
                    order_status = self.exchange_api.exchange.fetch_order(sell_order['id'], symbol)
                except Exception as e:
                    logging.error(f"Error fetching order status: {e}")
                    sleep(5)
                    continue

                if order_status['status'] == 'closed':
                    balance = self.exchange_api.get_balance("USDT")
                    profit = balance - usdt_balance
                    logging.info(f"SOLD {symbol} at take profit. Profit: {profit} USDT")
                    
                    self.current_symbol_index = (self.current_symbol_index + 1) % len(self.symbols)
                    break

                if time() % 3000 < 1:
                    current_price = self.exchange_api.get_price(symbol)
                    balance = self.exchange_api.get_balance("USDT")
                    logging.info(f"BALANCE: {balance} USDT | {symbol} price: {current_price} | {ctime()}")

                sleep(0.2)

if __name__ == "__main__":
    symbols = ['GRASS/USDT', 'COW/USDT', 'SMILE/USDT', 'MOODENG/USDT', 'VISTA/USDT', 'X/USDT', 'SUI/USDT', 'POPCAT/USDT']
    trade_bot = TradeBot(symbols, profit_margin=1.005)
    trade_bot.execute_trade_cycle()
