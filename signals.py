from collections import Counter


def analyze_digits(history, duration=5):

    if len(history) < 50:
        return {
            "signal": "WAIT",
            "number": "-",
            "match_probability": 0,
            "differ_probability": 0,
            "confidence": "LOW",
            "duration": duration
        }


    # Full history analysis
    total = len(history)

    frequency = Counter(history)


    # Recent behaviour (last 100 ticks)
    recent = history[-100:]

    recent_frequency = Counter(recent)


    scores = {}


    for digit in range(10):

        # Long term frequency
        long_score = (
            frequency.get(digit, 0) / total
        ) * 100


        # Recent momentum weighting
        recent_score = (
            recent_frequency.get(digit, 0) / len(recent)
        ) * 100


        # Combined Blueprint score
        score = (
            (long_score * 0.6)
            +
            (recent_score * 0.4)
        )


        scores[digit] = round(score, 2)


    # Highest scoring digit
    best_digit = max(
        scores,
        key=scores.get
    )


    match_probability = scores[best_digit]


    differ_probability = 100 - match_probability


    if match_probability >= 60:

        signal = "MATCH"

        confidence = (
            "HIGH"
            if match_probability >= 75
            else "MEDIUM"
        )

    else:

        signal = "DIFFER"

        confidence = (
            "HIGH"
            if differ_probability >= 75
            else "MEDIUM"
        )


    return {

        "signal": signal,

        "number": best_digit,

        "match_probability": round(
            match_probability,
            2
        ),

        "differ_probability": round(
            differ_probability,
            2
        ),

        "confidence": confidence,

        "duration": duration,

        "ranking": scores
    }
