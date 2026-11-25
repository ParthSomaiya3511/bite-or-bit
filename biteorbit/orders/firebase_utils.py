import firebase_admin

from firebase_admin import credentials
from firebase_admin import messaging

import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

cred = credentials.Certificate(

    os.path.join(
        BASE_DIR,
        "firebase-service-account.json"
    )
)

if not firebase_admin._apps:

    firebase_admin.initialize_app(cred)


def send_push_notification(

    token,
    title,
    body
):

    try:

        message = messaging.Message(

            notification=messaging.Notification(

                title=title,
                body=body
            ),

            token=token
        )

        response = messaging.send(message)

        print("Push Sent:", response)

        return True

    except Exception as e:

        print("Push Error:", e)

        return False
