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


        blueprint_data = result.get(

            "details",

            {}

        ).get(

            "blueprint",

            {}

        ).get(

            target,

            {}

        )


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

            frequency_score=blueprint_data.get(

                "frequency",

                0

            ),

            momentum_score=blueprint_data.get(

                "momentum",

                0

            ),

            transition_score=blueprint_data.get(

                "transition",

                0

            ),

            confidence=result["confidence"],

            signal=result["signal"],

            duration=duration

        )


    return result
