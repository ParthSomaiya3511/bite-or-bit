// =========================================
// PAY NOW
// =========================================

document
    .getElementById("pay-btn")

    ?.addEventListener(

        "click",

        async () => {

            try {

                // DEMO ORDER ID

                const orderId =
                    localStorage.getItem(
                        "current_order_id"
                    )

                const amount =
                    localStorage.getItem(
                        "current_order_amount"
                    )

                // CREATE PAYMENT

                const response =
                    await fetch(

                        "http://127.0.0.1:8000/api/orders/payment/",

                        {

                            method: "POST",

                            headers: {

                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                amount,
                                order_id: orderId
                            })
                        }
                    )

                const data =
                    await response.json()

                console.log(data)

                // RAZORPAY

                const options = {

                    key: data.key,

                    amount: data.amount,

                    currency: "INR",

                    name: "BiteOrbit",

                    description:
                        "Food Order Payment",

                    order_id:
                        data.razorpay_order_id,

                    handler: async function (response) {

                        // VERIFY PAYMENT

                        const verifyResponse =
                            await fetch(

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
                            await verifyResponse.json()

                        console.log(verifyData)

                        // SUCCESS

                        if (verifyData.success) {

                            localStorage.setItem(

                                "success_order_id",

                                orderId
                            )

                            // REDIRECT

                            window.location.href =

                                `payment-success.html?order_id=${orderId}`
                        }
                    },

                    theme: {

                        color: "#00c896"
                    }
                }

                const razorpay =
                    new Razorpay(options)

                razorpay.open()

            } catch (error) {

                console.log(error)

                showToast(
                    "❌ Payment Failed"
                )
            }
        }
    )
