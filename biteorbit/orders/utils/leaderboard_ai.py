# =========================================
# AI LEADERBOARD SYSTEM
# =========================================

from orders.models import (
    RiderPerformance
)


def update_rider_performance(

    rider,
    eta_minutes,
    success=True
):

    performance, created = RiderPerformance.objects.get_or_create(

        rider=rider
    )

    # =====================================
    # UPDATE DELIVERY COUNTS
    # =====================================

    performance.total_deliveries += 1

    if success:

        performance.successful_deliveries += 1

    else:

        performance.failed_deliveries += 1

    # =====================================
    # ETA SCORE
    # =====================================

    performance.average_eta = (

        performance.average_eta + eta_minutes
    ) / 2

    # =====================================
    # PERFORMANCE SCORE
    # =====================================

    score = 0

    score += performance.successful_deliveries * 10

    score -= performance.failed_deliveries * 5

    score -= performance.fraud_reports * 20

    if performance.average_eta < 20:

        score += 50

    performance.performance_score = score

    # =====================================
    # RANK SYSTEM
    # =====================================

    if score >= 1000:

        performance.rider_rank = "Platinum"

    elif score >= 700:

        performance.rider_rank = "Gold"

    elif score >= 400:

        performance.rider_rank = "Silver"

    else:

        performance.rider_rank = "Bronze"

    performance.save()

    return {

        "score": score,

        "rank": performance.rider_rank
    }
