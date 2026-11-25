// =========================================
// CART SYSTEM
// =========================================

let cart = JSON.parse(localStorage.getItem("biteorbit_cart")) || [];


// =========================================
// SAVE CART
// =========================================

function saveCart() {

    localStorage.setItem(
        "biteorbit_cart",
        JSON.stringify(cart)
    );
}


// =========================================
// ADD TO CART
// =========================================

function addToCart(name, price, image) {

    const existingItem =
        cart.find(item => item.name === name);

    if (existingItem) {

        existingItem.quantity++;

    } else {

        cart.push({

            name: name,

            price: price,

            image: image,

            quantity: 1
        });
    }

    saveCart();

    updateCart();
}


// =========================================
// UPDATE CART
// =========================================

function updateCart() {

    const cartItems =
        document.getElementById("cart-items");

    const cartTotal =
        document.getElementById("cart-total");

    const cartCount =
        document.getElementById("cart-count");

    if (!cartItems) return;

    cartItems.innerHTML = "";

    let total = 0;

    let count = 0;

    if (cart.length === 0) {

        cartItems.innerHTML = `

            <p class="empty-cart">
                Cart is empty
            </p>

        `;
    }

    cart.forEach((item, index) => {

        total += item.price * item.quantity;

        count += item.quantity;

        cartItems.innerHTML += `

        <div class="cart-product">

            <div class="cart-product-info">

                <img 
                    src="${item.image}" 
                    class="cart-product-image"
                >

                <div>

                    <h6>${item.name}</h6>

                    <small>
                        ₹${item.price}
                    </small>

                </div>

            </div>

            <div class="cart-actions">

                <button onclick="decreaseQty(${index})">
                    -
                </button>

                <span>${item.quantity}</span>

                <button onclick="increaseQty(${index})">
                    +
                </button>

            </div>

        </div>

        `;
    });

    if (cartTotal) {

        cartTotal.innerHTML = `₹${total}`;
    }

    if (cartCount) {

        cartCount.innerHTML = count;
    }
}


// =========================================
// INCREASE QTY
// =========================================

function increaseQty(index) {

    cart[index].quantity++;

    saveCart();

    updateCart();
}


// =========================================
// DECREASE QTY
// =========================================

function decreaseQty(index) {

    if (cart[index].quantity > 1) {

        cart[index].quantity--;

    } else {

        cart.splice(index, 1);
    }

    saveCart();

    updateCart();
}


// =========================================
// LOAD RESTAURANTS
// =========================================

