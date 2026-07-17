class ConfidenceEngine:

    def __init__(self):

        self.max_confidence = 100


    def analyze(
        self,
        frequency_scores,
        momentum_scores,
        transition_scores
    ):

        digits = {}

        # -------------------------------
        # Combine all engine scores
        # -------------------------------

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

            total = (
                frequency +
                momentum +
                transition
            )

            digits[digit] = {

                "frequency": frequency,

                "momentum": momentum,

                "transition": transition,

                "total": round(
                    total,
                    2
                )

            }

        # -------------------------------
        # Rank digits
        # -------------------------------

        ranking = sorted(

            digits.items(),

            key=lambda x: x[1]["total"],

            reverse=True

        )

        best_digit = ranking[0][0]
        best_total = ranking[0][1]["total"]

        second_total = ranking[1][1]["total"]

        # -------------------------------
        # Separation Score
        # -------------------------------

        separation = max(
            best_total -
            second_total,
            0
        )

        separation_score = min(
            separation * 6,
            40
        )

        # -------------------------------
        # Agreement Score
        # -------------------------------

        agreement = 0

        best_frequency = max(

            frequency_scores,

            key=lambda x:
            frequency_scores[x]["score"]

        )

        best_momentum = max(

            momentum_scores,

            key=lambda x:
            momentum_scores[x]["score"]

        )

        best_transition = max(

            transition_scores,

            key=lambda x:
            transition_scores[x]["score"]

        )

        if best_digit == best_frequency:

            agreement += 20

        if best_digit == best_momentum:

            agreement += 20

        if best_digit == best_transition:

            agreement += 20

        # -------------------------------
        # Stability Score
        # -------------------------------

        stability = min(
            best_total,
            20
        )

        # -------------------------------
        # Final Confidence
        # -------------------------------

        confidence = round(

            separation_score +
            agreement +
            stability,

            2

        )

        confidence = min(
            confidence,
            self.max_confidence
        )

        return {

            "target_digit": best_digit,

            "confidence": confidence,

            "ranking": ranking,

            "details": digits

          }
