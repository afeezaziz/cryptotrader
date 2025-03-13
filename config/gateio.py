from config import ccxt, os

# Initialize Bybit with futures as the default type
gateio = ccxt.gateio({
    'apiKey': os.getenv('GATEIO_API_KEY'),
    'secret': os.getenv('GATEIO_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})