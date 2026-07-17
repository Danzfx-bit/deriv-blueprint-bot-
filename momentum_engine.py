from collections import Counter


class MomentumEngine:

    def __init__(self):

        # Maximum contribution to Blueprint Score
        self.max_score = 25

        # Number of recent ticks to analyse
        self.window = 100


    def analyze(self, history):

        if len(history) == 0:
            return {}

        recent = history[-self.window:]

        total = len(history)

        recent_total = len(recent)

        overall_counts = Counter(history)

        recent_counts = Counter(recent)

        scores = {}

        for digit in range(10):

            overall_frequency = (
                overall_counts.get(digit, 0)
                / total
            )

            recent_frequency = (
                recent_counts.get(digit, 0)
                / recent_total
            )

            # Positive = gaining momentum
            # Negative = losing momentum
            momentum = (
                recent_frequency -
                overall_frequency
            )

            # Convert momentum into a score
            if momentum <= 0:

                score = 0

            else:

                score = min(
                    momentum * 250,
                    self.max_score
                )

            scores[digit] = {

                "overall_frequency": round(
                    overall_frequency * 100,
                    2
                ),

                "recent_frequency": round(
                    recent_frequency * 100,
                    2
                ),

                "momentum": round(
                    momentum * 100,
                    2
                ),

                "score": round(
                    score,
                    2
                )

            }

        return scores
