
from collections import Counter


def analyze_digits(history):

    if len(history) == 0:
        return {
            "match_probability": 0,
            "differ_probability": 0,
            "recommendation": "WAIT",
            "confidence": 0
        }

    current_digit = history[-1]

    counts = Counter(history)

    digit_frequency = counts.get(current_digit, 0)

    match_probability = (digit_frequency / len(history)) * 100

    differ_probability = 100 - match_probability


    if differ_probability > match_probability:
        recommendation = "DIFFER"
        confidence = differ_probability

    else:
        recommendation = "MATCH"
        confidence = match_probability


    return {
        "current_digit": current_digit,
        "match_probability": round(match_probability, 2),
        "differ_probability": round(differ_probability, 2),
        "recommendation": recommendation,
        "confidence": round(confidence, 2),
        "frequency": digit_frequency
    }  
