window.onload = function () {

    // Ahmedabad

    const riderLat = 23.0225
    const riderLng = 72.5714

    const customerLat = 23.0300
    const customerLng = 72.5800

    // CREATE MAP

    const map = L.map("map").setView(
        [riderLat, riderLng],
        14
    )

    // TILE

    L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
            attribution:
                "© OpenStreetMap"
        }
    ).addTo(map)

    // RIDER ICON

    const riderIcon = L.icon({

        iconUrl:
            "https://cdn-icons-png.flaticon.com/512/2972/2972185.png",

        iconSize: [50, 50]
    })

    // CUSTOMER ICON

    const customerIcon = L.icon({

        iconUrl:
            "https://cdn-icons-png.flaticon.com/512/1046/1046784.png",

        iconSize: [45, 45]
    })

    // MARKERS

    const riderMarker = L.marker(
        [riderLat, riderLng],
        { icon: riderIcon }
    ).addTo(map)

    const customerMarker = L.marker(
        [customerLat, customerLng],
        { icon: customerIcon }
    ).addTo(map)

    // ROUTE LINE

    const route = L.polyline(

        [
            [riderLat, riderLng],
            [customerLat, customerLng]
        ],

        {

            color: "#00ff88",
            weight: 6
        }

    ).addTo(map)

    map.fitBounds(route.getBounds())

    // ANIMATION

    let lat = riderLat
    let lng = riderLng

    setInterval(() => {

        lat += 0.0002
        lng += 0.0002

        riderMarker.setLatLng([lat, lng])

    }, 1000)
}


const orderId =
localStorage.getItem(
    "track_order_id"
)

const socket = new WebSocket(

    `ws://127.0.0.1:8000/ws/order/${orderId}/`
)

socket.onmessage = function(event){

    const data =

    JSON.parse(event.data)

    console.log(data)

    if(data.status){

        document.getElementById(

            "order-status"

        ).innerHTML =

        data.status
    }

    if(data.eta){

        document.getElementById(

            "eta"

        ).innerHTML =

        data.eta + " mins"
    }
}