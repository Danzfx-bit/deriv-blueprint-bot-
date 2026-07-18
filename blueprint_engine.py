from frequency_engine import FrequencyEngine
from momentum_engine import MomentumEngine
from transition_engine import TransitionEngine
from confidence_engine import ConfidenceEngine


class BlueprintEngine:

    def __init__(self):

        self.frequency_engine = FrequencyEngine()

        self.momentum_engine = MomentumEngine()

        self.transition_engine = TransitionEngine()

        self.confidence_engine = ConfidenceEngine()


    def analyze(self, history):


        # -----------------------------------
        # Minimum history requirement
        # -----------------------------------

        if len(history) < 50:

            return {

                "signal": "WAIT",

                "number": "-",

                "target_digit": "-",

                "blueprint_score": 0,

                "confidence": 0,

                "duration": 1,

                "ranking": [],

                "details": {}

            }


        # -----------------------------------
        # Run Analysis Engines
        # -----------------------------------

        frequency_scores = self.frequency_engine.analyze(

            history

        )


        momentum_scores = self.momentum_engine.analyze(

            history

        )


        transition_scores = self.transition_engine.analyze(

            history

        )


        # -----------------------------------
        # Combine Blueprint Scores
        # -----------------------------------

        blueprint_scores = {}


        for digit in range(10):


            frequency = frequency_scores.get(

                digit, {}

            ).get(

                "score",

                0

            )


            momentum = momentum_scores.get(

                digit, {}

            ).get(

                "score",

                0

            )


            transition = transition_scores.get(

                digit, {}

            ).get(

                "score",

                0

            )


            total = round(

                frequency +

                momentum +

                transition,

                2

            )


            blueprint_scores[digit] = {

                "frequency": frequency,

                "momentum": momentum,

                "transition": transition,

                "blueprint_score": total

            }


        # -----------------------------------
        # Rank Digits
        # -----------------------------------

        ranking = sorted(

            blueprint_scores.items(),

            key=lambda x:

            x[1]["blueprint_score"],

            reverse=True

        )


        best_digit = ranking[0][0]


        best_score = ranking[0][1]["blueprint_score"]


        # -----------------------------------
        # New Historical Confidence
        # -----------------------------------

        confidence_result = self.confidence_engine.analyze(

            blueprint_score=best_score,

            predicted_digit=best_digit,

            engine_scores=blueprint_scores

        )


        confidence = confidence_result["confidence"]


        # -----------------------------------
        # Signal Decision
        # -----------------------------------

        if confidence >= 80:

            signal = "STRONG MATCH"


        elif confidence >= 60:

            signal = "MATCH"


        elif confidence >= 40:

            signal = "WATCH"


        else:

            signal = "WAIT"



        # -----------------------------------
        # Final Ranking
        # -----------------------------------

        final_ranking = []


        for digit, values in ranking:

            final_ranking.append(

                (

                    digit,

                    round(

                        values["blueprint_score"],

                        2

                    )

                )

            )


        # -----------------------------------
        # Details
        # -----------------------------------

        details = {

            "frequency": frequency_scores,

            "momentum": momentum_scores,

            "transition": transition_scores,

            "blueprint": blueprint_scores,

            "confidence": confidence_result

        }



        return {


            "signal": signal,


            "number": best_digit,


            "target_digit": best_digit,


            "blueprint_score": round(

                best_score,

                2

            ),


            "confidence": round(

                confidence,

                2

            ),


            "duration": 1,


            "ranking": final_ranking,


            "details": details

        }
