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

        predicted_digit = row[1]

        correct = int(predicted_digit == actual_digit)

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

    # ---------------------------------------
    # Completed Predictions
    # ---------------------------------------

    def get_completed_predictions(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM predictions

            WHERE correct IS NOT NULL

            ORDER BY id DESC

        """)

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ---------------------------------------
    # Pending Predictions
    # ---------------------------------------

    def get_pending_predictions(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM predictions

            WHERE correct IS NULL

            ORDER BY id ASC

        """)

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ---------------------------------------
    # Predictions By Digit
    # ---------------------------------------

    def get_predictions_by_digit(

        self,

        digit

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM predictions

            WHERE predicted_digit=?

            ORDER BY id DESC

        """, (digit,))

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ---------------------------------------
    # Recent Predictions
    # ---------------------------------------

    def get_recent_predictions(

        self,

        limit=100

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM predictions

            ORDER BY id DESC

            LIMIT ?

        """, (limit,))

        rows = cursor.fetchall()

        conn.close()

        return rows

    # ---------------------------------------
    # Predictions By Market
    # ---------------------------------------

    def get_predictions_by_market(

        self,

        market

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT *

            FROM predictions

            WHERE market=?

            ORDER BY id DESC

        """, (market,))

        rows = cursor.fetchall()

        conn.close()

        return rows
     # ---------------------------------------
    # Total Predictions
    # ---------------------------------------

    def get_total_predictions(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM predictions

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    # ---------------------------------------
    # Total Validated Predictions
    # ---------------------------------------

    def get_total_validated(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM predictions

            WHERE correct IS NOT NULL

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    # ---------------------------------------
    # Total Correct Predictions
    # ---------------------------------------

    def get_total_correct(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM predictions

            WHERE correct = 1

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    # ---------------------------------------
    # Total Incorrect Predictions
    # ---------------------------------------

    def get_total_incorrect(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT COUNT(*)

            FROM predictions

            WHERE correct = 0

        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


    # ---------------------------------------
    # Learning Accuracy
    # ---------------------------------------

    def get_accuracy(self):

        validated = self.get_total_validated()

        if validated == 0:

            return 0.0

        correct = self.get_total_correct()

        return round(

            (correct / validated) * 100,

            2

        )


    # ---------------------------------------
    # Learning Statistics
    # ---------------------------------------

    def get_learning_statistics(self):

        return {

            "stored": self.get_total_predictions(),

            "validated": self.get_total_validated(),

            "correct": self.get_total_correct(),

            "incorrect": self.get_total_incorrect(),

            "accuracy": self.get_accuracy()

        }
