// =========================================
// LOAD HEADER
// =========================================

async function loadHeader() {

    const header =
        document.getElementById("header");

    if (!header) return;

    try {

        const response = await fetch(
            "components/header.html"
        );

        const data = await response.text();

        header.innerHTML = data;

        // IMPORTANT
        // HEADER LOAD THAYA PACHI
        // AA FUNCTIONS CALL KARVI

        if (typeof updateNavbarUser === "function") {

            updateNavbarUser();
        }

        if (typeof updateCart === "function") {

            updateCart();
        }

    } catch (error) {

        console.log("Header Load Error:", error);
    }
}


// =========================================
// LOAD FOOTER
// =========================================

async function loadFooter() {

    const footer =
        document.getElementById("footer");

    if (!footer) return;

    try {

        const response = await fetch(
            "components/footer.html"
        );

        const data = await response.text();

        footer.innerHTML = data;

    } catch (error) {

        console.log("Footer Load Error:", error);
    }
}


// =========================================
// AUTO LOAD
// =========================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        loadHeader();

        loadFooter();
    }
);


// =========================================
// LOAD COMPONENTS
// =========================================

async function loadComponent(id, file) {

    const element =
        document.getElementById(id)

    if (!element) return

    const response =
        await fetch(file)

    const data =
        await response.text()

    element.innerHTML = data
}

// =========================================
// AUTO LOAD
// =========================================

window.addEventListener(

    "DOMContentLoaded",

    () => {

        loadComponent(

            "loader-container",

            "../components/loader.html"
        )
    }
)
