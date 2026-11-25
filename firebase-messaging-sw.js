importScripts(

'https://www.gstatic.com/firebasejs/10.12.2/firebase-app-compat.js'

);

importScripts(

'https://www.gstatic.com/firebasejs/10.12.2/firebase-messaging-compat.js'

);


firebase.initializeApp({

   apiKey: "AIzaSyBXG4_mVS1F8l4BNQvkp0Fh3417jELuKQU",
    authDomain: "biteorbit-1d72b.firebaseapp.com",
    projectId: "biteorbit-1d72b",
    storageBucket: "biteorbit-1d72b.firebasestorage.app",
    messagingSenderId: "91737331565",
    appId: "1:91737331565:web:2906208a274afbd04f6c64"

});


const messaging = firebase.messaging();


// BACKGROUND NOTIFICATION

messaging.onBackgroundMessage(

(payload) => {

    self.registration.showNotification(

        payload.notification.title,

        {

            body:
                payload.notification.body,

            icon:
                '/logo.png'
        }
    );
});