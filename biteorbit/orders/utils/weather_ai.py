# =========================================
# AI WEATHER IMPACT SYSTEM
# =========================================

import random


def weather_delivery_ai():

    weather_types = [

        "Clear",
        "Rain",
        "Heavy Rain",
        "Storm",
        "Hot Weather"
    ]

    weather = random.choice(
        weather_types
    )

    delay_minutes = 0

    risk = "Low"

    rider_alert = "Safe"

    # =====================================
    # WEATHER CONDITIONS
    # =====================================

    if weather == "Rain":

        delay_minutes = 10

        risk = "Medium"

        rider_alert = "Drive Carefully"

    elif weather == "Heavy Rain":

        delay_minutes = 20

        risk = "High"

        rider_alert = "Slow Delivery"

    elif weather == "Storm":

        delay_minutes = 35

        risk = "Very High"

        rider_alert = "Danger Zone"

    elif weather == "Hot Weather":

        delay_minutes = 5

        risk = "Medium"

        rider_alert = "Hydration Required"

    return {

        "weather": weather,

        "delay_minutes": delay_minutes,

        "risk": risk,

        "rider_alert": rider_alert
    }
