from collections import defaultdict


class TransitionEngine:

    def __init__(self):

        # Maximum Blueprint contribution
        self.max_score = 15


    def analyze(self, history):

        if len(history) < 2:
            return {}

        # Transition matrix
        transitions = defaultdict(
            lambda: defaultdict(int)
        )

        # Build transition counts
        for i in range(len(history) - 1):

            current_digit = history[i]
            next_digit = history[i + 1]

            transitions[current_digit][next_digit] += 1

        current_digit = history[-1]

        current_transitions = transitions[current_digit]

        total = sum(
            current_transitions.values()
        )

        scores = {}

        for digit in range(10):

            count = current_transitions.get(
                digit,
                0
            )

            probability = 0

            if total > 0:

                probability = (
                    count / total
                )

            score = probability * self.max_score

            scores[digit] = {

                "transitions": count,

                "probability": round(
                    probability * 100,
                    2
                ),

                "score": round(
                    score,
                    2
                )

            }

        return scores
