from config import ccxt, os

# Initialize Bitmex with futures as the default type
bitmex = ccxt.bitmex({
    'apiKey': os.getenv('BITMEX_API_KEY'),
    'secret': os.getenv('BITMEX_API_SECRET'),
    'options': {
        'defaultType': 'future',  # Use futures market
    },
})