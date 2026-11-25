async function loadAdminOrders() {


    const container =
        document.getElementById(
            "admin-orders-container"
        );

    if (!container) {
        console.log("Container Not Found");
        return;
    }

    try {

        container.innerHTML = `

        <div class="text-center text-white">

            Loading Orders...

        </div>

    `;

        const response = await fetch(

            "http://127.0.0.1:8000/api/orders/admin-orders/"
        );

        const orders = await response.json();

        console.log("ORDERS:", orders);

        container.innerHTML = "";

        // EMPTY
        if (!orders.length) {

            container.innerHTML = `

            <div class="alert alert-warning">

                No Orders Found

            </div>

        `;

            return;
        }

        orders.forEach(order => {

            container.innerHTML += `

        <div class="order-card">

            <div class="d-flex
                        justify-content-between
                        align-items-center">

                <div>

                    <h4>

                        Order #${order.id}

                    </h4>

                    <p>

                        ${order.customer_name}

                    </p>

                    <p>

                        ₹${order.total_price}

                    </p>

                    <p>

                        Status:
                        <strong>${order.status}</strong>

                    </p>

                    <p>

                        Rider:
                        <strong>

                            ${order.assigned_rider_name || "Not Assigned"}

                        </strong>

                    </p>

                </div>

                <div style="width:220px;">

                    <select
                        class="form-select"

                        onchange="updateStatus(
                            ${order.id},
                            this.value
                        )"
                    >

                        <option value="Pending"
                            ${order.status === "Pending" ? "selected" : ""}
                        >
                            Pending
                        </option>

                        <option value="Preparing"
                            ${order.status === "Preparing" ? "selected" : ""}
                        >
                            Preparing
                        </option>

                        <option value="Out For Delivery"
                            ${order.status === "Out For Delivery" ? "selected" : ""}
                        >
                            Out For Delivery
                        </option>

                        <option value="Delivered"
                            ${order.status === "Delivered" ? "selected" : ""}
                        >
                            Delivered
                        </option>

                    </select>

                </div>

            </div>

        </div>

        `;
        });

    } catch (error) {

        console.log("ERROR:", error);

        container.innerHTML = `

        <div class="alert alert-danger">

            Failed To Load Orders

        </div>

    `;
    }


}

// =========================================
// UPDATE STATUS
// =========================================

async function updateStatus(id, status) {


    try {

        const response = await fetch(

            `http://127.0.0.1:8000/api/orders/update-status/${id}/`,

            {

                method: "PUT",

                headers: {

                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({

                    status: status
                })
            }
        );

        const data =
            await response.json();

        console.log(data);

        alert("Status Updated");

    } catch (error) {

        console.log(error);
    }


}

// =========================================
// AUTO LOAD
// =========================================

document.addEventListener(


    "DOMContentLoaded",

    function () {

        loadAdminOrders();

        // AUTO REFRESH
        setInterval(() => {

            loadAdminOrders();

        }, 5000);

    }
);