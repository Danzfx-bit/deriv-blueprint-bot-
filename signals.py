from blueprint_engine import BlueprintEngine
from learning_engine import LearningEngine
from tracker import save_signal


blueprint = BlueprintEngine()

learning = LearningEngine()


def analyze_digits(
    history,
    market="Unknown",
    duration=1
):

    result = blueprint.analyze(history)

    if result["signal"] != "WAIT":

        target = result["target_digit"]

        save_signal(

            market=market,

            signal=result["signal"],

            digit=target,

            probability=result["confidence"],

            duration=duration

        )

        learning.save_prediction(

            market=market,

            predicted_digit=target,

            frequency_score=result["details"]["blueprint"][target]["frequency"],

            momentum_score=result["details"]["blueprint"][target]["momentum"],

            transition_score=result["details"]["blueprint"][target]["transition"],

            confidence=result["confidence"],

            signal=result["signal"],

            duration=duration

        )

    return result
