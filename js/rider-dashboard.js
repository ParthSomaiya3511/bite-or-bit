// =========================================
// GPS SOCKET
// =========================================

const gpsSocket =

    new WebSocket(

        "ws://127.0.0.1:8000/ws/gps/"
    )


// =========================================
// WEBSOCKET
// =========================================

const socket =

    new WebSocket(

        "ws://127.0.0.1:8000/ws/orders/"
    )

socket.onopen = () => {

    console.log(
        "WebSocket Connected"
    )
}

// LIVE ORDER

socket.onmessage = function (e) {

    const data =
        JSON.parse(e.data)

    console.log(data)

    // NEW ORDER

    if (data.type === "new_order") {

        showToast(
            "🔥 New Order Received"
        )

        loadOrders()
    }
}


// =========================================
// AUTH CHECK
// =========================================

const isLoggedIn =

    localStorage.getItem(
        "rider_logged_in"
    )

if (!isLoggedIn) {

    window.location.href =
        "rider-login.html"
}



// =========================================
// ONLINE OFFLINE
// =========================================


const toggle =
    document.getElementById(
        "online-toggle"
    )

toggle.addEventListener(

    "change",

    function () {

        const text =
            document.getElementById(
                "online-text"
            )

        if (this.checked) {

            text.innerHTML =
                "Online"

            showToast(
                "🟢 You are Online"
            )

        } else {

            text.innerHTML =
                "Offline"

            showToast(
                "🔴 You are Offline"
            )
        }
    }
)


// =========================================
// LOAD ORDERS
// =========================================

async function loadOrders() {

    const container =
        document.getElementById(
            "orders-container"
        )

    container.innerHTML = `
    
        <h4 class="text-white">
            Loading Orders...
        </h4>
    `

    try {

        const response =
            await fetch(

                "http://127.0.0.1:8000/api/orders/admin-orders/"
            )

        const orders =
            await response.json()

        console.log(orders)

        container.innerHTML = ""

        // =========================================
        // FILTER ONLY PREPARING
        // =========================================

        const availableOrders =
            orders.filter(order =>

                order.status === "Preparing" &&

                !order.is_accepted
            )

        // =========================================
        // NO ORDERS
        // =========================================

        if (availableOrders.length === 0) {

            container.innerHTML = `

                <div class="empty-box">

                    🚫 No Orders Available

                </div>
            `

            return
        }

        // =========================================
        // SHOW ORDERS
        // =========================================

        availableOrders.forEach(order => {

            container.innerHTML += `

            <div class="order-card"
                 id="order-${order.id}">

                <div>

                    <h4>

                        Order #${order.id}

                    </h4>

                    <p>

                        Customer:
                        ${order.customer_name}

                    </p>

                    <p>

                        Amount:
                        ₹${order.total_price}

                    </p>

                    <p>

                        Status:
                        <strong>

                            ${order.status}

                        </strong>

                    </p>

                    <p>

                        Rider:
                        <strong>

                            ${order.rider_name}

                        </strong>

                    </p>

                </div>

                <div class="order-actions">

                <button

                    class="accept-btn"
                    onclick = "openChat(${order.id})" >
                    Chat
                </button >
                

                    <button
                        class="reject-btn">

                        Reject

                    </button>

                </div>

            </div>
            `
        })

    }

    catch (error) {

        console.log(error)

        container.innerHTML = `

            <div class="empty-box">

                ❌ Server Error

            </div>
        `
    }
}



// =========================================
// ACCEPT ORDER
// =========================================

async function acceptOrder(id) {

    try {

        const response =
            await fetch(

                `http://127.0.0.1:8000/api/orders/accept-order/${id}/`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        rider_id: riderId
                    })
                }
            )

        const data =
            await response.json()

        console.log(data)

        if (data.success) {

            showToast(
                "✅ Order Accepted"
            )

            loadOrders()

            loadStats()

        } else {

            showToast(
                "❌ " + data.message
            )
        }

    } catch (error) {

        console.log(error)
    }
}


// =========================================
// COMPLETE ORDER
// =========================================

async function completeOrder(id) {

    try {

        const response =
            await fetch(

                `http://127.0.0.1:8000/api/orders/complete-order/${id}/`,

                {

                    method: "POST"
                }
            )

        const data =
            await response.json()

        console.log(data)

        if (data.success) {

            showToast(
                "🎉 Order Delivered"
            )

            loadOrders()

            loadStats()
        }

    } catch (error) {

        console.log(error)
    }
}



// =========================================
// TOAST
// =========================================

