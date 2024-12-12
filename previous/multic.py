from ccxt import mexc,RequestTimeout
from time import ctime,time,sleep
from os import getenv
from dotenv import load_dotenv
import random
load_dotenv()

api_key=getenv("API_KEY")
secret_key=getenv("SECRET_KEY")
mexc_exchange = mexc({
    'apiKey': api_key,
    'secret': secret_key,
    'enableRateLimit': True,
    'options': {
        'recvWindow': 10000  # Increased recvWindow for better timing tolerance
    },
})


def buy_order(symbol,amount):
    "Buy order of the symbol according to the amount"
    # Place the initial buy order
    usdt_balance=mexc_exchange.amount_to_precision(symbol, amount)
    mexc_exchange.create_market_buy_order(symbol,None,{'quoteOrderQty':usdt_balance})
    symbol_price = mexc_exchange.fetch_ticker(symbol)['last']
    print(f'BOUGHT {symbol} AT {symbol_price}')
    return symbol_price


def check_profit(symbol,buy_price):
    "Check the percentage profit of a symbol"
    for _ in range(10):
        try:
            current_price = mexc_exchange.fetch_ticker(symbol)['last']
            break
        except RequestTimeout as e:
            sleep(1)
    profit=current_price-buy_price
    percentage_profit=profit/buy_price*100
    return percentage_profit


def check_selling(selected_symbols):
    "Check if the average profit is over x% if it is the sell orders are triggered"
    sum_profit=0
    for symbol in selected_symbols: sum_profit+=check_profit(symbol,selected_symbols[symbol])
    average_profit=sum_profit/len(selected_symbols)
    if time()%60<1:print(f'{ctime()} - AVG ETF PRICE: {average_profit}%')
    return sell_all(selected_symbols) if average_profit> 0.45 else False

def sell_all(selected_symbols):
    for symbol in selected_symbols:
        mexc_exchange.create_market_sell_order(symbol, mexc_exchange.fetch_balance()[symbol.split("/")[0]]['free'])
        print(f'SOLD {symbol}')
    return True
        
def calculate_profit(initial_investment):
    balance = mexc_exchange.fetch_balance()['free']['USDT']
    profit = balance - initial_investment
    percentage_profit=profit/initial_investment*100
    print(f'OVERALL PROFIT: {profit} ~ {percentage_profit}%')

def trade_n_crypto(nb_currencies):
    """""This bot aims to trade on <nb_currencies> different cryptocurrencies and sell the moment the overall profit reaches 5%"""
    symbols = ['MEMESAI/USDT','PIPPIN/USDT','PEAQ/USDT','PNUT/USDT','GRASS/USDT','SMILE/USDT','SXCH/USDT','MEW/USDT','HMSTR/USDT','STRUMP/USDT','DRIFT/USDT',  'X/USDT', 'MOODENG/USDT', 'VISTA/USDT' , 'SUI/USDT', 'POPCAT/USDT']
    initial_investment = mexc_exchange.fetch_balance()['free']['USDT']
    step=0
    while True:
        dic_symbols={}
        selected_symbols=symbols[:nb_currencies]
        random.shuffle(symbols)
        bal=mexc_exchange.fetch_balance()['free']['USDT']
        for symbol in selected_symbols:
            buy_price=buy_order(symbol,bal/nb_currencies)
            dic_symbols[symbol]=buy_price
        while True:
            if check_selling(dic_symbols):
                step+=1
                calculate_profit(initial_investment)
                print(f'STEP : {step} ')
                break
            sleep(0.5)

trade_n_crypto(3)


def trade_x_percent():
    """""This function aims to check on an hourly price, and if there's a specific percetage increase within the hour, the bot should be triggered"""   
    # Get the price about an hour before 
    pass
