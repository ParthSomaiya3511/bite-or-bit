document.getElementById(

    "pay-btn"

).onclick = async () => {

    const response = await fetch(

        "http://127.0.0.1:8000/api/orders/create-razorpay-order/",

        {

            method:"POST",

            headers:{

                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                order_id:1
            })
        }
    )

    const data = await response.json()

    const options = {

        key:data.key,

        amount:data.amount,

        currency:"INR",

        order_id:data.razorpay_order_id,

        name:"BiteOrbit",

        description:"Food Order",

        handler:async function(payment){

            await fetch(

                "http://127.0.0.1:8000/api/orders/verify-razorpay-payment/",

                {

                    method:"POST",

                    headers:{

                        "Content-Type":"application/json"
                    },

                    body:JSON.stringify({

                        order_id:1,

                        payment_id:
                        payment.razorpay_payment_id,

                        razorpay_order_id:
                        payment.razorpay_order_id,

                        signature:
                        payment.razorpay_signature
                    })
                }
            )

            alert(

                "Payment Successful"
            )
        }
    }

    const rzp = new Razorpay(options)

    rzp.open()
}