from config import ccxt, os

# Initialize Bybit with futures as the default type
bitget = ccxt.bitget({
    'apiKey': os.getenv('BITGET_API_KEY'),
    'secret': os.getenv('BITGET_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})