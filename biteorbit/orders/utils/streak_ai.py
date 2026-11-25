# =========================================
# AI STREAK SYSTEM
# =========================================

from datetime import date, timedelta

from orders.models import (

    RiderStreak,
    RiderWallet
)


def update_rider_streak(rider):

    streak, created = RiderStreak.objects.get_or_create(

        rider=rider
    )

    today = date.today()

    # =====================================
    # FIRST DELIVERY
    # =====================================

    if not streak.last_delivery_date:

        streak.current_streak = 1

    else:

        difference = (

            today - streak.last_delivery_date
        ).days

        # =================================
        # CONTINUE STREAK
        # =================================

        if difference == 1:

            streak.current_streak += 1

        # =================================
        # SAME DAY
        # =================================

        elif difference == 0:

            pass

        # =================================
        # STREAK BROKEN
        # =================================

        else:

            streak.current_streak = 1

    # =====================================
    # HIGHEST STREAK
    # =====================================

    if streak.current_streak > streak.highest_streak:

        streak.highest_streak = streak.current_streak

    # =====================================
    # XP SYSTEM
    # =====================================

    xp_gain = 50 * streak.current_streak

    streak.total_xp += xp_gain

    # =====================================
    # LEVEL SYSTEM
    # =====================================

    streak.rider_level = (

        streak.total_xp // 500
    ) + 1

    # =====================================
    # MULTIPLIER
    # =====================================

    if streak.current_streak >= 30:

        streak.streak_multiplier = 3.0

    elif streak.current_streak >= 15:

        streak.streak_multiplier = 2.0

    elif streak.current_streak >= 7:

        streak.streak_multiplier = 1.5

    else:

        streak.streak_multiplier = 1.0

    # =====================================
    # BONUS WALLET
    # =====================================

    bonus = (

        20 * streak.streak_multiplier
    )

    wallet, created = RiderWallet.objects.get_or_create(

        rider=rider
    )

    wallet.available_balance += bonus

    wallet.bonus += bonus

    wallet.save()

    # =====================================
    # SAVE
    # =====================================

    streak.last_delivery_date = today

    streak.save()

    return {

        "current_streak":
        streak.current_streak,

        "highest_streak":
        streak.highest_streak,

        "xp":
        streak.total_xp,

        "level":
        streak.rider_level,

        "multiplier":
        streak.streak_multiplier,

        "bonus":
        bonus
    }
