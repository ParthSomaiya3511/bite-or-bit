async function loadDashboard() {

    try {

        const response = await fetch(

            "http://127.0.0.1:8000/api/orders/admin-orders/"
        )

        const orders =
            await response.json()

        console.log(orders)

        let revenue = 0
        let pending = 0
        let delivered = 0

        orders.forEach(order => {

            revenue += Number(order.total_price)

            if(order.status === "Pending"){

                pending++
            }

            if(order.status === "Delivered"){

                delivered++
            }
        })

        document.getElementById(
            "total-orders"
        ).innerHTML = orders.length

        document.getElementById(
            "total-revenue"
        ).innerHTML = `₹${revenue}`

        document.getElementById(
            "pending-orders"
        ).innerHTML = pending

        document.getElementById(
            "delivered-orders"
        ).innerHTML = delivered

        // TABLE

        const table =
            document.getElementById(
                "recent-orders"
            )

        table.innerHTML = ""

        orders.slice(0,5).forEach(order => {

            let badge = "pending"

            if(order.status === "Delivered"){

                badge = "delivered"
            }

            if(order.status === "Preparing"){

                badge = "preparing"
            }

            table.innerHTML += `

            <tr>

                <td>
                    #${order.id}
                </td>

                <td>
                    ${order.customer_name}
                </td>

                <td>
                    ₹${order.total_price}
                </td>

                <td>

                    <span class="status ${badge}">

                        ${order.status}

                    </span>

                </td>

            </tr>
            `
        })

        loadCharts(
            revenue,
            pending,
            delivered
        )

    } catch(error){

        console.log(error)
    }
}

/* REVENUE CHART */

function loadCharts(revenue, pending, delivered){

    document.querySelector("#revenueChart").innerHTML = ""

    const revenueChart = new ApexCharts(

        document.querySelector("#revenueChart"),

        {

            chart:{
                type:'area',
                height:350,
                toolbar:{show:false},
                background:'transparent'
            },

            series:[{

                name:'Revenue',

                data:[1200,2100,1800,3200,2800,4500,5200]

            }],

            colors:['#00d084'],

            stroke:{
                curve:'smooth',
                width:4
            },

            grid:{
                borderColor:'#1f2937'
            },

            xaxis:{
                categories:[
                    'Mon',
                    'Tue',
                    'Wed',
                    'Thu',
                    'Fri',
                    'Sat',
                    'Sun'
                ],

                labels:{
                    style:{
                        colors:'#fff'
                    }
                }
            },

            yaxis:{
                labels:{
                    style:{
                        colors:'#fff'
                    }
                }
            },

            theme:{
                mode:'dark'
            }
        }
    )

    revenueChart.render()

    /* STATUS CHART */

    document.querySelector("#statusChart").innerHTML = ""

    const statusChart = new ApexCharts(

        document.querySelector("#statusChart"),

        {

            chart:{
                type:'donut',
                height:350
            },

            series:[
                pending,
                delivered
            ],

            labels:[
                'Pending',
                'Delivered'
            ],

            colors:[
                '#f59e0b',
                '#10b981'
            ],

            theme:{
                mode:'dark'
            }
        }
    )

    statusChart.render()
}

loadDashboard()

setInterval(() => {

    loadDashboard()

},5000)
