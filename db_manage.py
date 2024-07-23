import sqlite3
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_name: str):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    memo TEXT PRIMARY KEY,
                    balance REAL
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    event_id TEXT PRIMARY KEY,
                    owner_id INTEGER,
                    volume INTEGER,
                    value REAL,
                    jetton_price REAL
                )
            ''')
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS withdrawals (
                    withdrawal_id INTEGER PRIMARY KEY,
                    owner_id INTEGER,
                    bank_card_number TEXT,
                    card_owner_name TEXT,
                    status BOOLEAN
                )
            ''')

    def add_user(self, memo: str, balance: float):
        with self.conn:
            self.conn.execute('INSERT INTO users (memo, balance) VALUES (?, ?)', (memo, balance))

    def get_user(self, memo: str) -> Optional[Tuple[str, float]]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE memo = ?', (memo,))
        return cursor.fetchone()

    def add_transaction(self, event_id: str, owner_id: int, volume: int, value: float, jetton_price: float):
        with self.conn:
            self.conn.execute('''
                INSERT INTO transactions (event_id, owner_id, volume, value, jetton_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (event_id, owner_id, volume, value, jetton_price))

    def get_transaction(self, event_id: str) -> Optional[Tuple[str, int, int, float, float]]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM transactions WHERE event_id = ?', (event_id,))
        return cursor.fetchone()

    def add_withdrawal(self, withdrawal_id: int, owner_id: int, bank_card_number: str, card_owner_name: str, status: bool):
        with self.conn:
            self.conn.execute('''
                INSERT INTO withdrawals (withdrawal_id, owner_id, bank_card_number, card_owner_name, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (withdrawal_id, owner_id, bank_card_number, card_owner_name, status))

    def get_withdrawal(self, withdrawal_id: int) -> Optional[Tuple[int, int, str, str, bool]]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM withdrawals WHERE withdrawal_id = ?', (withdrawal_id,))
        return cursor.fetchone()

    def update_user_balance(self, memo: str, new_balance: float):
        with self.conn:
            self.conn.execute('UPDATE users SET balance = ? WHERE memo = ?', (new_balance, memo))

    def update_withdrawal_status(self, withdrawal_id: int, new_status: bool):
        with self.conn:
            self.conn.execute('UPDATE withdrawals SET status = ? WHERE withdrawal_id = ?', (new_status, withdrawal_id))

    def delete_user(self, memo: str):
        with self.conn:
            self.conn.execute('DELETE FROM users WHERE memo = ?', (memo,))

    def delete_transaction(self, event_id: str):
        with self.conn:
            self.conn.execute('DELETE FROM transactions WHERE event_id = ?', (event_id,))

    def delete_withdrawal(self, withdrawal_id: int):
        with self.conn:
            self.conn.execute('DELETE FROM withdrawals WHERE withdrawal_id = ?', (withdrawal_id,))

    def close(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    db = DatabaseManager('my_database.db')
    db.add_user('user1', 100.0)
    db.add_transaction('event1', 1, 10, 200.0, 20.0)
    db.add_withdrawal(1, 1, '1234-5678-9101-1121', 'John Doe', True)
    print(db.get_user('user1'))
    print(db.get_transaction('event1'))
    print(db.get_withdrawal(1))
    db.update_user_balance('user1', 150.0)
    db.update_withdrawal_status(1, False)
    print(db.get_user('user1'))
    print(db.get_withdrawal(1))
    db.delete_user('user1')
    db.delete_transaction('event1')
    db.delete_withdrawal(1)
    db.close()
