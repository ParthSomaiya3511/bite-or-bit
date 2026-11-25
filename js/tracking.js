
// =========================================
// GET ORDER ID
// =========================================

const params =

    new URLSearchParams(
        window.location.search
    )

const orderId =
    params.get("order_id")

console.log(orderId)



// =========================================
// MAP VARIABLES
// =========================================

let customerMarker
let restaurantMarker
let routeLine

let trackingInterval

let lastStatus = ""


// =========================================
// CUSTOMER LOCATION
// =========================================

const customerLat = 23.0225
const customerLng = 72.5714


// =========================================
// RESTAURANT LOCATION
// =========================================

const restaurantLat = 23.0300
const restaurantLng = 72.5800


// =========================================
// MAP
// =========================================

const map =

    L.map(

        "live-map"

    ).setView(

        [23.0225, 72.5714],

        13
    )

// TILE

L.tileLayer(

    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

    {

        attribution:
            '&copy; OpenStreetMap'
    }

).addTo(map)

// RIDER MARKER

const riderMarker =

    L.marker(

        [23.0225, 72.5714]

    ).addTo(map)



// =========================================
// GPS SOCKET
// =========================================

const gpsSocket =

    new WebSocket(

        "ws://127.0.0.1:8000/ws/gps/"
    )

gpsSocket.onmessage =

    function (e) {

        const data =
            JSON.parse(e.data)

        console.log(data)

        const latitude =
            data.latitude

        const longitude =
            data.longitude

        // UPDATE MARKER

        riderMarker.setLatLng([

            latitude,
            longitude
        ])

        // CENTER MAP

        map.panTo([

            latitude,
            longitude
        ])
    }



// =========================================
// CUSTOMER MARKER
// =========================================

customerMarker = L.marker(

    [customerLat, customerLng],

    {

        icon: L.divIcon({

            html: "🏠",

            className: "",

            iconSize: [40, 40]
        })
    }

).addTo(map)

    .bindPopup("Customer")


// =========================================
// RESTAURANT MARKER
// =========================================

restaurantMarker = L.marker(

    [restaurantLat, restaurantLng],

    {

        icon: L.divIcon({

            html: "🍔",

            className: "",

            iconSize: [40, 40]
        })
    }

).addTo(map)

    .bindPopup("Restaurant")


// =========================================
// RIDER MARKER
// =========================================

riderMarker = L.marker(

    [restaurantLat, restaurantLng],

    {

        icon: L.divIcon({

            html: "🛵",

            className: "",

            iconSize: [45, 45]
        })
    }

).addTo(map)

    .bindPopup("Delivery Boy")


// =========================================
// ROUTE LINE
// =========================================

routeLine = L.polyline(

    [

        [restaurantLat, restaurantLng],

        [customerLat, customerLng]

    ],

    {

        color: "#10b981",

        weight: 6,

        opacity: 0.9
    }

).addTo(map)



// =========================================
// RESET TIMELINE
// =========================================

function resetSteps() {

    document
        .querySelectorAll(".step")
        .forEach(step => {

            step.classList.remove("active")
        })
}


// =========================================
// ACTIVATE STEP
// =========================================

function activateStep(stepId) {

    const step =
        document.getElementById(stepId)

    if (step) {

        step.classList.add("active")
    }
}


// =========================================
// SHOW NOTIFICATION
// =========================================

function showNotification(

    title,
    body

) {

    if (

        Notification.permission ===
        "granted"

    ) {

        new Notification(title, {

            body: body,

            icon:
                "https://cdn-icons-png.flaticon.com/512/3595/3595455.png"
        })
    }
}



// =========================================
// LOAD TRACKING
// =========================================

async function loadTracking() {

    try {

        const response =
            await fetch(

                `http://127.0.0.1:8000/api/orders/track/${orderId}/`
            )

        const data =
            await response.json()

        console.log(data)

        // ORDER ID

        document.getElementById(

            "tracking-order-id"

        ).innerHTML =

            "Order #" + data.id

        // STATUS

        document.getElementById(

            "order-status"

        ).innerHTML = data.status

        // ETA

        document
            .getElementById(
                "eta-text"
            )
            .innerHTML =

            `Estimated Delivery:

        <b>

            ${data.eta_minutes}

            mins

        </b>`

        // RIDER

        if (data.assigned_rider) {

            document.getElementById(

                "rider-name"

            ).innerHTML =

                data.assigned_rider.name

            document.getElementById(

                "rider-mobile"

            ).innerHTML =

                data.assigned_rider.mobile
        }

        // PROGRESS

        const progress =
            document.getElementById(
                "progress-fill"
            )

        if (data.status === "Pending") {

            progress.style.width =
                "20%"
        }

        else if (

            data.status === "Preparing"
        ) {

            progress.style.width =
                "40%"
        }

        else if (

            data.status ===
            "Out For Delivery"
        ) {

            progress.style.width =
                "80%"
        }

        else if (

            data.status ===
            "Delivered"
        ) {

            progress.style.width =
                "100%"

            showToast(
                "🎉 Order Delivered"
            )
        }

    } catch (error) {

        console.log(error)
    }
}

