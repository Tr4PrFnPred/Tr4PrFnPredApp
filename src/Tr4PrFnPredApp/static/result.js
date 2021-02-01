function goToHomepage() {

    window.location.href = "/";
}

function filterContent() {

    let filter = document.getElementById("filter");
    let filterValue = filter.value.toUpperCase();

    let table = document.getElementById("resultTable");
    let rows = table.getElementsByTagName("tr");
    for (let i = 0; i < rows.length; i++) {
        if (rows[i].hasAttribute("entry")) {
            if (rows[i].attributes.entry.value.toUpperCase().indexOf(filterValue) > -1) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}


function addFilterEventListeners() {
    document.getElementById("filter").addEventListener("keyup", filterContent);
}


document.addEventListener("DOMContentLoaded", function(event) {

    document.getElementById("backButton").addEventListener("click", goToHomepage);
    addFilterEventListeners();
});
