from collections import Counter


class MatchesStrategy:
    """
    Digit Matches prediction strategy - on-demand, live data only.

    Every time this runs (i.e. every time SCAN is pressed), it does a
    completely fresh evaluation using whatever ticks are currently
    available - no clock-hour windows, no persisted state between
    calls, no locking across scans.

    Rules:

    1. Take the last WINDOW ticks currently available. Rank all 10
       digits by frequency % over that window.
    2. Take the top 3 ranked digits. Each must be "gaining": its %
       in the most recent HALF ticks must be higher than its % in
       the older HALF ticks of that same window.
    3. The #1 (most frequent) digit must be >= MIN_TOP_PERCENT (12%).
    4. The live digit (the very latest tick) must equal the #1
       digit right now - the "cursor touches it" entry condition.
    5. If ALL of the above hold, this is a match: the prediction is
       the #2 (second most frequent) digit, confidence 98%.
       If ANY condition fails, it's a flat "no match" - confidence 0,
       target "-" - regardless of which condition(s) failed.
    """

    WINDOW = 200
    HALF = 100
    MIN_TOP_PERCENT = 12.0

    def _percentages(self, digits):

        total = len(digits)

        if total == 0:
            return {d: 0.0 for d in range(10)}

        counts = Counter(digits)

        return {
            d: round((counts.get(d, 0) / total) * 100, 2)
            for d in range(10)
        }

    def analyze(self, history):

        if len(history) < self.WINDOW:

            return {
                "valid": False,
                "entry_active": False,
                "confidence": 0,
                "reason": f"Need {self.WINDOW} ticks, have {len(history)}",
                "target_digit": "-",
                "top_digit": "-",
                "top_percent": 0,
                "second_digit": "-",
                "second_percent": 0,
                "third_digit": "-",
                "third_percent": 0,
                "gaining": {},
                "live_digit": history[-1] if history else "-",
                "ranking": [],
                "full_percentages": {},
            }

        window = list(history[-self.WINDOW:])
        older_half = window[:self.HALF]
        recent_half = window[self.HALF:]

        full_pct = self._percentages(window)
        older_pct = self._percentages(older_half)
        recent_pct = self._percentages(recent_half)

        ranking = sorted(
            full_pct.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top3 = ranking[:3]

        top1_digit, top1_pct = top3[0]
        top2_digit, top2_pct = top3[1]
        top3_digit, top3_pct = top3[2]

        gaining_flags = {
            digit: recent_pct[digit] > older_pct[digit]
            for digit, _ in top3
        }

        all_gaining = all(gaining_flags.values())
        threshold_met = top1_pct >= self.MIN_TOP_PERCENT

        live_digit = window[-1]
        touch = (live_digit == top1_digit)

        valid = threshold_met and all_gaining
        entry_active = valid and touch

        if not threshold_met:
            reason = f"Top digit {top1_digit} only {top1_pct}% (< {self.MIN_TOP_PERCENT}%) - NO MATCH"
        elif not all_gaining:
            declining = [str(d) for d, ok in gaining_flags.items() if not ok]
            reason = f"Digit(s) {', '.join(declining)} in top 3 declining, not gaining - NO MATCH"
        elif not touch:
            reason = f"Live digit hasn't touched {top1_digit} yet - NO MATCH"
        else:
            reason = f"Live digit touched {top1_digit} - match {top2_digit}"

        return {
            "valid": valid,
            "entry_active": entry_active,
            "confidence": 98 if entry_active else 0,
            "reason": reason,
            "target_digit": top2_digit if entry_active else "-",
            "top_digit": top1_digit,
            "top_percent": top1_pct,
            "second_digit": top2_digit,
            "second_percent": top2_pct,
            "third_digit": top3_digit,
            "third_percent": top3_pct,
            "gaining": gaining_flags,
            "live_digit": live_digit,
            "ranking": ranking,
            "full_percentages": full_pct,
        }
