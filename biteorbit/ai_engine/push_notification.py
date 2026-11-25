import firebase_admin

from firebase_admin import (
    credentials,
    messaging
)

# =====================================
# FIREBASE INIT
# =====================================

if not firebase_admin._apps:

    cred = credentials.Certificate(

        "firebase-key.json"
    )

    firebase_admin.initialize_app(

        cred
    )

# =====================================
# SEND PUSH
# =====================================

def send_push_notification(

    token,

    title,

    body
):

    try:

        message = messaging.Message(

            notification=

            messaging.Notification(

                title=title,

                body=body
            ),

            token=token
        )

        response = messaging.send(

            message
        )

        return response

    except Exception as e:

        print(e)