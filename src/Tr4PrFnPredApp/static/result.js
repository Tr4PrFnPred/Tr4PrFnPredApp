function goToHomepage() {


    window.location.href = "/";
}

document.addEventListener("DOMContentLoaded", function(event) {

    document.getElementById("backButton").addEventListener("click", goToHomepage);
});
