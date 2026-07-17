"""
==========================================================
NUTEC Blueprint Engine v2.0
Core Analysis Engine
==========================================================

This engine combines:

1. Frequency Engine
2. Momentum Engine
3. Transition Engine
4. Confidence Engine

Future versions will add:

- Pattern Engine
- Recency Engine
- AI Learning Engine

==========================================================
"""

from frequency_engine import FrequencyEngine
from momentum_engine import MomentumEngine
from transition_engine import TransitionEngine
from confidence_engine import ConfidenceEngine


class BlueprintEngine:

    def __init__(self):

        # Initialise all engines

        self.frequency_engine = FrequencyEngine()

        self.momentum_engine = MomentumEngine()

        self.transition_engine = TransitionEngine()

        self.confidence_engine = ConfidenceEngine()


    def analyze(self, history):

        """
        Main Blueprint Analysis Pipeline

        Input:
            history -> List[int]

        Output:
            Blueprint Analysis Dictionary
        """

        if len(history) < 50:

            return {

                "signal": "WAIT",

                "target_digit": "-",

                "blueprint_score": 0,

                "confidence": 0,

                "ranking": [],

                "details": {}

            }

        # ---------------------------------------
        # Run every analysis engine
        # ---------------------------------------

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

        # Everything after this point will be
        # calculated in Part 2

        return {

            "frequency_scores": frequency_scores,

            "momentum_scores": momentum_scores,

            "transition_scores": transition_scores,

            "confidence_result": confidence_result

          }
