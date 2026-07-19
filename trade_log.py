import sqlite3
import os
from datetime import datetime, timezone


DB_FOLDER = "data"
DB_FILE = "data/trades.db"


def create_database():

    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            market TEXT,
            digit INTEGER,
            stake REAL,
            success INTEGER,
            contract_id TEXT,
            buy_price REAL,
            payout REAL,
            error TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_trade(market, digit, stake, result):

    create_database()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trades (
            timestamp, market, digit, stake, success,
            contract_id, buy_price, payout, error
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now(timezone.utc).isoformat(),
        market,
        digit,
        stake,
        1 if result.get("success") else 0,
        str(result.get("contract_id", "") or ""),
        result.get("buy_price"),
        result.get("payout"),
        result.get("error"),
    ))

    conn.commit()
    conn.close()


def get_recent_trades(limit=20):

    create_database()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp, market, digit, stake,
            success, contract_id, buy_price, payout, error
        FROM trades
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_todays_trade_count():

    create_database()

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    today_start = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    ).isoformat()

    cursor.execute("""
        SELECT COUNT(*)
        FROM trades
        WHERE timestamp >= ?
        AND success = 1
    """, (today_start,))

    count = cursor.fetchone()[0]
    conn.close()

    return count
