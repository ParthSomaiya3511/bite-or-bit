# =========================================
# AI DISCIPLINE SYSTEM
# =========================================

from orders.models import (
    RiderDiscipline
)


def update_rider_discipline(

    rider,
    late_delivery=False,
    fraud=False,
    cancelled=False
):

    discipline, created = RiderDiscipline.objects.get_or_create(

        rider=rider
    )

    # =====================================
    # LATE DELIVERY
    # =====================================

    if late_delivery:

        discipline.late_delivery_count += 1

        discipline.warning_count += 1

        discipline.trust_score -= 5

    # =====================================
    # FRAUD
    # =====================================

    if fraud:

        discipline.fraud_count += 1

        discipline.warning_count += 2

        discipline.trust_score -= 25

    # =====================================
    # CANCELLED
    # =====================================

    if cancelled:

        discipline.cancelled_delivery_count += 1

        discipline.warning_count += 1

        discipline.trust_score -= 10

    # =====================================
    # MIN SCORE
    # =====================================

    if discipline.trust_score < 0:

        discipline.trust_score = 0

    # =====================================
    # REPUTATION LEVEL
    # =====================================

    score = discipline.trust_score

    if score >= 90:

        discipline.reputation_level = "Excellent"

    elif score >= 70:

        discipline.reputation_level = "Good"

    elif score >= 50:

        discipline.reputation_level = "Average"

    elif score >= 30:

        discipline.reputation_level = "Risky"

    else:

        discipline.reputation_level = "Danger"

    # =====================================
    # AUTO SUSPEND
    # =====================================

    if discipline.trust_score <= 20:

        discipline.is_suspended = True

        discipline.suspension_reason = (

            "AI Auto Suspension Triggered"
        )

    discipline.save()

    return {

        "trust_score":
        discipline.trust_score,

        "warnings":
        discipline.warning_count,

        "reputation":
        discipline.reputation_level,

        "is_suspended":
        discipline.is_suspended
    }
