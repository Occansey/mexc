from ccxt import mexc
from time import sleep,ctime,time
from os import getenv
from dotenv import load_dotenv

load_dotenv()

api_key=getenv("API_KEY")
secret_key=getenv("SECRET_KEY")
symbols=['GRASS/USDT','SMILE/USDT','MOODENG/USDT','VISTA/USDT','X/USDT','SUI/USDT','POPCAT/USDT','SWELL/USDT']
mexc_exchange = mexc({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
    'options': {
        'recvWindow': 10000  # Increased recvWindow for better timing tolerance
    },
})


def calculate_parameters(symbol):
    coef=1.0025 ##first profitable coef:1.005
    symbol_price= mexc_exchange.fetch_ticker(symbol)['last']
    symbol_balance=mexc_exchange.fetch_balance()[symbol.split("/")[0]]['free']
    take_profit= symbol_price*coef
    return symbol_balance,take_profit,symbol_price


def buy_and_sell_orders(symbol,amount):
    # Place the initial buy order
    usdt_balance=mexc_exchange.amount_to_precision(symbol, amount)
    buy_order = mexc_exchange.create_market_buy_order(symbol,None,{'quoteOrderQty':usdt_balance})
    symbol_balance, take_profit,symbol_price=calculate_parameters(symbol)
    print(f'BOUGHT {symbol} AT {symbol_price}')
    sell_order = mexc_exchange.create_limit_sell_order(symbol, symbol_balance, take_profit)
    print(f'SELL {symbol} AT {take_profit}')
    return sell_order

def calculate_profit(initial_investment):
    balance = mexc_exchange.fetch_balance()['free']['USDT']
    profit = balance - initial_investment
    percentage_profit=profit/initial_investment*100
    print(f'OVERALL PROFIT: {profit} ~ {percentage_profit}%')

def print_symbol_price(symbol):
    symbol_price = mexc_exchange.fetch_ticker(symbol)['last']
    print(f'{ctime()} {symbol} price: {symbol_price}$')

def execute_trade(symbols):
    initial_investment = mexc_exchange.fetch_balance()['free']['USDT']
    step = 0
    for _ in range(1000):
        symbol = symbols[step%len(symbols)]
        sell_order=buy_and_sell_orders(symbol,initial_investment)
        while True:
            try:
                order_status = mexc_exchange.fetch_order(sell_order['id'], symbol)
                if order_status['status'] == 'closed':
                    print(f'SOLD {symbol}')
                    calculate_profit(initial_investment)
                    step += 1
                    break
                if time() % 300 < 1: print_symbol_price(symbol)
                sleep(0.2)
            except Exception as e : print('error occured zer',e)




execute_trade(symbols)
