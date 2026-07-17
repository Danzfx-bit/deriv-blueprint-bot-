from collections import Counter


def analyze_digits(ticks):
    """
    Analyze the last digits from a list of tick prices.
    """

    digits = [int(str(price)[-1]) for price in ticks]

    counts = Counter(digits)

    total = len(digits)

    probabilities = {
        digit: round((counts.get(digit, 0) / total) * 100, 2)
        for digit in range(10)
    }

    hottest = max(probabilities, key=probabilities.get)
    coldest = min(probabilities, key=probabilities.get)

    return {
        "counts": counts,
        "probabilities": probabilities,
        "hot_digit": hottest,
        "cold_digit": coldest
  }