async function loadRestaurants() {

    const restaurantContainer =
        document.getElementById(
            "restaurantContainer"
        );

    if (!restaurantContainer) return;

    try {

        restaurantContainer.innerHTML = `

            <div class="text-center py-5">

                <div class="spinner-border text-success"></div>

            </div>

        `;

        const response = await fetch(
            "http://127.0.0.1:8000/api/restaurants/"
        );

        const restaurants =
            await response.json();

        console.log(restaurants);

        restaurantContainer.innerHTML = "";

        restaurants.forEach((restaurant) => {

            const imageUrl =
                restaurant.image
                    ? restaurant.image.startsWith("http")
                        ? restaurant.image
                        : `http://127.0.0.1:8000${restaurant.image}`
                    : "https://via.placeholder.com/500x300";

            restaurantContainer.innerHTML += `

<div class="col-xl-4 col-lg-6 col-md-6">

    <div class="orbit-restaurant-card">

        <!-- IMAGE -->
        <div class="orbit-image-wrapper">

            <img
                src="${imageUrl}"
                class="orbit-restaurant-image"
            >

            <!-- OVERLAY -->
            <div class="orbit-overlay"></div>

            <!-- TOP BADGES -->
            <div class="orbit-top-badges">

                <span class="orbit-premium-badge">

                    <i class="fa-solid fa-crown"></i>
                    Premium

                </span>

                <span class="orbit-discount-badge">

                    50% OFF

                </span>

            </div>

            <!-- DELIVERY -->
            <div class="orbit-delivery-time">

                <i class="fa-solid fa-bolt"></i>

                ${restaurant.delivery_time || "20-30 Min"}

            </div>

        </div>

        <!-- CONTENT -->
        <div class="orbit-content">

            <!-- TITLE -->
            <div class="d-flex
                        justify-content-between
                        align-items-start
                        mb-2">

                <div>

                    <h3 class="orbit-title">

                        ${restaurant.name}

                    </h3>

                    <p class="orbit-subtitle">

                        Global • Fast Food • Premium

                    </p>

                </div>

                <div class="orbit-rating">

                    <i class="fa-solid fa-star"></i>

                    ${restaurant.rating || "4.8"}

                </div>

            </div>

            <!-- DESCRIPTION -->
            <p class="orbit-description">

                ${restaurant.description || "Experience world-class flavors with ultra-fast delivery and premium quality dishes."}

            </p>

            <!-- FEATURES -->
            <div class="orbit-features">

                <span>

                    <i class="fa-solid fa-motorcycle"></i>

                    Free Delivery

                </span>

                <span>

                    <i class="fa-solid fa-fire"></i>

                    Trending

                </span>

                <span>

                    <i class="fa-solid fa-shield-heart"></i>

                    Hygienic

                </span>

            </div>

            <!-- FOOTER -->
            <div class="orbit-footer">

                <div class="orbit-price-info">

                    <span class="orbit-price-label">

                        Starting From

                    </span>

                    <h4>

                        ₹199

                    </h4>

                </div>

                <button
                    class="orbit-view-btn"

                    onclick="openRestaurant(${restaurant.id})"
                >

                    Explore Menu

                    <i class="fa-solid fa-arrow-right"></i>

                </button>

            </div>

        </div>

    </div>

</div>

`;
        });

    } catch (error) {

        console.log(error);

        restaurantContainer.innerHTML = `

            <div class="text-center text-danger">

                Failed To Load Restaurants

            </div>

        `;
    }
}


// =========================================
// OPEN RESTAURANT PAGE
// =========================================

function openRestaurant(id) {

    window.location.href =
        `restaurant-details.html?id=${id}`;
}


// =========================================
// GET RESTAURANT ID
// =========================================

function getRestaurantId() {

    const params =
        new URLSearchParams(window.location.search);

    return params.get("id");
}


// =========================================
// LOAD RESTAURANT DETAILS
// =========================================

async function loadRestaurantDetails() {

    const restaurantId =
        getRestaurantId();

    if (!restaurantId) return;

    try {

        const response = await fetch(
            `http://127.0.0.1:8000/api/restaurants/${restaurantId}/`
        );

        const restaurant =
            await response.json();

        console.log(restaurant);

        const restaurantName =
            document.getElementById("restaurant-name");

        const restaurantDescription =
            document.getElementById("restaurant-description");

        const restaurantRating =
            document.getElementById("restaurant-rating");

        const restaurantDelivery =
            document.getElementById("restaurant-delivery");

        const restaurantImage =
            document.getElementById("restaurant-image");

        if (restaurantName) {
            restaurantName.innerHTML =
                restaurant.name;
        }

        if (restaurantDescription) {
            restaurantDescription.innerHTML =
                restaurant.description;
        }

        if (restaurantRating) {
            restaurantRating.innerHTML =
                restaurant.rating;
        }

        if (restaurantDelivery) {
            restaurantDelivery.innerHTML =
                restaurant.delivery_time;
        }

        if (restaurantImage) {
            restaurantImage.src =
                restaurant.image.startsWith("http")
                    ? restaurant.image
                    : `http://127.0.0.1:8000${restaurant.image}`;
        }

        // LOAD FOODS
        loadRestaurantFoods(restaurantId);

    } catch (error) {

        console.log(error);
    }
}


// =========================================
// LOAD RESTAURANT FOODS
// =========================================

