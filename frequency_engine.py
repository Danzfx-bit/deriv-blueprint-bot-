from collections import Counter


class FrequencyEngine:

    def __init__(self):
        self.max_score = 25


    def analyze(self, history):

        if len(history) == 0:
            return {}

        total = len(history)

        counts = Counter(history)

        scores = {}

        for digit in range(10):

            frequency = counts.get(digit, 0)

            percentage = frequency / total

            score = percentage * self.max_score

            scores[digit] = {
                "count": frequency,
                "percentage": round(
                    percentage * 100,
                    2
                ),
                "score": round(
                    score,
                    2
                )
            }

        return scores
