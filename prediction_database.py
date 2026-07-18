import sqlite3
import os
from datetime import datetime


DB_FOLDER = "data"
DB_FILE = "data/predictions.db"


class PredictionDatabase:

    def __init__(self):

        os.makedirs(DB_FOLDER, exist_ok=True)

        self.db = DB_FILE

        self.create_table()

    # ---------------------------------------
    # Create Predictions Table
    # ---------------------------------------

    def create_table(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            market TEXT,

            predicted_digit INTEGER,

            frequency_score REAL,

            momentum_score REAL,

            transition_score REAL,

            confidence REAL,

            signal TEXT,

            duration INTEGER,

            actual_digit INTEGER,

            correct INTEGER

        )

        """)

        conn.commit()

        conn.close()

    # ---------------------------------------
    # Save Prediction
    # ---------------------------------------

    def save_prediction(

        self,

        market,

        predicted_digit,

        frequency_score,

        momentum_score,

        transition_score,

        confidence,

        signal,

        duration

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute(

            """

            INSERT INTO predictions (

                timestamp,

                market,

                predicted_digit,

                frequency_score,

                momentum_score,

                transition_score,

                confidence,

                signal,

                duration,

                actual_digit,

                correct

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)

            """,

            (

                datetime.utcnow().isoformat(),

                market,

                predicted_digit,

                frequency_score,

                momentum_score,

                transition_score,

                confidence,

                signal,

                duration

            )

        )

        conn.commit()

        conn.close()

    # ---------------------------------------
    # Validate Oldest Pending Prediction
    # ---------------------------------------

    def validate_prediction(

        self,

        actual_digit

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT

                id,

                predicted_digit

            FROM predictions

            WHERE actual_digit IS NULL

            ORDER BY id ASC

            LIMIT 1

        """)

        row = cursor.fetchone()

        if row is None:

            conn.close()

            return

        prediction_id = row[0]

        predicted = row[1]

        correct = int(

            predicted == actual_digit

        )

        cursor.execute(

            """

            UPDATE predictions

            SET

                actual_digit=?,

                correct=?

            WHERE id=?

            """,

            (

                actual_digit,

                correct,

                prediction_id

            )

        )

        conn.commit()

        conn.close()

    # ---------------------------------------
    # Load All Predictions
    # ---------------------------------------

    def load_predictions(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM predictions

            ORDER BY id DESC

        """)

        rows = cursor.fetchall()

        conn.close()

        return rows
