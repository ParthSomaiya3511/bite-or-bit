from random import randint


# =========================================
# AI SAFETY DETECTION
# =========================================

def detect_rider_safety(

    speed,
    sudden_brakes,
    overspeed_count
):

    score = 100

    danger = False

    reasons = []

    # =====================================
    # OVER SPEED
    # =====================================

    if speed > 80:

        score -= 30

        reasons.append(
            "Over Speeding"
        )

    # =====================================
    # EXTREME SPEED
    # =====================================

    if speed > 100:

        score -= 50

        danger = True

        reasons.append(
            "Extreme Dangerous Speed"
        )

    # =====================================
    # SUDDEN BRAKES
    # =====================================

    if sudden_brakes >= 3:

        score -= 25

        reasons.append(
            "Sudden Braking"
        )

    # =====================================
    # OVERSPEED HISTORY
    # =====================================

    if overspeed_count >= 5:

        score -= 20

        reasons.append(
            "Repeated Over-speeding"
        )

    # =====================================
    # RANDOM ACCIDENT SIMULATION
    # =====================================

    accident_chance = randint(1, 100)

    if accident_chance >= 97:

        danger = True

        reasons.append(
            "Possible Accident Detected"
        )

    score = max(score, 0)

    return {

        "safety_score": score,

        "danger": danger,

        "reasons": reasons
    }