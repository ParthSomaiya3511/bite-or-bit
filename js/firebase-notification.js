// =========================================
// FIREBASE CONFIG
// =========================================

const firebaseConfig = {

    apiKey: "AIzaSyBXG4_mVS1F8l4BNQvkp0Fh3417jELuKQU",
    authDomain: "biteorbit-1d72b.firebaseapp.com",
    projectId: "biteorbit-1d72b",
    storageBucket: "biteorbit-1d72b.firebasestorage.app",
    messagingSenderId: "91737331565",
    appId: "1:91737331565:web:2906208a274afbd04f6c64"
};

// INIT FIREBASE

firebase.initializeApp(firebaseConfig);

// MESSAGING

const messaging = firebase.messaging();


// =========================================
// REQUEST PERMISSION
// =========================================

async function requestPermission() {

    try {

        const permission =
            await Notification.requestPermission();

        if (permission === "granted") {

            console.log("Notification Allowed");

            getToken();

        } else {

            console.log("Notification Denied");
        }

    } catch (error) {

        console.log(error);
    }
}


// =========================================
// GET DEVICE TOKEN
// =========================================

async function getToken() {

    try {

        const currentToken =
            await messaging.getToken({

                vapidKey:
                    "BP9UyIvQzNKzFmG3eanO_BxVkXw89tuofbjzuFmG3lFNGYqacCg9ASFnZPO6Vnt09Wfebk6E2m-jcdZ9GA-dtKU"
            });

        console.log("FCM TOKEN:");

        console.log(currentToken);

        localStorage.setItem(

            "fcm_token",

            currentToken
        );

    } catch (error) {

        console.log(error);
    }
}


// =========================================
// FOREGROUND NOTIFICATION
// =========================================

messaging.onMessage((payload) => {

    console.log(payload);

    new Notification(

        payload.notification.title,

        {

            body:
                payload.notification.body,

            icon:
                "/logo.png"
        }
    );
});


// =========================================
// AUTO ENABLE
// =========================================

document.addEventListener(

    "DOMContentLoaded",

    function () {

        Notification.requestPermission()
        
        requestPermission();
    }
);