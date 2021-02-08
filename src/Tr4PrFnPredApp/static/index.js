
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
    let file_input = document.getElementById("sequences-input-file");
    let model_select = document.getElementById("model-select");
    let sequences_input = input.value;
    let model = model_select.value;

    if (!sequences_input && file_input.files.length === 0) {

        // set invalid text
        document.getElementById("sequences-invalid").style.display = "block";

        // set invalid textarea form
        input.className = "form-control is-invalid";
    } else {

        // disappear when successful
        document.getElementById("sequences-invalid").style.display = "none";

        // set valid textarea form
        input.className = "form-control";

        if (!sequences_input) {
            let form = document.getElementById("job-form");
            form.action = "/predict/file";
            form.submit();

            fetch("/predict/file", {
                method: "post",
                body: new FormData(form)
            }).then((resp) => {
                return resp.json();
            }).then(function(data) {

                let jobId = data.job_id;
                window.location.href = `/result/page/${jobId}`
            })
        } else {

            let sequences = sequences_input;


            let body = {
                    "data": {
                        "model": model,
                        "sequences": sequences
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

                let jobId = data.job_id;
                window.location.href = `/result/page/${jobId}`
            })
        }
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
    sequenceInput.value = ">KR103_HUMAN\n" +
        "MATSTMSVCSSAYSDSWQVDACPESCCEPPCCATSCCAPAPCLTLVCTPVSCVSSPCCQAACEPSPCQSGCTSSCTPSCCQQSSCQPACCTSSPCQQACCVPVCCKPVCCVPVCCKPVCCKPICCVPVCSGASSSCCQQSSRQPACCTTSCCRPSSSVSLLCRPVCRSTCCVPIPSCCAPASTCQPSCCRPASCVSLLCRPTCSRLSSACCGLSSGQKSSC\n" +
        ">DUX4C_HUMAN\n" +
        "MALPTPSDSTLPAEARGRGRRRRLVWTPSQSEALRACFERNPYPGIATRERLAQAIGIPEPRVQIWFQNERSRQLRQHRRESRPWPGRRGPPEGRRKRTAVTGSQTALLLRAFEKDRFPGIAAREELARETGLPESRIQIWFQNRRARHPGQGGRAPAQAGGLCSAAPGGGHPAPSWVAFAHTGAWGTGLPAPHVPCAPGALPQGAFVSQAARAAPALQPSQAAPAEGISQPAPARGDFAYAAPAPPDGALSHPQAPRWPPHPGKSREDRDPQRDGLPGPCAVAQPGPAQAGPQGQGVLAPPTSQGSPWWGWGRGPQVAGAAWEPQAGAAPPPQPAPPDASAASTDASHPGASQPLQEPGRSSTVTSSLLYELL";
}