async function loadRestaurantFoods(restaurantId) {

    const foodsContainer =
        document.getElementById("foods-container");

    if (!foodsContainer) return;

    try {

        foodsContainer.innerHTML = `

            <div class="text-center py-5">

                <div class="spinner-border text-success"></div>

            </div>

        `;

        const response = await fetch(
            `http://127.0.0.1:8000/api/restaurants/${restaurantId}/foods/`
        );

        const foods = await response.json();

        console.log("Foods:", foods);

        foodsContainer.innerHTML = "";

        // EMPTY
        if (foods.length === 0) {

            foodsContainer.innerHTML = `

                <div class="alert alert-dark border-0 rounded-4">

                    No Foods Available

                </div>

            `;

            return;
        }

        foods.forEach((food) => {

            // IMAGE FIX
            const imageUrl =
                food.image
                    ? food.image.startsWith("http")
                        ? food.image
                        : `http://127.0.0.1:8000${food.image}`
                    : "https://via.placeholder.com/400x300";

            foodsContainer.innerHTML += `

            <div class="food-card-premium mb-4">

                <div class="row align-items-center g-4">

                    <div class="col-md-4">

                        <img 
                            src="${imageUrl}"

                            class="food-image-premium"
                        >

                    </div>

                    <div class="col-md-8">

                        <div class="food-content-premium">

                            <span class="food-tag">

                                Bestseller

                            </span>

                            <h3 class="food-title">

                                ${food.name}

                            </h3>

                            <p class="food-description">

                                ${food.description || ""}

                            </p>

                            <div class="food-footer">

                                <h4 class="food-price">

                                    ₹${food.price}

                                </h4>

                                <button 
                                    class="btn btn-success rounded-pill px-4"

                                    onclick="addToCart(
                                        '${food.name}',
                                        ${food.price},
                                        '${imageUrl}'
                                    )"
                                >

                                    <i class="fa-solid fa-cart-plus"></i>

                                    Add To Cart

                                </button>

                            </div>

                        </div>

                    </div>

                </div>

            </div>

            `;
        });

    } catch (error) {

        console.log(error);

        foodsContainer.innerHTML = `

            <div class="alert alert-danger rounded-4">

                Failed To Load Foods

            </div>

        `;
    }
}


// =========================================
// LOAD CHECKOUT PAGE
// =========================================

function loadCheckoutPage() {

    const checkoutItems =
        document.getElementById("checkout-items");

    const subtotal =
        document.getElementById("subtotal");

    const finalTotal =
        document.getElementById("final-total");

    if (!checkoutItems) return;

    checkoutItems.innerHTML = "";

    let total = 0;

    cart.forEach(item => {

        total += item.price * item.quantity;

        checkoutItems.innerHTML += `

        <div class="summary-item">

            <div class="d-flex align-items-center gap-3">

                <img 
                    src="${item.image}" 
                    class="summary-image"
                >

                <div>

                    <h6>${item.name}</h6>

                    <small>
                        Qty: ${item.quantity}
                    </small>

                </div>

            </div>

            <strong>
                ₹${item.price * item.quantity}
            </strong>

        </div>

        `;
    });

    if (subtotal) {

        subtotal.innerHTML = `₹${total}`;
    }

    if (finalTotal) {

        finalTotal.innerHTML = `₹${total + 49}`;
    }
}