function showToast(message) {

    const toastBox =
        document.getElementById(
            "toast-box"
        )

    const toast =
        document.createElement("div")

    toast.classList.add("toast")

    toast.innerHTML = message

    toastBox.appendChild(toast)

    setTimeout(() => {

        toast.remove()

    }, 3000)
}


// =========================================
// WEBSOCKET
// =========================================

const socket =
    new WebSocket(

        "ws://127.0.0.1:8000/ws/rider-orders/"
    )

socket.onopen = () => {

    console.log(
        "WebSocket Connected"
    )

    loadOrders()
}

socket.onmessage = function (event) {

    const data =
        JSON.parse(event.data)

    console.log(data)

    // LIVE UPDATE

    loadOrders()

    showToast(
        "🚀 Live Order Update"
    )
}

socket.onclose = () => {

    console.log(
        "WebSocket Closed"
    )
}


// LOAD ONCE

loadOrders()


// REFRESH BUTTON ONLY

document
    .querySelector(".refresh-btn")

    .addEventListener(

        "click",

        function () {

            loadOrders()
        }
    )


// =========================================
// LOAD RIDER
// =========================================

document.getElementById(

    "rider-name"

).innerHTML =

    "Welcome Back, " +

    localStorage.getItem(
        "rider_name"
    )


// =========================================
// RIDER ID
// =========================================

const riderId =

    localStorage.getItem(
        "rider_id"
    )

// =========================================
// LOAD STATS
// =========================================

async function loadStats() {

    try {

        const response =
            await fetch(

                `http://127.0.0.1:8000/api/orders/rider-stats/${riderId}/`
            )

        const data =
            await response.json()

        console.log(data)

        // EARNINGS

        document.getElementById(

            "earnings"

        ).innerHTML =

            "₹" + data.earnings

        // ORDERS

        document.getElementById(

            "orders-count"

        ).innerHTML =

            data.total_orders

        // COMPLETED

        document.getElementById(

            "completed-orders"

        ).innerHTML =

            data.completed_orders

        // STATUS

        document.getElementById(

            "availability-status"

        ).innerHTML =

            data.available
                ? "Online"
                : "Busy"

    } catch (error) {

        console.log(error)
    }
}




// =========================================
// LOGOUT
// =========================================

document
    .querySelector(".logout-btn")

    .addEventListener(

        "click",

        () => {

            localStorage.clear()

            showToast(
                "👋 Logged Out"
            )

            setTimeout(() => {

                window.location.href =
                    "rider-login.html"

            }, 1000)
        }
    )


loadStats()

setInterval(() => {

    loadStats()

    loadOrders()

}, 5000)



// =========================================
// LIVE GPS
// =========================================

function sendLiveGPS() {

    if (navigator.geolocation) {

        navigator.geolocation.watchPosition(

            position => {

                const latitude =
                    position.coords.latitude

                const longitude =
                    position.coords.longitude

                console.log(

                    latitude,
                    longitude
                )

                gpsSocket.send(

                    JSON.stringify({

                        latitude,
                        longitude
                    })
                )

            },

            error => {

                console.log(error)
            },

            {

                enableHighAccuracy: true
            }
        )
    }
}

sendLiveGPS()


// =========================================
// ORDER ID
// =========================================

let activeOrderId = null

// =========================================
// OPEN CHAT
// =========================================

function openChat(orderId) {

    activeOrderId = orderId

    connectChat()
}

// =========================================
// CHAT SOCKET
// =========================================

let riderChatSocket = null

function connectChat() {

    riderChatSocket =

        new WebSocket(

            `ws://127.0.0.1:8000/ws/chat/${activeOrderId}/`
        )

    // RECEIVE

    riderChatSocket.onmessage =

        function (e) {

            const data =
                JSON.parse(e.data)

            addRiderMessage(

                data.message,

                data.sender
            )
        }
}

// SEND

document.getElementById(

    "rider-send-btn"

).addEventListener(

    "click",

    function () {

        const input =
            document.getElementById(
                "rider-chat-input"
            )

        const message =
            input.value

        if (!activeOrderId)
            return

        riderChatSocket.send(

            JSON.stringify({

                "message":
                    message,

                "sender":
                    "rider"
            })
        )

        input.value = ""
    }
)

// ADD MESSAGE

function addRiderMessage(

    message,
    sender
) {

    const box =
        document.getElementById(
            "rider-chat-messages"
        )

    const div =
        document.createElement(
            "div"
        )

    div.classList.add(
        "chat-message"
    )

    if (sender === "rider") {

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

    box.scrollTop =
        box.scrollHeight
}
