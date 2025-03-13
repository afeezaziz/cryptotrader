from config.binance import binance
from config.bingx import bingx
from config.bitfinex import bitfinex
from config.bitget import bitget
from config.bitmex import bitmex
from config.bybit import bybit
from config.gateio import gateio
from config.htx import htx
from config.kraken import kraken
from config.mexc import mexc

def getOrderBook(exchange, symbol):

    # Fetch the order book based on the exchange
    if exchange == 'binance':
        order_book = binance.fetch_order_book(symbol)
    elif exchange == 'bingx':
        order_book = bingx.fetch_order_book(symbol)     
    elif exchange == 'bitfinex':
        order_book = bitfinex.fetch_order_book(symbol)   
    elif exchange == 'bitget':
        order_book = bitget.fetch_order_book(symbol)                      
    elif exchange == 'bitmex':
        order_book = bitmex.fetch_order_book(symbol)
    elif exchange == 'bybit':
        order_book = bybit.fetch_order_book(symbol)   
    elif exchange == 'gateio':
        order_book = gateio.fetch_order_book(symbol)  
    elif exchange == 'htx':
        order_book = htx.fetch_order_book(symbol)                      
    elif exchange == 'kraken':
        order_book = kraken.fetch_order_book(symbol)
    elif exchange == 'mexc':
        order_book = mexc.fetch_order_book(symbol)        
    else:
        raise ValueError(f"Unsupported exchange: {exchange}")

    # Print the order book (for demonstration - it's usually a large dictionary)
    # print(order_book)

    # Access bids (buy orders) and asks (sell orders)
    bids = order_book['bids']
    asks = order_book['asks']

    # Print the best bid and ask
    print(f"Best Bid: {bids[0]}")  # [price, quantity]
    print(f"Best Ask: {asks[0]}")   # [price, quantity]

    # Example: Accessing the first few bids and asks
    print("--- Bids (Buy Orders) ---")
    for bid in bids:
        price, quantity = bid
        print(f"Price: {price}, Quantity: {quantity}")

    print("\n--- Asks (Sell Orders) ---")
    for ask in asks:
        price, quantity = ask
        print(f"Price: {price}, Quantity: {quantity}")

    # Example: calculate the mid price
    mid_price = (bids[0][0] + asks[0][0]) / 2
    print(f"\nMid Price: {mid_price}")    



