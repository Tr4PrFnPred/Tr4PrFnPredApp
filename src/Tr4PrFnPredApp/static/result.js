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

function pollJobStatus(job_id) {

    return fetch(`/result/${job_id}`, {
        "method": "GET",
        "Accept": "application/json"
    }).then((response) => {
        return response.json();
    })
}

function createPollInterval(job_id, timeout) {
    let pollInterval = setInterval(function() {
        pollJobStatus(job_id).then((response) => {

            let status = response.status;
            if (status === "COMPLETED") {
                clearInterval(pollInterval);
                document.getElementById("waiting").style.display = "none";
                // document.getElementById("results").style.display = "block";
                window.location.reload();
            } else if (status === "ERROR") {
                clearInterval(pollInterval);
            } else {
                document.getElementById("job-status").innerHTML = response.status;
            }
        });
    }, timeout);
}

document.addEventListener("DOMContentLoaded", function(event) {

    document.getElementById("backButton").addEventListener("click", goToHomepage);
    document.getElementById("filter").addEventListener("keyup", filterContent);

    // get the job id via the url
    // regex gets the last string following the last /
    let job_id = window.location.href.match(/[^\/]+$/);

    // poll for results every 10 seconds
    createPollInterval(job_id, 10000);
});
