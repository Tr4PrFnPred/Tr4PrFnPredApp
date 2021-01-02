function goToHomepage() {


    window.location.href = "/";
}

function filterContent() {

    let filter = document.getElementById("filter");
    let filterValue = filter.value;

    let table = document.getElementById("resultTable");
    let rows = table.getElementsByTagName("tr");
    for (let i = 0; i < rows.length; i++) {
        let col = rows[i].getElementsByTagName("td")[0];
        if (col) {
            let txtValue = col.textContent || col.innerText;
            if (txtValue.toUpperCase().indexOf(filterValue) > -1) {
                rows[i].style.display = "";
            } else {
                rows[i].style.display = "none";
            }
        }
    }
}

document.addEventListener("DOMContentLoaded", function(event) {

    document.getElementById("backButton").addEventListener("click", goToHomepage);
    document.getElementById("filter").addEventListener("keyup", filterContent);
});
