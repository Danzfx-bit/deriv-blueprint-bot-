from collections import Counter
from datetime import datetime, timedelta

from database import load_ticks_between, load_ticks


class MatchesStrategy:
    """
    Digit Matches prediction strategy - fully automatic, tick-driven.

    Every tick/rerun (no button needed):

    1. Compute each digit's % in the CURRENT, still-filling clock
       hour, and each digit's % in the PREVIOUS, fully-completed
       clock hour.
    2. Rank digits by current-hour %. Take the top 3.
    3. "Gaining" = a top-3 digit's current-hour % is higher than its
       previous-hour %.
    4. Valid setup = top-1 digit is >= MIN_TOP_PERCENT (12%) AND all
       of the top 3 are gaining.
    5. If valid, the target is the #2 (second most frequent) digit.
    6. The #1 digit becomes the "anchor" and stays locked in as the
       active signal for as long as later recalculations keep
       agreeing it's still #1 - even through momentary dips below
       the threshold. The lock only breaks when a DIFFERENT digit
       takes over the #1 spot.
    7. Entry only fires once the live/current digit actually equals
       the locked anchor digit (the "cursor touches it" rule).
    """

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

    def get_snapshot(self, market):
        """
        Stateless: computes the live current-hour-vs-previous-hour
        picture right now, for this instant. Does not know or care
        about any previously locked anchor - that's handled by
        update_anchor().
        """

        now = datetime.utcnow()

        current_hour_start = now.replace(
            minute=0, second=0, microsecond=0
        )

        previous_hour_start = current_hour_start - timedelta(hours=1)

        current_digits = load_ticks_between(
            market,
            current_hour_start.isoformat()
        )

        previous_digits = load_ticks_between(
            market,
            previous_hour_start.isoformat(),
            current_hour_start.isoformat()
        )

        latest = load_ticks(market, limit=1)
        live_digit = latest[-1] if latest else "-"

        empty = {
            "ready": False,
            "reason": "Waiting for a full previous hour of tick data",
            "current_pct": {},
            "previous_pct": {},
            "ranking": [],
            "top1_digit": "-", "top1_pct": 0,
            "top2_digit": "-", "top2_pct": 0,
            "top3_digit": "-", "top3_pct": 0,
            "gaining": {}, "all_gaining": False, "threshold_met": False,
            "live_digit": live_digit,
        }

        if not current_digits or not previous_digits:
            return empty

        current_pct = self._percentages(current_digits)
        previous_pct = self._percentages(previous_digits)

        ranking = sorted(
            current_pct.items(),
            key=lambda x: x[1],
            reverse=True
        )

        top3 = ranking[:3]

        top1_digit, top1_pct = top3[0]
        top2_digit, top2_pct = top3[1]
        top3_digit, top3_pct = top3[2]

        gaining = {
            d: current_pct[d] > previous_pct.get(d, 0)
            for d, _ in top3
        }

        all_gaining = all(gaining.values())
        threshold_met = top1_pct >= self.MIN_TOP_PERCENT

        return {
            "ready": True,
            "reason": "",
            "current_pct": current_pct,
            "previous_pct": previous_pct,
            "ranking": ranking,
            "top1_digit": top1_digit, "top1_pct": top1_pct,
            "top2_digit": top2_digit, "top2_pct": top2_pct,
            "top3_digit": top3_digit, "top3_pct": top3_pct,
            "gaining": gaining,
            "all_gaining": all_gaining,
            "threshold_met": threshold_met,
            "live_digit": live_digit,
        }

    def update_anchor(self, snapshot, anchor_state):
        """
        anchor_state: {"digit": X, "target": Y} or None - whatever
        was locked in from the previous call.

        Returns (new_anchor_state, status):

        - If the anchor's digit is still #1 right now, it stays
          locked exactly as-is (even if threshold/gaining momentarily
          dip) - identity of #1 is the only thing that breaks a lock.
        - If a different digit is now #1 and IT currently qualifies
          (threshold + gaining), it becomes the new anchor.
        - If a different digit is now #1 but doesn't qualify, the
          lock clears and there's no active signal.
        """

        if not snapshot["ready"]:
            return None, {
                "valid": False,
                "entry_active": False,
                "reason": snapshot["reason"],
                "target_digit": "-",
                "top_digit": "-",
                "second_digit": "-",
            }

        top1 = snapshot["top1_digit"]
        top2 = snapshot["top2_digit"]

        qualifies = snapshot["threshold_met"] and snapshot["all_gaining"]

        if anchor_state and anchor_state.get("digit") == top1:

            new_anchor = anchor_state

        elif qualifies:

            new_anchor = {"digit": top1, "target": top2}

        else:

            new_anchor = None

        if new_anchor is None:

            if not snapshot["threshold_met"]:
                reason = (
                    f"Top digit {top1} only {snapshot['top1_pct']}% "
                    f"(< {self.MIN_TOP_PERCENT}%)"
                )
            else:
                declining = [
                    str(d) for d, ok in snapshot["gaining"].items()
                    if not ok
                ]
                reason = (
                    f"Digit(s) {', '.join(declining)} in top 3 "
                    f"aren't gaining vs last hour"
                )

            return None, {
                "valid": False,
                "entry_active": False,
                "reason": reason,
                "target_digit": "-",
                "top_digit": top1,
                "second_digit": top2,
            }

        live_digit = snapshot["live_digit"]
        entry_active = (live_digit == new_anchor["digit"])

        if entry_active:
            reason = (
                f"Live digit touched {new_anchor['digit']} - "
                f"match {new_anchor['target']} now"
            )
        else:
            reason = (
                f"Locked on {new_anchor['digit']} - waiting for "
                f"live digit to touch it"
            )

        return new_anchor, {
            "valid": True,
            "entry_active": entry_active,
            "reason": reason,
            "target_digit": new_anchor["target"] if entry_active else "-",
            "top_digit": new_anchor["digit"],
            "second_digit": new_anchor["target"],
        }
