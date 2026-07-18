from prediction_database import PredictionDatabase


class LearningEngine:

    def __init__(self):

        self.db = PredictionDatabase()

    # ----------------------------------------
    # Save New Prediction
    # ----------------------------------------

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

        self.db.save_prediction(

            market=market,

            predicted_digit=predicted_digit,

            frequency_score=frequency_score,

            momentum_score=momentum_score,

            transition_score=transition_score,

            confidence=confidence,

            signal=signal,

            duration=duration

        )

    # ----------------------------------------
    # Validate Prediction
    # ----------------------------------------

    def validate_prediction(

        self,

        actual_digit

    ):

        self.db.validate_prediction(

            actual_digit

        )

    # ----------------------------------------
    # Prediction Statistics
    # ----------------------------------------

    def get_total_predictions(self):

        predictions = self.db.load_predictions()

        return len(predictions)

    def get_correct_predictions(self):

        predictions = self.db.load_predictions()

        wins = 0

        for row in predictions:

            if row[11] == 1:

                wins += 1

        return wins

    def get_wrong_predictions(self):

        predictions = self.db.load_predictions()

        losses = 0

        for row in predictions:

            if row[11] == 0:

                losses += 1

        return losses

    def get_accuracy(self):

        total = self.get_total_predictions()

        if total == 0:

            return 0

        wins = self.get_correct_predictions()

        return round(

            wins / total * 100,

            2

        )

    # ----------------------------------------
    # Future AI Training
    # ----------------------------------------

    def train(self):

        """
        Placeholder.

        Future versions of NUTEC will use this
        method to learn from historical data.

        Planned features:

        - Pattern learning
        - Market clustering
        - Confidence calibration
        - Adaptive weighting
        """

        pass
