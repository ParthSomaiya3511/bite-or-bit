// =========================================
// GET ORDER ID
// =========================================

const params =
    new URLSearchParams(
        window.location.search
    );

const orderId =
    params.get("order_id");


// =========================================
// MAP VARIABLES
// =========================================

let map;

let riderMarker;

let customerMarker;


// =========================================
// CUSTOMER LOCATION
// =========================================

const customerLocation = {

    lat: 23.0225,

    lng: 72.5714
};


// =========================================
// INITIALIZE MAP
// =========================================

function initMap() {

    map = new google.maps.Map(

        document.getElementById("map"),

        {

            center: customerLocation,

            zoom: 14,

            styles: [

                {
                    elementType: "geometry",

                    stylers: [
                        {
                            color: "#1f2937"
                        }
                    ]
                },

                {
                    elementType: "labels.text.fill",

                    stylers: [
                        {
                            color: "#f8fafc"
                        }
                    ]
                }
            ]
        }
    );

    // CUSTOMER MARKER

    customerMarker =
        new google.maps.Marker({

            position: customerLocation,

            map: map,

            title: "Customer",

            icon: {

                url:
                    "https://maps.google.com/mapfiles/ms/icons/green-dot.png"
            }
        });

    // RIDER MARKER

    riderMarker =
        new google.maps.Marker({

            position: {

                lat: 23.0300,

                lng: 72.5800
            },

            map: map,

            title: "Rider",

            icon: {

                url:
                    "https://maps.google.com/mapfiles/ms/icons/red-dot.png"
            }
        });

    startLiveTracking();
}


// =========================================
// LIVE TRACKING
// =========================================

async function startLiveTracking() {

    setInterval(async () => {

        try {

            const response =
                await fetch(

                    `http://127.0.0.1:8000/api/orders/simulate-delivery/${orderId}/`,

                    {
                        method: "POST"
                    }
                );

            const data =
                await response.json();

            console.log(data);

            if (data.success) {

                const newPosition = {

                    lat:
                        parseFloat(data.latitude),

                    lng:
                        parseFloat(data.longitude)
                };

                riderMarker.setPosition(
                    newPosition
                );

                map.panTo(
                    newPosition
                );

                document.getElementById(
                    "delivery-status"
                ).innerHTML =
                    data.status;

                loadETA();
            }

        } catch (error) {

            console.log(error);
        }

    }, 3000);
}


// =========================================
// LOAD ETA
// =========================================

async function loadETA() {

    try {

        const response =
            await fetch(

                `http://127.0.0.1:8000/api/orders/eta/${orderId}/`
            );

        const data =
            await response.json();

        console.log(data);

        if (data.success) {

            document.getElementById(
                "eta-time"
            ).innerHTML =
                `${data.eta} Min`;
        }

    } catch (error) {

        console.log(error);
    }
}


// =========================================
// START
// =========================================

window.onload = initMap;


