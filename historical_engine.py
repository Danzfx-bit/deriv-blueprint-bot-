from prediction_database import PredictionDatabase


class HistoricalEngine:

    def __init__(self):

        self.db = PredictionDatabase()


    # ---------------------------------------
    # Overall Accuracy
    # ---------------------------------------

    def get_overall_accuracy(self):

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
    # Accuracy By Digit
    # ---------------------------------------

    def get_digit_accuracy(

        self,

        digit

    ):

        predictions = self.db.get_predictions_by_digit(

            digit

        )


        completed = [

            p for p in predictions

            if p[11] is not None

        ]


        if len(completed) == 0:

            return 0


        correct = 0


        for prediction in completed:

            if prediction[11] == 1:

                correct += 1


        return round(

            (correct / len(completed)) * 100,

            2

        )


    # ---------------------------------------
    # Recent Accuracy
    # ---------------------------------------

    def get_recent_accuracy(

        self,

        limit=100

    ):

        predictions = self.db.get_recent_predictions(

            limit

        )


        completed = [

            p for p in predictions

            if p[11] is not None

        ]


        if len(completed) == 0:

            return 0


        correct = 0


        for prediction in completed:

            if prediction[11] == 1:

                correct += 1


        return round(

            (correct / len(completed)) * 100,

            2

        )


    # ---------------------------------------
    # Confidence Performance
    # ---------------------------------------

    def get_confidence_accuracy(

        self,

        minimum_confidence=0

    ):

        predictions = self.db.get_completed_predictions()


        filtered = [

            p for p in predictions

            if p[7] >= minimum_confidence

        ]


        if len(filtered) == 0:

            return 0


        correct = 0


        for prediction in filtered:

            if prediction[11] == 1:

                correct += 1


        return round(

            (correct / len(filtered)) * 100,

            2

        )


    # ---------------------------------------
    # Full Historical Report
    # ---------------------------------------

    def analyze(self):

        return {

            "overall_accuracy":

                self.get_overall_accuracy(),


            "recent_accuracy":

                self.get_recent_accuracy(),


            "confidence_accuracy":

                self.get_confidence_accuracy()

        }
