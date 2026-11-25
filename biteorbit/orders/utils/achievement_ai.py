# =========================================
# AI ACHIEVEMENT SYSTEM
# =========================================

from orders.models import (

    RiderAchievement,
    RiderPerformance
)


def unlock_rider_achievement(

    rider,
    performance
):

    unlocked = []

    # =====================================
    # SPEED MASTER
    # =====================================

    if performance.average_eta < 15:

        badge_name = "Speed Master"

        if not RiderAchievement.objects.filter(

            rider=rider,
            badge_name=badge_name

        ).exists():

            RiderAchievement.objects.create(

                rider=rider,

                badge_name=badge_name,

                badge_icon="⚡",

                description="Ultra Fast Delivery Rider",

                xp_reward=100
            )

            performance.xp_points += 100

            unlocked.append(badge_name)

    # =====================================
    # DELIVERY KING
    # =====================================

    if performance.successful_deliveries >= 100:

        badge_name = "Delivery King"

        if not RiderAchievement.objects.filter(

            rider=rider,
            badge_name=badge_name

        ).exists():

            RiderAchievement.objects.create(

                rider=rider,

                badge_name=badge_name,

                badge_icon="👑",

                description="100+ Successful Deliveries",

                xp_reward=300
            )

            performance.xp_points += 300

            unlocked.append(badge_name)

    # =====================================
    # ELITE RIDER
    # =====================================

    if performance.performance_score >= 1000:

        badge_name = "Elite Rider"

        if not RiderAchievement.objects.filter(

            rider=rider,
            badge_name=badge_name

        ).exists():

            RiderAchievement.objects.create(

                rider=rider,

                badge_name=badge_name,

                badge_icon="🔥",

                description="Top Performance Rider",

                xp_reward=500
            )

            performance.xp_points += 500

            unlocked.append(badge_name)

    # =====================================
    # LEVEL SYSTEM
    # =====================================

    performance.level = (

        performance.xp_points // 500
    ) + 1

    performance.save()

    return {

        "unlocked": unlocked,

        "xp": performance.xp_points,

        "level": performance.level
    }
