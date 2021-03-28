
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


function showInvalidInput(input, message) {

    // set invalid text
    let invalidSequenceMessage = document.getElementById("sequences-invalid");
    invalidSequenceMessage.style.display = "block";
    invalidSequenceMessage.innerHTML = message;

    // set invalid textarea form
    input.className = "form-control is-invalid";
}

function displayLoadingIcon() {

    document.getElementById("loading-icon").style.display = "inline-block";
}

function hideLoadingIcon() {

    document.getElementById("loading-icon").style.display = "none";
}

function toggleSubmitButton() {

    document.getElementById("submit-button").disabled =
        !document.getElementById("submit-button").disabled;
}


function submitSequence(e) {

    let input = document.getElementById("sequences-input");
    let file_input = document.getElementById("sequences-input-file");
    let model_select = document.getElementById("model-select");
    let sequences_input = input.value;
    let model = model_select.value;

    displayLoadingIcon();
    toggleSubmitButton();

    if (!sequences_input && file_input.files.length === 0) {

        showInvalidInput(input, "Must not be empty");
        hideLoadingIcon();
        toggleSubmitButton();
    } else {

        document.getElementById("sequences-invalid").style.display = "none";

        // set valid textarea form
        input.className = "form-control";

        if (!sequences_input) {
            let form = document.getElementById("job-form");
            form.action = "/tr4prfn/predict/file";
            form.submit();

            fetch("/tr4prfn/predict/file", {
                method: "post",
                body: new FormData(form)
            }).then((resp) => {
                return resp.json();
            }).then(function(data) {
                if (data.error) {
                    showInvalidInput(input, data.error);
                    hideLoadingIcon();
                    toggleSubmitButton();
                } else {
                    redirectToResultPage(data);
                }
            })
        } else {

            let body = {
                "data": {
                    "model": model,
                    "sequences": sequences_input
                }
            };

            fetch("/tr4prfn/predict", {
                method: 'post',
                headers: {
                    'Content-Type': 'application/json'
                },
                cache: 'no-cache',
                body: JSON.stringify(body)
            }).then(function (response) {
                return response.json();
            }).then(function(data) {
                if (data.error) {
                    showInvalidInput(input, data.error);
                    hideLoadingIcon();
                    toggleSubmitButton();
                } else {
                    redirectToResultPage(data);
                }
            });
        }
    }
}

function redirectToResultPage(data) {

    let jobId = data.job_id;
    window.location.href = `/tr4prfn/result/page/${jobId}`
}

function searchResult(e) {
    let jobIdInput = document.getElementById("jobid");
    let jobId = jobIdInput.value;

    // redirect page to the result page
    window.location.href = `/tr4prfn/result/page/${jobId}`;
}

function fillExample() {

    let sequenceInput = document.getElementById("sequences-input");
    sequenceInput.value = ">KR103_HUMAN\n" +
        "MATSTMSVCSSAYSDSWQVDACPESCCEPPCCATSCCAPAPCLTLVCTPVSCVSSPCCQAACEPSPCQSGCTSSCTPSCCQQSSCQPACCTSSPCQQACCVPVCCKPVCCVPVCCKPVCCKPICCVPVCSGASSSCCQQSSRQPACCTTSCCRPSSSVSLLCRPVCRSTCCVPIPSCCAPASTCQPSCCRPASCVSLLCRPTCSRLSSACCGLSSGQKSSC\n" +
        ">DUX4C_HUMAN\n" +
        "MALPTPSDSTLPAEARGRGRRRRLVWTPSQSEALRACFERNPYPGIATRERLAQAIGIPEPRVQIWFQNERSRQLRQHRRESRPWPGRRGPPEGRRKRTAVTGSQTALLLRAFEKDRFPGIAAREELARETGLPESRIQIWFQNRRARHPGQGGRAPAQAGGLCSAAPGGGHPAPSWVAFAHTGAWGTGLPAPHVPCAPGALPQGAFVSQAARAAPALQPSQAAPAEGISQPAPARGDFAYAAPAPPDGALSHPQAPRWPPHPGKSREDRDPQRDGLPGPCAVAQPGPAQAGPQGQGVLAPPTSQGSPWWGWGRGPQVAGAAWEPQAGAAPPPQPAPPDASAASTDASHPGASQPLQEPGRSSTVTSSLLYELL";
}