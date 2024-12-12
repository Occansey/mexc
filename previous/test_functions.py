from ccxt import mexc
from time import sleep,ctime,time

api_key='mx0vglurK0t3QdCbl8'####VERY BAD PRACTICE
secret_key='fa42de6ef1e144deabac8de7cd60cfc0' ###VERY BAD PRACTICE
symbols=['COW/USDT','GRASS/USDT','SMILE/USDT','MOODENG/USDT','VISTA/USDT','X/USDT','SUI/USDT','POPCAT/USDT']
mexc_exchange=mexc({
    'apiKey': api_key,
    'secret': secret_key,
})

def calculate_parameters(symbol,wished_amount):
    coef=1.01
    symbol_price= mexc_exchange.fetch_ticker(symbol)['last']
    size= wished_amount/symbol_price
    take_profit= symbol_price*coef
    return size, take_profit

def test_symbols(symbols):
    "The goal is to test which symbols work with the mexc API on spot Trading"
    symbols=['GME/USDT','METIS/USDT','HMSTR/USDT','SXCH/USDT','STRUMP/USDT','MOODENG/USDT','X/USDT','GRASS/USDT']

# Print available markets
    for symbol in symbols:
        try:
            size, take_profit=calculate_parameters(symbol, 10)
            order= mexc_exchange.create_market_buy_order(symbol, size)
        except Exception as e:
            print(symbol,e)
            continue
def fetch():
    balances=mexc_exchange.fetch_balance()
    print(balances)

# fetch()
# analysis={'info': {'makerCommission': None, 'takerCommission': None, 'buyerCommission': None, 'sellerCommission': None, 'canTrade': True, 'canWithdraw': True, 'canDeposit': True, 'updateTime': None, 'accountType': 'SPOT', 'balances': [{'asset': 'USDT', 'free': '0.261482845177852', 'locked': '0'}, {'asset': 'VISTA', 'free': '0', 'locked': '0.07'}, {'asset': 'BOB', 'free': '1099190.420000000056502951', 'locked': '0'}, {'asset': 'GSTOP', 'free': '10967.88', 'locked': '0'}, {'asset': 'RCG', 'free': '2806.42', 'locked': '0'}, {'asset': 'TX20', 'free': '196.22', 'locked': '0'}, {'asset': 'MEMEAI', 'free': '0.003917305', 'locked': '0'}], 'permissions': ['SPOT']}, 'USDT': {'free': 0.261482845177852, 'used': 0.0, 'total': 0.261482845177852}, 'VISTA': {'free': 0.0, 'used': 0.07, 'total': 0.07}, 'BOB': {'free': 1099190.4200000002, 'used': 0.0, 'total': 1099190.4200000002}, 'GSTOP': {'free': 10967.88, 'used': 0.0, 'total': 10967.88}, 'RCG': {'free': 2806.42, 'used': 0.0, 'total': 2806.42}, 'TX20': {'free': 196.22, 'used': 0.0, 'total': 196.22}, 'MEMEAI': {'free': 0.003917305, 'used': 0.0, 'total': 0.003917305}, 'free': {'USDT': 0.261482845177852, 'VISTA': 0.0, 'BOB': 1099190.4200000002, 'GSTOP': 10967.88, 'RCG': 2806.42, 'TX20': 196.22, 'MEMEAI': 0.003917305}, 'used': {'USDT': 0.0, 'VISTA': 0.07, 'BOB': 0.0, 'GSTOP': 0.0, 'RCG': 0.0, 'TX20': 0.0, 'MEMEAI': 0.0}, 'total': {'USDT': 0.261482845177852, 'VISTA': 0.07, 'BOB': 1099190.4200000002, 'GSTOP': 10967.88, 'RCG': 2806.42, 'TX20': 196.22, 'MEMEAI': 0.003917305}}
# print(analysis['VISTA']['used'])
# print('GRASS/USDT'.split("/")[0])
test_symbols(symbols)
