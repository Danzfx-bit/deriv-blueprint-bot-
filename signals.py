from collections import Counter
from tracker import save_signal


def analyze_digits(history, market="Unknown", duration=5):

    if len(history) < 50: 
        return {
            "signal": "WAIT",
            "number": "-",
            "blueprint_score": 0,
            "confidence": "LOW",
            "duration": duration,
            "ranking": []
        }

    total = len(history)

    recent = history[-100:]

    frequency = Counter(history)

    recent_frequency = Counter(recent)

    scores = {}

    for digit in range(10):

        # Long-term frequency (0–25)
        long_freq = frequency.get(digit, 0) / total
        long_score = long_freq * 25

        # Recent frequency (0–35)
        recent_freq = recent_frequency.get(digit, 0) / len(recent)
        recent_score = recent_freq * 35

        # Momentum (0–20)
        momentum = max(0, recent_freq - long_freq)
        momentum_score = min(momentum * 200, 20)

        # Recency (0–10)
        try:
            last_seen = len(history) - 1 - history[::-1].index(digit)
            ticks_since = len(history) - last_seen
            recency_score = max(0, 10 - (ticks_since / 10))
        except ValueError:
            recency_score = 0

        # Pattern bonus (placeholder)
        pattern_bonus = 10

        blueprint_score = (
            long_score +
            recent_score +
            momentum_score +
            recency_score +
            pattern_bonus
        )

        scores[digit] = round(min(blueprint_score, 100), 2)

    ranking = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    best_digit = ranking[0][0]
    best_score = ranking[0][1]

    if best_score >= 80:
        confidence = "VERY HIGH"
    elif best_score >= 70:
        confidence = "HIGH"
    elif best_score >= 60:
        confidence = "MEDIUM"
    else:
        confidence = "LOW"

    signal = "MATCH"

    save_signal(
        market=market,
        signal=signal,
        digit=best_digit,
        probability=best_score,
        duration=duration
    )

    return {
        "signal": signal,
        "number": best_digit,
        "blueprint_score": best_score,
        "confidence": confidence,
        "duration": duration,
        "ranking": ranking
    }
