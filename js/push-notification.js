// =========================================
// REQUEST PERMISSION
// =========================================

async function requestPermission() {

    const permission =
        await Notification.requestPermission()

    console.log(permission)

    if (permission === "granted") {

        alert(
            "Notifications Enabled"
        )

    } else {

        alert(
            "Notification Permission Denied"
        )
    }
}


// =========================================
// SHOW NOTIFICATION
// =========================================

function showNotification(title, body) {

    if (Notification.permission === "granted") {

        new Notification(title, {

            body: body,

            icon:
                "https://cdn-icons-png.flaticon.com/512/3595/3595455.png",

            badge:
                "https://cdn-icons-png.flaticon.com/512/3595/3595455.png"
        })
    }
}