from blueprint_engine import BlueprintEngine
from learning_engine import LearningEngine
from tracker import save_signal


blueprint = BlueprintEngine()

learning = LearningEngine()


def analyze_digits(
    history,
    market="Unknown",
    duration=5
):

    result = blueprint.analyze(history)

    if result["signal"] != "WAIT":

        save_signal(

            market=market,

            signal=result["signal"],

            digit=result["number"],

            probability=result["blueprint_score"],

            duration=duration

        )

        learning.save_prediction(

            market=market,

            predicted_digit=result["number"],

            blueprint_score=result["blueprint_score"],

            confidence=result["confidence"],

            signal=result["signal"],

            duration=duration

        )

    return result
