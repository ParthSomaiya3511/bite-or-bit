# =========================================
# IMPORTS
# =========================================

import random


# =========================================
# AI TRAFFIC SIMULATOR
# =========================================

def simulate_traffic():

    traffic_levels = [

        {
            "level": "LOW",
            "delay": 2,
            "color": "green"
        },

        {
            "level": "MEDIUM",
            "delay": 5,
            "color": "orange"
        },

        {
            "level": "HIGH",
            "delay": 10,
            "color": "red"
        },

        {
            "level": "ROAD BLOCK",
            "delay": 20,
            "color": "darkred"
        },

        {
            "level": "FESTIVAL RUSH",
            "delay": 15,
            "color": "purple"
        }
    ]

    selected = random.choice(
        traffic_levels
    )

    return selected
