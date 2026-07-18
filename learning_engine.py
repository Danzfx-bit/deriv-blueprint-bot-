from prediction_database import PredictionDatabase


class LearningEngine:

    def __init__(self):

        self.db = PredictionDatabase()


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


    # ---------------------------------------
    # Validate Prediction
    # ---------------------------------------

    def validate_prediction(

        self,

        actual_digit

    ):

        self.db.validate_prediction(

            actual_digit

        )


    # ---------------------------------------
    # Statistics
    # ---------------------------------------

    def get_total_predictions(self):

        return len(

            self.db.load_predictions()

        )


    def get_completed_predictions(self):

        return len(

            self.db.get_completed_predictions()

        )


    def get_accuracy(self):

        predictions = self.db.get_completed_predictions()


        if len(predictions) == 0:

            return 0


        correct = 0


        for prediction in predictions:

            if prediction[11] == 1:

                correct += 1


        return round(

            (correct / len(predictions)) * 100,

            2

        )
