class OverUnderStrategy:
    """
    Over/Under 5 prediction strategy.

    Groups: Under = {0,1,2,3,4}, Over = {5,6,7,8,9}.

    Every STEP (20) ticks, take a fresh snapshot of Over%'s value
    across the current rolling WINDOW (200) ticks. These snapshots
    are computed retroactively straight from stored tick history -
    no persisted state needed, since we can always re-slice the
    same history at different offsets from "now".

    From a short series of these snapshots:

        trend[i]        = snapshot[i] - snapshot[i-1]
        acceleration[i]  = trend[i] - trend[i-1]

    Since Over% + Under% = 100% always, Under's trend/acceleration
    are exactly the negative of Over's - only Over% needs computing.

    Signal:
        Over trend  > +2% AND Over acceleration  > 0  -> "OVER 5"
        Under trend > +2% AND Under acceleration > 0  -> "UNDER 5"
        otherwise -> no signal

    Only one side can ever fire at once (they're exact opposites),
    so there's no risk of both triggering simultaneously.

    Confidence is graded: floors at 50% right at the +2% threshold,
    scales up with how far trend exceeds it, plus a small bonus for
    stronger acceleration, capped at 99%.
    """

    STEP = 20
    WINDOW = 200
    NUM_SNAPSHOTS = 5
    MIN_SNAPSHOTS = 3
    TREND_THRESHOLD = 2.0

    def _over_percent(self, digits):

        total = len(digits)

        if total == 0:
            return 0.0

        over_count = sum(1 for d in digits if d >= 5)

        return round((over_count / total) * 100, 2)

    def _build_snapshots(self, history):
        """
        Returns Over% snapshots, oldest to newest. snapshot for step
        k uses the WINDOW-tick window ending STEP*k ticks before the
        most recent tick - i.e. "what Over% looked like k updates
        ago." Uses as many snapshots as the available history
        allows, up to NUM_SNAPSHOTS.
        """

        if len(history) < self.WINDOW:
            return []

        max_possible = 1 + (len(history) - self.WINDOW) // self.STEP
        count = min(self.NUM_SNAPSHOTS, max_possible)

        snapshots = []

        for k in range(count - 1, -1, -1):

            offset = self.STEP * k
            end = len(history) - offset
            start = end - self.WINDOW

            if start < 0:
                continue

            window = history[start:end]
            snapshots.append(self._over_percent(window))

        return snapshots

    def _confidence(self, trend, acceleration):

        excess = max(0, trend - self.TREND_THRESHOLD)

        base = 50 + excess * 5
        bonus = min(10, acceleration * 4)

        return min(99, round(base + bonus, 2))

    def analyze(self, history):

        snapshots = self._build_snapshots(history)

        if len(snapshots) < self.MIN_SNAPSHOTS:

            needed = self.WINDOW + self.STEP * (self.MIN_SNAPSHOTS - 1)

            return {
                "valid": False,
                "signal": "-",
                "confidence": 0,
                "reason": f"Need {needed} ticks for {self.MIN_SNAPSHOTS} snapshots, have {len(history)}",
                "over_percent": 0,
                "under_percent": 0,
                "over_trend": 0,
                "under_trend": 0,
                "over_acceleration": 0,
                "under_acceleration": 0,
                "snapshots": snapshots,
            }

        trends = [
            round(snapshots[i] - snapshots[i - 1], 2)
            for i in range(1, len(snapshots))
        ]

        accelerations = [
            round(trends[i] - trends[i - 1], 2)
            for i in range(1, len(trends))
        ]

        latest_over_pct = snapshots[-1]
        latest_under_pct = round(100 - latest_over_pct, 2)

        over_trend = trends[-1]
        under_trend = round(-over_trend, 2)

        over_acceleration = accelerations[-1] if accelerations else 0
        under_acceleration = round(-over_acceleration, 2) if accelerations else 0

        over_valid = (over_trend > self.TREND_THRESHOLD) and (over_acceleration > 0)
        under_valid = (under_trend > self.TREND_THRESHOLD) and (under_acceleration > 0)

        if over_valid:

            signal = "OVER 5"
            confidence = self._confidence(over_trend, over_acceleration)
            reason = f"Over trend +{over_trend}% (accel +{over_acceleration}) - OVER 5"

        elif under_valid:

            signal = "UNDER 5"
            confidence = self._confidence(under_trend, under_acceleration)
            reason = f"Under trend +{under_trend}% (accel +{under_acceleration}) - UNDER 5"

        else:

            signal = "-"
            confidence = 0
            reason = (
                f"No signal - Over trend {over_trend:+.2f}%, "
                f"Under trend {under_trend:+.2f}% "
                f"(need > {self.TREND_THRESHOLD}% + positive acceleration)"
            )

        return {
            "valid": signal != "-",
            "signal": signal,
            "confidence": confidence,
            "reason": reason,
            "over_percent": latest_over_pct,
            "under_percent": latest_under_pct,
            "over_trend": over_trend,
            "under_trend": under_trend,
            "over_acceleration": over_acceleration,
            "under_acceleration": under_acceleration,
            "snapshots": snapshots,
        }
