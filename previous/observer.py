from ccxt import mexc,RequestTimeout
from time import ctime,sleep
from os import getenv
from dotenv import load_dotenv
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

def check_prices(symbols):
    "Check if the average profit is over x% if it is the sell orders are triggered"
    selected_symbols={}
    max=0
    low=0
    for symbol in symbols:
        selected_symbols[symbol]=mexc_exchange.fetch_ticker(symbol)['last']

    while True :
        sum_profit=0
        for symbol in selected_symbols:
            sum_profit+=check_profit(symbol,selected_symbols[symbol])
        average_profit=sum_profit/len(selected_symbols)
        if average_profit>max: max=average_profit
        if average_profit<low: low=average_profit
        print(f'{ctime()} - AVG ETF PRICE: {average_profit}% max:{max}% low:{low}')
        sleep(2)


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
    
def main():
    symbols = ['PNUT/USDT','SOL/USDT','PEAQ/USDT','GRASS/USDT','SMILE/USDT','MEW/USDT','HMSTR/USDT','DRIFT/USDT',  'X/USDT', 'MOODENG/USDT', 'VISTA/USDT' , 'SUI/USDT', 'POPCAT/USDT']
    check_prices(symbols)
    
main()