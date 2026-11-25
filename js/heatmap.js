// =====================================
// MAP
// =====================================

const map = L.map(

    'map'

).setView(

    [23.0225, 72.5714],
    12
)

// =====================================
// TILE
// =====================================

L.tileLayer(

    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',

    {

        attribution:
            'BiteOrbit AI'
    }

).addTo(map)

// =====================================
// LOAD HEATMAP
// =====================================

async function loadHeatmap() {

    const response =
        await fetch(

            "http://127.0.0.1:8000/api/orders/delivery-heatmap/"
        )

    const data =
        await response.json()

    const points = []

    data.heatmap.forEach(item => {

        points.push([

            item.latitude,
            item.longitude,
            item.count
        ])
    })

    L.heatLayer(

        points,

        {
            radius: 40,
            blur: 25
        }

    ).addTo(map)
}

loadHeatmap()
