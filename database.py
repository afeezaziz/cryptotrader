import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager

# Database file path
DB_PATH = os.environ.get('DB_PATH', 'trader.db')

# Maximum age of transaction records to keep (in days)
MAX_RECORD_AGE_DAYS = int(os.environ.get('MAX_RECORD_AGE_DAYS', 30))

def init_db():
    """Initialize the database with required tables."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Create transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            exchange TEXT NOT NULL,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            price REAL NOT NULL,
            amount REAL NOT NULL,
            total REAL NOT NULL,
            status TEXT NOT NULL
        )
        ''')
        
        # Create index on timestamp for faster purging queries
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp)')
        
        conn.commit()

@contextmanager
def get_db_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
    finally:
        conn.close()

def add_transaction(transaction_data):
    """Add a new transaction to the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO transactions 
        (timestamp, exchange, symbol, side, price, amount, total, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction_data['timestamp'],
            transaction_data['exchange'],
            transaction_data['symbol'],
            transaction_data['side'],
            transaction_data['price'],
            transaction_data['amount'],
            transaction_data['total'],
            transaction_data['status']
        ))
        conn.commit()
        return cursor.lastrowid

def get_all_transactions():
    """Get all transactions from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions ORDER BY timestamp DESC')
        return [dict(row) for row in cursor.fetchall()]

def get_recent_transactions(limit=5):
    """Get the most recent transactions."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transactions ORDER BY timestamp DESC LIMIT ?', (limit,))
        return [dict(row) for row in cursor.fetchall()]

def purge_old_transactions():
    """Delete transactions older than MAX_RECORD_AGE_DAYS."""
    cutoff_date = (datetime.now() - timedelta(days=MAX_RECORD_AGE_DAYS)).strftime('%Y-%m-%d %H:%M:%S')
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE timestamp < ?', (cutoff_date,))
        deleted_count = cursor.rowcount
        conn.commit()
        
        # Vacuum the database to reclaim space
        conn.execute('VACUUM')
        
        return deleted_count

def get_transaction_stats():
    """Get statistics about transactions."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) as count FROM transactions')
        total_count = cursor.fetchone()['count']
        
        # Get unique exchanges
        cursor.execute('SELECT COUNT(DISTINCT exchange) as count FROM transactions')
        exchange_count = cursor.fetchone()['count']
        
        # Get buy/sell counts
        cursor.execute('SELECT COUNT(*) as count FROM transactions WHERE side = "buy"')
        buy_count = cursor.fetchone()['count']
        
        cursor.execute('SELECT COUNT(*) as count FROM transactions WHERE side = "sell"')
        sell_count = cursor.fetchone()['count']
        
        # Get volume by exchange
        cursor.execute('''
        SELECT exchange, 
               SUM(CASE WHEN side = 'buy' THEN total ELSE 0 END) as buy_volume,
               SUM(CASE WHEN side = 'sell' THEN total ELSE 0 END) as sell_volume
        FROM transactions
        GROUP BY exchange
        ''')
        volume_by_exchange = [dict(row) for row in cursor.fetchall()]
        
        return {
            'total_count': total_count,
            'exchange_count': exchange_count,
            'buy_count': buy_count,
            'sell_count': sell_count,
            'volume_by_exchange': volume_by_exchange
        }

# Initialize the database when this module is imported
init_db()
