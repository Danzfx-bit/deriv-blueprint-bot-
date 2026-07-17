from collections import Counter
from tracker import save_signal


def analyze_digits(history, market="Unknown", duration=5):

    if len(history) < 100:

        return {
            "signal": "WAIT",
            "number": "-",
            "match_probability": 0,
            "differ_probability": 0,
            "confidence": "LOW",
            "duration": duration,
            "ranking": {}
        }

    total = len(history)

    frequency = Counter(history)

    recent = history[-100:]

    recent_frequency = Counter(recent)

    scores = {}

    for digit in range(10):

        long_score = (
            frequency.get(digit, 0) / total
        ) * 100

        recent_score = (
            recent_frequency.get(digit, 0) / len(recent)
        ) * 100

        score = (
            long_score * 0.60
            +
            recent_score * 0.40
        )

        scores[digit] = round(score, 2)

    ranking = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    best_digit = ranking[0][0]

    match_probability = ranking[0][1]

    differ_probability = round(
        100 - match_probability,
        2
    )

    if match_probability >= 60:
        signal = "MATCH"
    else:
        signal = "DIFFER"

    confidence = "LOW"

    if max(match_probability, differ_probability) >= 80:
        confidence = "HIGH"

    elif max(match_probability, differ_probability) >= 65:
        confidence = "MEDIUM"

    save_signal(
        market=market,
        signal=signal,
        digit=best_digit,
        probability=max(
            match_probability,
            differ_probability
        ),
        duration=duration
    )

    return {

        "signal": signal,

        "number": best_digit,

        "match_probability": round(
            match_probability,
            2
        ),

        "differ_probability": differ_probability,

        "confidence": confidence,

        "duration": duration,

        "ranking": ranking[:5]
    }