async function placeOrder() {

    const customerName =
        document.getElementById(
            "customer-name"
        ).value;

    const customerMobile =
        document.getElementById(
            "customer-mobile"
        ).value;

    const customerAddress =
        document.getElementById(
            "customer-address"
        ).value;

    const customerCity =
        document.getElementById(
            "customer-city"
        ).value;

    const customerPincode =
        document.getElementById(
            "customer-pincode"
        ).value;

    if (
        !customerName ||
        !customerMobile ||
        !customerAddress ||
        !customerCity ||
        !customerPincode
    ) {

        showToast(
            "Please Fill All Fields",
            "warning"
        )

        return;
    }

    let total = 0;

    cart.forEach(item => {

        total += item.price * item.quantity;
    });

    total += 49;

    const orderData = {

        customer_name: customerName,

        mobile: customerMobile,

        address: customerAddress,

        city: customerCity,

        pincode: customerPincode,

        payment_method: "UPI",

        total_price: total,

        items: cart,

        fcm_token:
            localStorage.getItem(
                "fcm_token"
            )
    };

    console.log(orderData);

    try {

        const token =
            localStorage.getItem(
                "biteorbit_access"
            );

        const response = await fetch(

            "http://127.0.0.1:8000/api/orders/",

            {

                method: "POST",

                headers: {

                    "Content-Type":
                        "application/json",

                    "Authorization":
                        `Bearer ${token}`
                },

                body: JSON.stringify(orderData)
            }
        );


        const result =
            await response.json();

        console.log(result);

        // TOKEN INVALID
        if (result.code === "token_not_valid") {

            showToast(
                "Session Expired Please Login Again",
                "warning"
            );

            logoutUser();

            return;
        }

        // SUCCESS
        if (response.ok) {

            showToast(
                "Order Created 🚀",
                "success"
            )

            localStorage.setItem(
                "latest_order_id",
                result.order_id
            );

            startPayment(
                result.order_id,
                total
            );

        } else {

            showToast(
                result.error ||
                result.detail ||
                "Order Failed",
                "error"
            );
        }


    } catch (error) {

        console.log(error);

        showToast(
            "Server Connection Error",
            "error"
        );
    }
}

// =========================================
// PROTECT CHECKOUT
// =========================================

function protectCheckout() {

    const currentPage =
        window.location.pathname;

    if (currentPage.includes("checkout.html")) {

        if (!isLoggedIn()) {

            showToast(
                "Please Login First",
                "warning"
            )

            window.location.href =
                "login.html";
        }
    }
}



// =========================================
// LOAD FOODS
// =========================================

async function loadFoods() {

    const foodContainer =
        document.getElementById(
            "foodContainer"
        );

    if (!foodContainer) return;

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/foods/"
        );

        const foods =
            await response.json();

        console.log(foods);

        foodContainer.innerHTML = "";

        foods.forEach((food) => {

            const imageUrl =
                food.image.startsWith("http")
                    ? food.image
                    : `http://127.0.0.1:8000${food.image}`;

            foodContainer.innerHTML += `

            <div class="col-lg-3 col-md-6 mb-4">

                <div class="card border-0 shadow-lg h-100 rounded-4 overflow-hidden">

                    <img
                        src="${imageUrl}"

                        class="card-img-top"

                        style="
                            height:220px;
                            object-fit:cover;
                        "
                    >

                    <div class="card-body">

                        <h5 class="fw-bold">

                            ${food.name}

                        </h5>

                        <p class="text-muted">

                            ${food.description}

                        </p>

                        <div class="d-flex
                                    justify-content-between
                                    align-items-center">

                            <h5 class="text-success">

                                ₹${food.price}

                            </h5>

                            <button
                                class="btn btn-success rounded-pill"

                                onclick="addToCart(
                                    '${food.name}',
                                    ${food.price},
                                    '${imageUrl}'
                                )"
                            >

                                Add

                            </button>

                        </div>

                    </div>

                </div>

            </div>

            `;
        });

    } catch (error) {

        console.log(error);
    }
}


async function startPayment(orderId, totalPrice) {

    const response = await fetch(

        "http://127.0.0.1:8000/api/orders/payment/",

        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({

                order_id: orderId,

                amount: totalPrice
            })
        }
    )

    const data = await response.json()

    const options = {

        key: data.key,

        amount: data.amount,

        currency: "INR",

        name: "BiteOrbit",

        description: "Food Order",

        order_id: data.razorpay_order_id,

        handler: async function (response) {

            const verify = await fetch(

                "http://127.0.0.1:8000/api/orders/verify-payment/",

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        razorpay_order_id:
                            response.razorpay_order_id,

                        razorpay_payment_id:
                            response.razorpay_payment_id,

                        razorpay_signature:
                            response.razorpay_signature
                    })
                }
            )

            const verifyData =
                await verify.json()

            if (verifyData.success) {

                showToast(
                    "Payment Success",
                    "success"
                )

                window.location.href =
                    "payment-success.html"

            } else {

                showToast(
                    "Payment Failed",
                    "error"
                )
            }
        }
    }

    const rzp =
        new Razorpay(options)

    rzp.open()
}



