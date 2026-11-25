# =========================================
# AI RIDER MISSION SYSTEM
# =========================================

from datetime import timedelta
from django.utils import timezone

from orders.models import (

    RiderMission,
    RiderWallet,
    RiderPerformance
)


# =========================================
# CREATE DAILY MISSIONS
# =========================================

def create_daily_missions(rider):

    if RiderMission.objects.filter(

        rider=rider,

        is_completed=False

    ).exists():

        return

    missions = [

        {
            "title": "Complete 5 Deliveries",

            "description":
            "Finish 5 deliveries today",

            "target": 5,

            "reward": 100,

            "xp": 50
        },

        {
            "title": "Peak Hour Hero",

            "description":
            "Complete 10 deliveries",

            "target": 10,

            "reward": 300,

            "xp": 150
        }
    ]

    for item in missions:

        RiderMission.objects.create(

            rider=rider,

            mission_title=item["title"],

            mission_description=item["description"],

            target_count=item["target"],

            reward_amount=item["reward"],

            xp_reward=item["xp"],

            expires_at=timezone.now() + timedelta(days=1)
        )


# =========================================
# UPDATE MISSIONS
# =========================================

def update_missions(rider):

    missions = RiderMission.objects.filter(

        rider=rider,

        is_completed=False
    )

    performance = RiderPerformance.objects.get(

        rider=rider
    )

    wallet, created = RiderWallet.objects.get_or_create(

        rider=rider
    )

    completed = []

    for mission in missions:

        mission.completed_count = (

            performance.successful_deliveries
        )

        # =====================================
        # COMPLETE MISSION
        # =====================================

        if mission.completed_count >= mission.target_count:

            mission.is_completed = True

            wallet.available_balance += mission.reward_amount

            wallet.bonus += mission.reward_amount

            performance.xp_points += mission.xp_reward

            wallet.save()

            performance.save()

            completed.append({

                "mission":
                mission.mission_title,

                "reward":
                mission.reward_amount
            })

        mission.save()

    return completed
