import os
from ccxt import mexc
from dotenv import load_dotenv
from time import sleep, time, ctime


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
        
        try:
            return self.exchange.create_limit_sell_order(symbol, size, price)
        except Exception as e:print(e)