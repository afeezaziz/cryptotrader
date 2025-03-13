from config import ccxt, os

# Initialize Bybit with futures as the default type
mexc = ccxt.mexc({
    'apiKey': os.getenv('MEXC_API_KEY'),
    'secret': os.getenv('MEXC_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})