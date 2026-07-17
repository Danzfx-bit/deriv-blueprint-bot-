import sqlite3
import os
from datetime import datetime


DB_FOLDER = "data"
DB_FILE = "data/ticks.db"


def create_database():

    os.makedirs(DB_FOLDER, exist_ok=True)

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            market TEXT,
            price REAL,
            digit INTEGER
        )
    """)

    conn.commit()
    conn.close()


def save_tick(market, price, digit):

    create_database()

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO ticks (
            timestamp,
            market,
            price,
            digit
        )
        VALUES (?, ?, ?, ?)
    """, (
        datetime.utcnow().isoformat(),
        market,
        float(price),
        int(digit)
    ))

    conn.commit()

    conn.close()


def load_ticks(market=None, limit=1000):

    create_database()

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    if market:

        cursor.execute("""
            SELECT digit
            FROM ticks
            WHERE market = ?
            ORDER BY id DESC
            LIMIT ?
        """, (
            market,
            limit
        ))

    else:

        cursor.execute("""
            SELECT digit
            FROM ticks
            ORDER BY id DESC
            LIMIT ?
        """, (
            limit,
        ))


    rows = cursor.fetchall()

    conn.close()


    # Reverse so oldest → newest
    digits = [
        row[0]
        for row in reversed(rows)
    ]

    return digits


def get_tick_count(market=None):

    create_database()

    conn = sqlite3.connect(DB_FILE)

    cursor = conn.cursor()


    if market:

        cursor.execute("""
            SELECT COUNT(*)
            FROM ticks
            WHERE market = ?
        """, (
            market,
        ))

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM ticks
        """)


    count = cursor.fetchone()[0]

    conn.close()

    return count
