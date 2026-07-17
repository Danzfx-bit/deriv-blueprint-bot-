"""
==========================================================
NUTEC Blueprint Engine v2.0
Core Analysis Engine
==========================================================
"""

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

                "target_digit": "-",

                "blueprint_score": 0,

                "confidence": 0,

                "duration": 5,

                "ranking": [],

                "details": {}

            }

        # -----------------------------------
        # Run all engines
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

        confidence_result = self.confidence_engine.analyze(

            frequency_scores,

            momentum_scores,

            transition_scores

        )

        # -----------------------------------
        # Merge Blueprint Scores
        # -----------------------------------

        blueprint_scores = {}

        for digit in range(10):

            frequency = frequency_scores.get(
                digit,
                {}
            ).get(
                "score",
                0
            )

            momentum = momentum_scores.get(
                digit,
                {}
            ).get(
                "score",
                0
            )

            transition = transition_scores.get(
                digit,
                {}
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
        # Rank Blueprint Scores
        # -----------------------------------

        ranking = sorted(

            blueprint_scores.items(),

            key=lambda x: x[1]["blueprint_score"],

            reverse=True

        )

        best_digit = ranking[0][0]

        best_score = ranking[0][1]["blueprint_score"]

        confidence = confidence_result["confidence"]        # -----------------------------------
        # Determine Signal
        # -----------------------------------

        if best_score >= 55:

            signal = "STRONG MATCH"

        elif best_score >= 40:

            signal = "MATCH"

        elif best_score >= 25:

            signal = "WATCH"

        else:

            signal = "WAIT"

        # -----------------------------------
        # Convert Ranking
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
        # Build Engine Details
        # -----------------------------------

        details = {

            "frequency": frequency_scores,

            "momentum": momentum_scores,

            "transition": transition_scores,

            "confidence": confidence_result,

            "blueprint": blueprint_scores

        }

        # -----------------------------------
        # Final Output
        # -----------------------------------

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

            "duration": 5,

            "ranking": final_ranking,

            "details": details

        }
