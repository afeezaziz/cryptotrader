from config import ccxt, os

# Initialize Bybit with futures as the default type
kraken = ccxt.kraken({
    'apiKey': os.getenv('KRAKEN_API_KEY'),
    'secret': os.getenv('KRAKEN_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})