import sqlite3


class LearningEngine:

    def __init__(self):

        self.db = "ticks.db"

        self.create_tables()


    def create_tables(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            market TEXT,

            predicted_digit INTEGER,

            blueprint_score REAL,

            confidence REAL,

            signal TEXT,

            duration INTEGER,

            actual_digit INTEGER,

            correct INTEGER

        )
        """)

        conn.commit()

        conn.close()


    def save_prediction(

        self,

        market,

        predicted_digit,

        blueprint_score,

        confidence,

        signal,

        duration

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute(

            """
            INSERT INTO predictions (

                market,

                predicted_digit,

                blueprint_score,

                confidence,

                signal,

                duration,

                actual_digit,

                correct

            )

            VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)

            """,

            (

                market,

                predicted_digit,

                blueprint_score,

                confidence,

                signal,

                duration

            )

        )

        conn.commit()

        conn.close()
