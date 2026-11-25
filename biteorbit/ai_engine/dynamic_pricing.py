import random
from datetime import datetime

# =========================================
# AI DYNAMIC PRICING ENGINE
# =========================================

def calculate_dynamic_price(

    base_fee,
    traffic="Low",
    weather="Clear",
    demand_level=1
):

    multiplier = 1

    reasons = []

    # =====================================
    # TRAFFIC
    # =====================================

    if traffic == "High":

        multiplier += 0.4

        reasons.append(
            "Heavy Traffic"
        )

    elif traffic == "Medium":

        multiplier += 0.2

        reasons.append(
            "Medium Traffic"
        )

    # =====================================
    # WEATHER
    # =====================================

    if weather == "Rain":

        multiplier += 0.3

        reasons.append(
            "Rain Pricing"
        )

    elif weather == "Storm":

        multiplier += 0.5

        reasons.append(
            "Storm Pricing"
        )

    # =====================================
    # DEMAND
    # =====================================

    if demand_level >= 8:

        multiplier += 0.5

        reasons.append(
            "High Demand"
        )

    elif demand_level >= 5:

        multiplier += 0.2

        reasons.append(
            "Medium Demand"
        )

    # =====================================
    # NIGHT CHARGE
    # =====================================

    hour = datetime.now().hour

    if hour >= 23 or hour <= 5:

        multiplier += 0.25

        reasons.append(
            "Night Charge"
        )

    # =====================================
    # FESTIVAL RANDOM
    # =====================================

    if random.randint(1, 20) == 10:

        multiplier += 0.6

        reasons.append(
            "Festival Surge"
        )

    # =====================================
    # FINAL PRICE
    # =====================================

    final_price = round(

        base_fee * multiplier,
        2
    )

    return {

        "base_fee": base_fee,

        "multiplier": multiplier,

        "final_price": final_price,

        "reasons": reasons
    }