// =========================================
// LOAD PROFILE
// =========================================

async function loadProfile() {

    if (!window.location.pathname.includes("profile.html")) {
        return;
    }

    const token =
        localStorage.getItem(
            "biteorbit_access"
        );

    if (!token) {

        window.location.href =
            "login.html";

        return;
    }

    try {

        const response = await fetch(

            "http://127.0.0.1:8000/api/users/profile/",

            {

                headers: {

                    "Authorization":
                        `Bearer ${token}`
                }
            }
        );

        const data = await response.json();

        console.log(data);

        // TOKEN EXPIRED
        if (data.code === "token_not_valid") {

            showToast(
                "Session Expired Please Login Again",
                "warning"
            );

            logoutUser();

            return;
        }

        document.getElementById(
            "profile-username"
        ).innerHTML = data.username || "";

        document.getElementById(
            "profile-email"
        ).innerHTML = data.email || "";

        document.getElementById(
            "profile-mobile"
        ).value = data.mobile || "";

        document.getElementById(
            "profile-address"
        ).value = data.address || "";

        document.getElementById(
            "profile-city"
        ).value = data.city || "";

        document.getElementById(
            "profile-pincode"
        ).value = data.pincode || "";

        // PROFILE IMAGE
        if (data.image) {

            document.getElementById(
                "profile-image"
            ).src =

                data.image.startsWith("http")
                    ? data.image
                    : `http://127.0.0.1:8000${data.image}`;
        }

    } catch (error) {

        console.log(error);
    }
}


// =========================================
// UPDATE PROFILE
// =========================================

async function updateProfile() {

    const token =
        localStorage.getItem(
            "biteorbit_access"
        );

    const mobile =
        document.getElementById(
            "profile-mobile"
        ).value;

    const address =
        document.getElementById(
            "profile-address"
        ).value;

    const city =
        document.getElementById(
            "profile-city"
        ).value;

    const pincode =
        document.getElementById(
            "profile-pincode"
        ).value;

    try {

        const response = await fetch(

            "http://127.0.0.1:8000/api/users/profile/",

            {

                method: "PUT",

                headers: {

                    "Content-Type":
                        "application/json",

                    Authorization:
                        `Bearer ${token}`
                },

                body: JSON.stringify({

                    mobile,
                    address,
                    city,
                    pincode
                })
            }
        );

        const data = await response.json();

        console.log(data);

        showToast(
            "Profile Updated",
            "success"
        );

    } catch (error) {

        console.log(error);
    }
}

// =========================================
// LOAD USER ORDERS
// =========================================

async function loadUserOrders() {

    if (!window.location.pathname.includes("orders.html")) {
        return;
    }

    const token =
        localStorage.getItem(
            "biteorbit_access"
        );

    if (!token) {

        window.location.href =
            "login.html";

        return;
    }

    const container =
        document.getElementById(
            "orders-container"
        );

    try {

        const response = await fetch(

            "http://127.0.0.1:8000/api/orders/my-orders/",

            {

                headers: {

                    Authorization:
                        `Bearer ${token}`
                }
            }
        );

        const orders =
            await response.json();

        console.log(orders);

        container.innerHTML = "";

        if (orders.length === 0) {

            container.innerHTML = `

                <div class="alert alert-dark rounded-4">

                    No Orders Found

                </div>

            `;

            return;
        }

        orders.forEach(order => {

            let badge = "secondary";

            if (order.status === "Pending") {
                badge = "warning";
            }

            if (order.status === "Preparing") {
                badge = "info";
            }

            if (order.status === "Out For Delivery") {
                badge = "primary";
            }

            if (order.status === "Delivered") {
                badge = "success";
            }

            container.innerHTML += `

            <div class="card border-0 shadow-lg rounded-4 mb-4">

                <div class="card-body">

                    <div class="d-flex justify-content-between align-items-center mb-3">

                        <h5>
                            Order #${order.id}
                        </h5>

                        <span class="badge bg-${badge}">
                            ${order.status}
                        </span>

                    </div>

                    <p>
                        ${order.customer_name}
                    </p>

                    <p>
                        ₹${order.total_price}
                    </p>

                </div>

            </div>

            `;
        });

    } catch (error) {

        console.log(error);
    }
}


