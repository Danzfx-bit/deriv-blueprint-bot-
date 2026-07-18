import sqlite3


class HistoricalEngine:

    def __init__(self):

        self.db = "ticks.db"

    # ----------------------------------
    # Overall Accuracy
    # ----------------------------------

    def get_overall_accuracy(self):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT
                COUNT(*),
                SUM(correct)

            FROM predictions

            WHERE correct IS NOT NULL

        """)

        total, wins = cursor.fetchone()

        conn.close()

        if total == 0:

            return 50.0

        if wins is None:

            wins = 0

        return round((wins / total) * 100, 2)

    # ----------------------------------
    # Digit Accuracy
    # ----------------------------------

    def get_digit_accuracy(self, digit):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT
                COUNT(*),
                SUM(correct)

            FROM predictions

            WHERE predicted_digit=?
            AND correct IS NOT NULL

        """, (digit,))

        total, wins = cursor.fetchone()

        conn.close()

        if total < 20:

            return self.get_overall_accuracy()

        if wins is None:

            wins = 0

        return round((wins / total) * 100, 2)

    # ----------------------------------
    # Market Accuracy
    # ----------------------------------

    def get_market_accuracy(self, market):

        conn = sqlite3.connect(self.db)

        cursor = conn.cursor()

        cursor.execute("""

            SELECT
                COUNT(*),
                SUM(correct)

            FROM predictions

            WHERE market=?
            AND correct IS NOT NULL

        """, (market,))

        total, wins = cursor.fetchone()

        conn.close()

        if total < 20:

            return self.get_overall_accuracy()

        if wins is None:

            wins = 0

        return round((wins / total) * 100, 2)

    # ----------------------------------
    # Combined Historical Probability
    # ----------------------------------

    def get_probability(

        self,

        digit,

        market

    ):

        overall = self.get_overall_accuracy()

        digit_accuracy = self.get_digit_accuracy(digit)

        market_accuracy = self.get_market_accuracy(market)

        probability = (

            overall * 0.40 +

            digit_accuracy * 0.30 +

            market_accuracy * 0.30

        )

        return round(probability, 2)
