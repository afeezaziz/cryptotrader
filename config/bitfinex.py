from config import ccxt, os

# Initialize Bybit with futures as the default type
bitfinex = ccxt.bitfinex({
    'apiKey': os.getenv('BITFINEX_API_KEY'),
    'secret': os.getenv('BITFINEX_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})