from config import ccxt, os

# Initialize Bybit with futures as the default type
bybit = ccxt.bybit({
    'apiKey': os.getenv('BYBIT_API_KEY'),
    'secret': os.getenv('BYBIT_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})