/* =========================================
AUTH SYSTEM
========================================= */

/* CHECK LOGIN */
function isLoggedIn() {

    return localStorage.getItem("biteorbit_access") !== null;
}


/* =========================================
REGISTER USER
========================================= */

async function registerUser() {

    const username =
        document.getElementById("username").value.trim();

    const email =
        document.getElementById("email").value.trim();

    const password =
        document.getElementById("password").value.trim();

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/users/register/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        console.log(data);

        if (response.ok && data.success) {

            showToast(
                "Registration Successful",
                "success"
            );

            window.location.href = "login.html";

        } else {

            showToast(
                data.message || "Registration Failed",
                "error"
            );
        }

    } catch (error) {

        console.log(error);

        showToast(
            "Server Error",
            "error"
        );
    }
}


/* =========================================
LOGIN USER
========================================= */

async function loginUser() {

    const username =
        document.getElementById("username").value.trim();

    const password =
        document.getElementById("password").value.trim();

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/users/login/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username,
                    password
                })
            }
        );

        const data = await response.json();

        console.log(data);

        if (response.ok && data.success) {

            localStorage.setItem(
                "biteorbit_access",
                data.access
            );

            localStorage.setItem(
                "biteorbit_refresh",
                data.refresh
            );

            localStorage.setItem(
                "biteorbit_username",
                data.username
            );

            updateNavbarUser();

            showSuccessAnimation()

            window.location.href = "index.html";

        } else {

            showToast(
                data.message ||
                "Invalid Login",
                "error"
            );
        }

    } catch (error) {

        console.log(error);

        showToast(
            "Server Error",
            "error"
        );
    }
}


/* =========================================
LOGOUT USER
========================================= */

function logoutUser() {

    localStorage.removeItem("biteorbit_access");

    localStorage.removeItem("biteorbit_refresh");

    localStorage.removeItem("biteorbit_username");

    updateNavbarUser();

    window.location.href = "index.html";
}


/* =========================================
UPDATE NAVBAR
========================================= */

function updateNavbarUser() {

    const token =
        localStorage.getItem("biteorbit_access");

    const username =
        localStorage.getItem("biteorbit_username");

    const guestArea =
        document.getElementById("guest-area");

    const loggedArea =
        document.getElementById("logged-user-area");

    const navUsername =
        document.getElementById("nav-username");

    if (!guestArea || !loggedArea) {

        console.log("Navbar elements not found");
        return;
    }

    if (token && username) {

        guestArea.style.display = "none";

        loggedArea.style.display = "block";

        navUsername.innerText = username;

    } else {

        guestArea.style.display = "block";

        loggedArea.style.display = "none";
    }
}


/* =========================================
PROTECT PAGES
========================================= */

function protectPages() {

    const protectedPages = [

        "profile.html",
        "orders.html",
        "checkout.html"

    ];

    const currentPage =
        window.location.pathname
            .split("/")
            .pop();

    if (
        protectedPages.includes(currentPage)
    ) {

        if (!isLoggedIn()) {

            window.location.href =
                "login.html";
        }
    }
}


/* =========================================
AUTO LOAD
========================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        console.log("JS Loaded");

        protectPages();

        loadCheckoutPage();

        loadRestaurants();

        loadFoods();

        loadRestaurantDetails();

        loadProfile();

        loadUserOrders();
    }
);