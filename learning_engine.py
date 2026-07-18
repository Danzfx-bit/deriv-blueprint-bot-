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

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL)

            """,

            (

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


    def validate_prediction(

        self,

        actual_digit

    ):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT

                id,

                predicted_digit

            FROM predictions

            WHERE actual_digit IS NULL

            ORDER BY id ASC

            LIMIT 1

            """

        )

        row = cursor.fetchone()

        if row is None:

            conn.close()

            return


        prediction_id = row[0]

        predicted_digit = row[1]

        correct = int(

            predicted_digit == actual_digit

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


    def get_accuracy(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT

                COUNT(*),

                SUM(correct)

            FROM predictions

            WHERE correct IS NOT NULL

            """

        )

        total, wins = cursor.fetchone()

        conn.close()

        if total == 0:

            return 0

        if wins is None:

            wins = 0

        return round(

            wins / total * 100,

            2

        )


    def get_total_predictions(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute(

            "SELECT COUNT(*) FROM predictions"

        )

        total = cursor.fetchone()[0]

        conn.close()

        return total


    def get_correct_predictions(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT COUNT(*)

            FROM predictions

            WHERE correct=1

            """

        )

        wins = cursor.fetchone()[0]

        conn.close()

        return wins


    def get_wrong_predictions(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute(

            """

            SELECT COUNT(*)

            FROM predictions

            WHERE correct=0

            """

        )

        losses = cursor.fetchone()[0]

        conn.close()

        return losses
