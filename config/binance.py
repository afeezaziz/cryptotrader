from config import ccxt, os

# Initialize Binance with futures as the default type
binance = ccxt.binance({
    'apiKey': os.getenv('BINANCE_API_KEY'),
    'secret': os.getenv('BINANCE_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})