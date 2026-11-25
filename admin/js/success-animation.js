// =========================================
// LOAD SUCCESS COMPONENT
// =========================================

async function loadSuccessAnimation() {

    const response = await fetch(

        "components/success-animation.html"
    );

    const html = await response.text();

    document.body.insertAdjacentHTML(

        "beforeend",

        html
    );
}


// =========================================
// INIT
// =========================================

loadSuccessAnimation();


// =========================================
// SHOW SUCCESS
// =========================================

function showSuccessAnimation() {

    const overlay =
        document.getElementById(
            "success-overlay"
        );

    overlay.classList.add("show");


    // CONFETTI

    confetti({

        particleCount: 250,

        spread: 120,

        origin: { y: 0.6 }
    });


    // AUTO REDIRECT

    setTimeout(() => {

        window.location.href =
            "rider-dashboard.html";

    }, 3500);

}