// =========================================
// AUTO REFRESH
// =========================================

loadTracking()

setInterval(() => {

    loadTracking()

}, 5000)



// =========================================
// ETA API
// =========================================

async function loadETA() {

    try {

        const response = await fetch(

            `http://127.0.0.1:8000/api/orders/eta/${orderId}/`
        )

        const data =
            await response.json()

        console.log(data)

        document.getElementById(

            "eta-time"

        ).innerHTML =

            data.eta + " Min"

        document.getElementById(

            "traffic-level"

        ).innerHTML =

            data.traffic

        document.getElementById(

            "distance-away"

        ).innerHTML =

            data.distance + " KM"

    } catch (error) {

        console.log(error)
    }
}


// =========================================
// LIVE RIDER MOVEMENT
// =========================================

async function simulateRiderMovement() {

    try {

        const response = await fetch(

            `http://127.0.0.1:8000/api/orders/simulate-rider/${orderId}/`,

            {
                method: "POST"
            }
        )

        const data =
            await response.json()

        console.log(data)

        const lat =
            data.latitude

        const lng =
            data.longitude


        // MOVE RIDER

        riderMarker.setLatLng([

            lat,
            lng
        ])


        // UPDATE ROUTE

        routeLine.setLatLngs([

            [lat, lng],

            [customerLat, customerLng]
        ])


        // AUTO PAN

        map.panTo([

            lat,
            lng
        ])

    } catch (error) {

        console.log(error)
    }
}


// =========================================
// AUTO LOAD
// =========================================

document.addEventListener(

    "DOMContentLoaded",

    function () {

        // ENABLE NOTIFICATION

        if ("Notification" in window) {

            Notification.requestPermission()
        }

        // INIT MAP

        initMap()

        // INITIAL LOAD

        loadTracking()

        loadETA()

        simulateRiderMovement()

        // AUTO REFRESH

        trackingInterval = setInterval(() => {

            loadTracking()

            loadETA()

            simulateRiderMovement()

        }, 3000)
    }
)


const socket = new WebSocket(

    `ws://127.0.0.1:8000/ws/live-tracking/${orderId}/`
)

socket.onmessage = function (event) {

    const data = JSON.parse(

        event.data
    )

    console.log(data)

    const lat = data.latitude

    const lng = data.longitude

    riderMarker.setLatLng([

        lat,
        lng
    ])

    routeLine.setLatLngs([

        [lat, lng],

        [customerLat, customerLng]
    ])

    map.panTo([

        lat,
        lng
    ])

    document.getElementById(

        "live-status"

    ).innerHTML =

        data.status
}


// =========================================
// CHAT SOCKET
// =========================================

const chatSocket =

    new WebSocket(

        `ws://127.0.0.1:8000/ws/chat/${orderId}/`
    )

// RECEIVE

chatSocket.onmessage = function (e) {

    const data =
        JSON.parse(e.data)

    addMessage(

        data.message,

        data.sender
    )
}

// SEND BUTTON

document.getElementById(

    "send-btn"

).addEventListener(

    "click",

    function () {

        const input =
            document.getElementById(
                "chat-input"
            )

        const message =
            input.value

        if (message.trim() === "")
            return

        chatSocket.send(

            JSON.stringify({

                "message":
                    message,

                "sender":
                    "customer"
            })
        )

        input.value = ""
    }
)

// ADD MESSAGE

function addMessage(

    message,
    sender
) {

    const box =
        document.getElementById(
            "chat-messages"
        )

    const div =
        document.createElement(
            "div"
        )

    div.classList.add(

        "chat-message"
    )

    if (sender === "customer") {

        div.classList.add(
            "customer-message"
        )

    } else {

        div.classList.add(
            "rider-message"
        )
    }

    div.innerHTML = message

    box.appendChild(div)

    // AUTO SCROLL

    box.scrollTop =
        box.scrollHeight
}


// =====================================
// TRAFFIC
// =====================================

document.getElementById(

    "traffic-level"

).innerHTML =

    data.traffic.level
