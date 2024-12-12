import os
from dotenv import load_dotenv
import ccxt
import time

# Load environment variables
load_dotenv()

def setup_mexc_client():
    """Initialize MEXC client using CCXT with contract trading settings"""
    exchange = ccxt.mexc({
        'apiKey': os.getenv('MEXC_API_KEY'),
        'secret': os.getenv('MEXC_SECRET_KEY'),
        'options': {
            'defaultType': 'swap',
            'defaultSubType': 'linear',
            'fetchMarkets': True
        },
        'urls': {
            'api': {
                'contract': 'https://contract.mexc.com',
                'private': 'https://contract.mexc.com'
            }
        }
    })
    return exchange

def get_contract_symbol(base_symbol):
    """Convert regular symbol to contract symbol format"""
    return f"{base_symbol}_USDT"

def place_leveraged_trade(symbol, usdt_amount, leverage=2, take_profit_percentage=2.0):
    """Place a leveraged long position with a take-profit order"""
    try:
        # Initialize client
        exchange = setup_mexc_client()
        
        # Convert symbol to contract format
        contract_symbol = get_contract_symbol(symbol.split('/')[0])
        print(f"Using contract symbol: {contract_symbol}")
        
        # Test API connection
        try:
            print('try balance')
            balance = exchange.fetch_balance({'type': 'future'})['total'].get(symbol, 0)
            print("Successfully connected to API")
        except Exception as e:
            print(f"Balance fetch error: {str(e)}")
            return None
        
        # Set leverage
        try:
            exchange.set_leverage(leverage, contract_symbol)
            print(f"Leverage set to {leverage}x")
        except Exception as e:
            print(f"Leverage setting error: {str(e)}")
            return None

        # Get current market price
        try:
            ticker = exchange.fetch_ticker(contract_symbol)
            entry_price = ticker['last']
            print(f"Current price: {entry_price}")
        except Exception as e:
            print(f"Price fetch error: {str(e)}")
            return None
        
        # Calculate position size (quantity)
        quantity = (usdt_amount * leverage) / entry_price
        
        # Calculate take-profit price
        take_profit_price = entry_price * (1 + (take_profit_percentage / 100))
        
        print(f"Attempting to place market buy order for {quantity} contracts...")
        
        # Place market buy order
        try:
            entry_order = exchange.create_market_order(
                symbol=contract_symbol,
                side='buy',
                amount=quantity,
                params={
                    'reduceOnly': False,
                    'positionSide': 'LONG'
                }
            )
            print("Entry order placed successfully")
        except Exception as e:
            print(f"Entry order error: {str(e)}")
            return None

        # Add small delay
        time.sleep(2)
        
        # Place take-profit limit sell order
        try:
            tp_order = exchange.create_limit_order(
                symbol=contract_symbol,
                side='sell',
                amount=quantity,
                price=take_profit_price,
                params={
                    'reduceOnly': True,
                    'timeInForce': 'GTC',
                    'positionSide': 'LONG'
                }
            )
            print("Take-profit order placed successfully")
        except Exception as e:
            print(f"Take-profit order error: {str(e)}")
            # Consider closing the position if TP order fails
            return None

        return {
            "entry_order": entry_order,
            "take_profit_order": tp_order,
            "entry_price": entry_price,
            "take_profit_price": float(take_profit_price),
            "quantity": float(quantity)
        }
        
    except ccxt.BaseError as e:
        print(f"CCXT Error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    # Trading parameters
    SYMBOL = "BTC/USDT"  # Will be converted to BTC_USDT
    USDT_AMOUNT = 0.0028  # Starting with a small amount for testing
    LEVERAGE = 2
    TAKE_PROFIT_PERCENTAGE = 2.0
    
    print("Starting trading bot...")
    print(f"Trading {SYMBOL} with {LEVERAGE}x leverage")
    print(f"Amount: {USDT_AMOUNT} USDT")
    print(f"Take profit: {TAKE_PROFIT_PERCENTAGE}%")
    
    # Execute the trade
    trade_result = place_leveraged_trade(
        symbol=SYMBOL,
        usdt_amount=USDT_AMOUNT,
        leverage=LEVERAGE,
        take_profit_percentage=TAKE_PROFIT_PERCENTAGE
    )
    
    if trade_result:
        print("\nTrade executed successfully!")
        print(f"Entry Price: {trade_result['entry_price']}")
        print(f"Take Profit Price: {trade_result['take_profit_price']}")
        print(f"Position Size: {trade_result['quantity']}")