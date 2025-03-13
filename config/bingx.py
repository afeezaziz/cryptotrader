from config import ccxt, os

# Initialize Bybit with futures as the default type
bingx = ccxt.bingx({
    'apiKey': os.getenv('BINGX_API_KEY'),
    'secret': os.getenv('BINGX_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})