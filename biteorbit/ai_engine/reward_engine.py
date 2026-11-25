# =========================================
# AI REWARD ENGINE
# =========================================

def calculate_rewards(

    order_amount,

    membership="Free"
):

    cashback_percentage = 2

    reward_multiplier = 1

    # =====================================
    # MEMBERSHIP BONUS
    # =====================================

    if membership == "Gold":

        cashback_percentage = 5

        reward_multiplier = 2

    elif membership == "Platinum":

        cashback_percentage = 10

        reward_multiplier = 3

    # =====================================
    # CALCULATE CASHBACK
    # =====================================

    cashback = (

        order_amount *

        cashback_percentage
    ) / 100

    # =====================================
    # REWARD POINTS
    # =====================================

    reward_points = int(

        order_amount / 10
    ) * reward_multiplier

    return {

        "cashback":

        round(cashback, 2),

        "reward_points":

        reward_points
    }
