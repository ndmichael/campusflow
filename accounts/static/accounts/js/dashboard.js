document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("dashboardSidebar");
    const sidebarToggle = document.getElementById("sidebarToggle");
    const sidebarOverlay = document.getElementById("sidebarOverlay");

    if (!sidebar || !sidebarToggle) {
        return;
    }


    function openSidebar() {
        sidebar.classList.add("show");

        if (sidebarOverlay) {
            sidebarOverlay.classList.add("show");
        }

        sidebarToggle.setAttribute("aria-expanded", "true");
        document.body.classList.add("sidebar-open");
    }


    function closeSidebar() {
        sidebar.classList.remove("show");

        if (sidebarOverlay) {
            sidebarOverlay.classList.remove("show");
        }

        sidebarToggle.setAttribute("aria-expanded", "false");
        document.body.classList.remove("sidebar-open");
    }


    function toggleSidebar(event) {
        event.stopPropagation();

        if (sidebar.classList.contains("show")) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }


    /* Hamburger button */
    sidebarToggle.addEventListener("click", toggleSidebar);


    /*
     * CLOSE WHEN CLICKING ANYWHERE OUTSIDE SIDEBAR
     *
     * Capture mode makes this fire before other click handlers.
     */
    document.addEventListener(
        "pointerdown",
        function (event) {

            if (window.innerWidth > 991) {
                return;
            }

            if (!sidebar.classList.contains("show")) {
                return;
            }

            const clickedInsideSidebar =
                sidebar.contains(event.target);

            const clickedToggle =
                sidebarToggle.contains(event.target);

            if (!clickedInsideSidebar && !clickedToggle) {
                closeSidebar();
            }

        },
        true
    );


    /* Close when clicking a sidebar link */
    const sidebarLinks =
        sidebar.querySelectorAll("a.sidebar-link");

    sidebarLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            if (window.innerWidth <= 991) {
                closeSidebar();
            }

        });

    });


    /* Escape key */
    document.addEventListener("keydown", function (event) {

        if (event.key === "Escape") {
            closeSidebar();
        }

    });


    /* Return to desktop */
    window.addEventListener("resize", function () {

        if (window.innerWidth >= 992) {
            closeSidebar();
        }

    });

});