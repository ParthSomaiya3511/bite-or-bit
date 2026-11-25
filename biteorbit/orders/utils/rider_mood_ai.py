from datetime import datetime
from random import randint


# =========================================
# AI MOOD DETECTION
# =========================================

def detect_rider_mood(rider):

    stress = 0

    reasons = []

    # =====================================
    # LATE DELIVERIES
    # =====================================

    if rider.late_delivery_count >= 5:

        stress += 30

        reasons.append(
            "Too many late deliveries"
        )

    # =====================================
    # FATIGUE
    # =====================================

    if rider.fatigue_score >= 70:

        stress += 40

        reasons.append(
            "High fatigue detected"
        )

    # =====================================
    # CUSTOMER REPORTS
    # =====================================

    if rider.anger_reports >= 3:

        stress += 25

        reasons.append(
            "Customer complaints increased"
        )

    # =====================================
    # RANDOM MICRO STRESS
    # =====================================

    stress += randint(5, 15)

    # =====================================
    # MOOD DECISION
    # =====================================

    if stress <= 30:

        mood = "Happy"

    elif stress <= 60:

        mood = "Normal"

    elif stress <= 80:

        mood = "Stressed"

    else:

        mood = "Burnout Risk"

    # =====================================
    # HEALTH SCORE
    # =====================================

    mental_health = max(
        0,
        100 - stress
    )

    return {

        "stress_level": stress,

        "mood": mood,

        "mental_health": mental_health,

        "reasons": reasons
    }