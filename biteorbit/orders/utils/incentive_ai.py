# =========================================
# AI RIDER INCENTIVE SYSTEM
# =========================================

from orders.models import (

    RiderWallet,
    RiderBonus
)


def apply_rider_bonus(

    rider,
    completed_orders,
    weather="Normal"
):

    bonus = 0

    bonus_type = None

    description = None

    # =====================================
    # DAILY TARGET BONUS
    # =====================================

    if completed_orders >= 10:

        bonus += 200

        bonus_type = "Daily Target"

        description = "Completed 10+ orders"

    # =====================================
    # PEAK BONUS
    # =====================================

    if completed_orders >= 20:

        bonus += 500

        bonus_type = "Peak Hour Bonus"

        description = "Peak performance"

    # =====================================
    # RAIN BONUS
    # =====================================

    if weather == "Rain":

        bonus += 150

        bonus_type = "Rain Bonus"

        description = "Rain delivery reward"

    # =====================================
    # UPDATE WALLET
    # =====================================

    if bonus > 0:

        wallet, created = RiderWallet.objects.get_or_create(

            rider=rider
        )

        wallet.available_balance += bonus

        wallet.bonus += bonus

        wallet.save()

        RiderBonus.objects.create(

            rider=rider,

            bonus_type=bonus_type,

            amount=bonus,

            description=description
        )

    return {

        "bonus": bonus,

        "bonus_type": bonus_type,

        "description": description
    }
