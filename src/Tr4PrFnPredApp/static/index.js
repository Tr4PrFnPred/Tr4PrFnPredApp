
/**
 * Switches tabs
 *
 * @param e event
 * @param tab name of tab to switch
 */
function switchTabs(e, tab) {

    // set new active tab
    let nav_tabs = document.getElementsByClassName("nav-item");
    for (let element of nav_tabs) {
        element.className = "nav-item";
    }
    e.currentTarget.parentNode.className = "nav-item active";

    // switch page content based on new tab
    let tabs =  document.getElementsByClassName("tab");
    for (let element of tabs) {
        element.style.display = 'none';
    }
    document.getElementById(tab).style.display = 'block';
}


function submitSequence(e) {

    let input = document.getElementById("sequences-input");
    let model_select = document.getElementById("model-select");
    let sequences = input.value;
    let model = model_select.value;

    if (!sequences) {

        // set invalid text
        document.getElementById("sequences-invalid").style.display = "block";

        // set invalid textarea form
        input.className = "form-control is-invalid";
    } else {

        // disappear when successful
        document.getElementById("sequences-invalid").style.display = "none";

        // set invalid textarea form
        input.className = "form-control";

        // remove all white space
        sequences = sequences.replace(/\s/g, '');
        //TODO: REMOVE NEXT LINE IN THE FUTURE - THIS IS JUST FOR TESTING
        let seq_number = sequences.split(",").map(value => parseInt(value));

        let body = {
                "data": {
                    "model": model,
                    "sequences": seq_number
                }
            };

        console.info(JSON.stringify(body));

        fetch("/predict", {
            method: 'post',
            headers: {
                'Content-Type': 'application/json'
            },
            cache: 'no-cache',
            body: JSON.stringify(body)
        }).then(function(response) {
            return response.json();
        }).then(function(data) {

            let jobId = data.data.jobId;
            window.location.href = `/result/page/${jobId}`
        })
    }
}

function searchResult(e) {
    let jobIdInput = document.getElementById("jobid");
    let jobId = jobIdInput.value;

    // redirect page to the result page
    window.location.href = `/result/page/${jobId}`;
}

function fillExample() {

    let sequenceInput = document.getElementById("sequences-input");
    sequenceInput.value = "15, 256, 4, 2, 7, 3766, 5, 723, 36, 71, 43, 530, 476, 26, 400, 317, 46, 7, 4, 12118, 1029, 13, 104, 88, 4, 381, 15, 297, 98, 32, 2071, 56, 26, 141, 6, 194, 7486, 18, 4, 226, 22, 21, 134, 476, 26, 480, 5, 144, 30, 5535, 18, 51, 36, 28, 224, 92, 25, 104, 4, 226, 65, 16, 38, 1334, 88, 12, 16, 283, 5, 16, 4472, 113, 103, 32, 15, 16, 5345, 19, 178, 32";
}