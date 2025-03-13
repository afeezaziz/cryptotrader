from config import ccxt, os

# Initialize Bybit with futures as the default type
htx = ccxt.htx({
    'apiKey': os.getenv('HTX_API_KEY'),
    'secret': os.getenv('HTX_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})