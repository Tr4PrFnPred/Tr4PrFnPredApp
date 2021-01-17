function goToHomepage() {

    window.location.href = "/";
}

function addFilterEventListeners() {
    document.getElementById("filter").addEventListener("keyup", filterContent);
}


document.addEventListener("DOMContentLoaded", function(event) {

    document.getElementById("backButton").addEventListener("click", goToHomepage);
});
