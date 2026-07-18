from historical_engine import HistoricalEngine


class ConfidenceEngine:

    def __init__(self):

        self.historical = HistoricalEngine()

        self.max_confidence = 100


    # ---------------------------------------
    # Calculate Confidence
    # ---------------------------------------

    def analyze(

        self,

        blueprint_score,

        predicted_digit,

        engine_scores=None

    ):


        # Historical performance

        overall_accuracy = (

            self.historical.get_overall_accuracy()

        )


        digit_accuracy = (

            self.historical.get_digit_accuracy(

                predicted_digit

            )

        )


        recent_accuracy = (

            self.historical.get_recent_accuracy(

                100

            )

        )


        # -----------------------------------
        # Confidence weighting
        # -----------------------------------

        confidence = (

            (overall_accuracy * 0.30)

            +

            (digit_accuracy * 0.40)

            +

            (recent_accuracy * 0.30)

        )


        # -----------------------------------
        # Small blueprint adjustment
        # -----------------------------------

        if blueprint_score >= 50:

            confidence += 5


        elif blueprint_score < 20:

            confidence -= 5


        confidence = max(

            confidence,

            0

        )


        confidence = min(

            confidence,

            self.max_confidence

        )


        return {

            "confidence": round(

                confidence,

                2

            ),

            "overall_accuracy": overall_accuracy,

            "digit_accuracy": digit_accuracy,

            "recent_accuracy": recent_accuracy,

            "predicted_digit": predicted_digit

        }
