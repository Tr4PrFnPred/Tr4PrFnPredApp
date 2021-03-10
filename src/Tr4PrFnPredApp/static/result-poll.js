

function pollJobStatus(job_id) {

    return fetch(`/tr4prfn/result/${job_id}`, {
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
                document.getElementById("job-status").innerHTML = response.status;
            } else {
                document.getElementById("job-status").innerHTML = response.status;
            }
        });
    }, timeout);
}
document.addEventListener("DOMContentLoaded", function(event) {

    // get the job id via the url
    // regex gets the last string following the last /
    let job_id = window.location.href.match(/[^\/]+$/);

    // poll for results every 10 seconds
    createPollInterval(job_id, 10000);
});

