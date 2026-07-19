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


    # ---------------------------------------
    # Calibrated Confidence
    # ---------------------------------------
    #
    # The "confidence" a signal reports at prediction time (from
    # BlueprintEngine) is a raw heatmap/frequency score - NOT a
    # measured win probability. This looks back at every past
    # prediction made with a similar raw confidence and returns the
    # REAL win rate those predictions achieved.
    #
    # Until there are enough completed predictions in that bucket
    # (min_samples), the number isn't trustworthy yet, so this falls
    # back to the raw confidence and flags it as uncalibrated rather
    # than pretending to have a real answer too early.

    def get_calibrated_confidence(

        self,

        raw_confidence,

        min_samples=30

    ):

        stats = self.db.get_winrate_by_confidence_bucket(

            raw_confidence

        )

        calibrated = stats["sample_size"] >= min_samples

        if calibrated:

            value = stats["winrate"]

        else:

            value = raw_confidence

        return {

            "value": value,
            "calibrated": calibrated,
            "sample_size": stats["sample_size"],
            "bucket": stats["bucket"],
            "raw_confidence": raw_confidence,
            "min_samples": min_samples

        }
