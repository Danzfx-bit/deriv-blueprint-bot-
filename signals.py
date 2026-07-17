from blueprint_engine import BlueprintEngine
from tracker import save_signal


engine = BlueprintEngine()


def analyze_digits(
    history,
    market="Unknown",
    duration=5
):

    result = engine.analyze(history)

    if result["signal"] != "WAIT":

        save_signal(

            market=market,

            signal=result["signal"],

            digit=result["number"],

            probability=result["blueprint_score"],

            duration=duration

        )

    return result
