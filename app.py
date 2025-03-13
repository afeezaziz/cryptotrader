from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from datetime import datetime
import threading
import time
from core.orderbook import getOrderBook
import database as db

app = Flask(__name__)

@app.context_processor
def inject_now():
    """Make the current date available to all templates."""
    return {'now': datetime.now()}

# Set up scheduled database purging
def purge_old_data():
    """Background thread to periodically purge old transaction data."""
    while True:
        # Sleep for a day (86400 seconds)
        time.sleep(86400)
        # Purge old transactions
        deleted_count = db.purge_old_transactions()
        print(f"Purged {deleted_count} old transactions from database")

# Start the purge thread if not in debug mode
if not os.environ.get('FLASK_DEBUG', 'False').lower() == 'true':
    purge_thread = threading.Thread(target=purge_old_data, daemon=True)
    purge_thread.start()

@app.route('/')
def index():
    """Home page showing available exchanges and symbols"""
    # Get list of supported exchanges from the orderbook module
    exchanges = ['binance', 'bingx', 'bitfinex', 'bitget', 'bitmex', 
                'bybit', 'gateio', 'htx', 'kraken', 'mexc']
    
    # Common trading pairs
    symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'SOL/USDT', 'BNB/USDT']
    
    # Get recent transactions
    recent_transactions = db.get_recent_transactions(5)
    
    return render_template('index.html', 
                          exchanges=exchanges, 
                          symbols=symbols,
                          transactions=recent_transactions)

@app.route('/orderbook', methods=['GET', 'POST'])
def orderbook():
    """View orderbook for a specific exchange and symbol"""
    if request.method == 'POST':
        exchange = request.form.get('exchange')
        symbol = request.form.get('symbol')
    else:
        exchange = request.args.get('exchange', 'binance')
        symbol = request.args.get('symbol', 'BTC/USDT')
    
    try:
        # Get orderbook data
        order_book = getOrderBook(exchange, symbol)
        
        # Extract data for the template
        bids = order_book['bids'][:10]  # Top 10 bids
        asks = order_book['asks'][:10]  # Top 10 asks
        mid_price = (bids[0][0] + asks[0][0]) / 2
        
        return render_template('orderbook.html', 
                              exchange=exchange, 
                              symbol=symbol,
                              bids=bids,
                              asks=asks,
                              mid_price=mid_price)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/simulate_trade', methods=['POST'])
def simulate_trade():
    """Simulate a trade and record it in the transaction history"""
    exchange = request.form.get('exchange')
    symbol = request.form.get('symbol')
    side = request.form.get('side')  # 'buy' or 'sell'
    price = float(request.form.get('price'))
    amount = float(request.form.get('amount'))
    
    # Create a transaction record
    transaction = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'exchange': exchange,
        'symbol': symbol,
        'side': side,
        'price': price,
        'amount': amount,
        'total': price * amount,
        'status': 'simulated'
    }
    
    # Add to database
    transaction_id = db.add_transaction(transaction)
    transaction['id'] = transaction_id
    
    return redirect(url_for('transaction_history'))

@app.route('/transactions')
def transaction_history():
    """View transaction history"""
    transactions = db.get_all_transactions()
    stats = db.get_transaction_stats()
    
    return render_template('transactions.html', 
                          transactions=transactions,
                          stats=stats)

@app.route('/api/orderbook/<exchange>/<path:symbol>')
def api_orderbook(exchange, symbol):
    """API endpoint to get orderbook data in JSON format"""
    try:
        # Replace slash in URL with actual slash for the symbol
        symbol = symbol.replace('_', '/')
        order_book = getOrderBook(exchange, symbol)
        return jsonify(order_book)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Use environment variables for configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5001))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)
