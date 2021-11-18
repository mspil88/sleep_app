let gapSubmit = document.getElementById("gap-submit");
let nextBtn3 = document.getElementById("next3-btn");
let backBtn = document.getElementById("back-btn");
let gapNumber = 0;

gapSubmit.addEventListener("click", () => {
    let gapEntry = document.getElementById("gap-entry").value;
    let numberOfGaps = gapEntry;
    gapNumber = numberOfGaps;
    console.log(numberOfGaps);
    if((numberOfGaps === '')) {
        return
    } else {
        sendData(numberOfGaps);
    }
})

nextBtn3.addEventListener("click", () => {
    if(gapNumber == 0) {
        location.href = "/feel";
    } else {
        location.href = "/add_gaps";
    }
})

function sendData(data) {
    $.ajax({
            url: Flask.url_for('gaps', {}),
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json"})
            .done(function(result) {console.log("success")})
}

backBtn.addEventListener("click", () => {
    location.href="/time_taken";

})