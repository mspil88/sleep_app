const next1Btn = document.getElementById("next1-btn");
const bedTime = document.getElementById("bed-time");
const bedMinute = document.getElementById("bed-minute");
const bedPart = document.getElementById("bed-part");
const outTime = document.getElementById("out-time");
const outMinute = document.getElementById("out-minute");
const outPart = document.getElementById("out-part");
const inputBackground = document.getElementById("input-background");
const validationContainer = document.getElementById("gap-input-add");
const allBtns = document.querySelectorAll("button");

function toggleBackground() {
    inputBackground.classList.toggle("visible");
}

function toggleValidationContainer() {
    validationContainer.classList.toggle("visible");
}



console.log("test index.js");
console.log(`next button ${next1Btn}`);

function bedWakeObj(bt, bm, bp, ot, om, op) {
    return {'inbed': bt + ":" + bm + bp,
            'outbed': ot + ":" + om + op
    }
}


let defaultInBed = "Hour I went to bed:Minute I went to bedam/ pm";
let defaultOutBed =  "Hour I got out of bed:Minute I got out of bedam/ pm";

function validateInputs(bedWakeData, defaultInBed, defaultOutBed) {
    if((bedWakeData.inbed === defaultInbed) || (bedWakeData.outbed === defaultOutbed)) {
        return true;
    }
}

next1Btn.addEventListener("click", () => {
    console.log("next btn clicked");

    let bedWakeData = bedWakeObj(bedTime.value, bedMinute.value, bedPart.value,
        outTime.value, outMinute.value, outPart.value);

    //console.log(bedTime);
    //json_data = JSON.stringify(bedWakeData);
    console.log(bedWakeData);
    console.log("bed wake data");

    if((bedWakeData.inbed === defaultInBed) || (bedWakeData.outbed === defaultOutBed)) {
        //alert("invalid inputs");
        toggleBackground();
        toggleValidationContainer();
    } else {
        console.log(JSON.stringify(bedWakeData));
        $.ajax({
            url: Flask.url_for('index', {}),
    //        url: '/index',
            type: "POST",
            data: JSON.stringify(bedWakeData),
            contentType: "application/json"})
            .done(function(result) {console.log("success")})
        location.href = "/time_taken";
    }
})

allBtns.forEach(btn => {
    btn.addEventListener("click", event => {
        const action = event.currentTarget.id;
        let bedWakeData = bedWakeObj(bedTime.value, bedMinute.value, bedPart.value,
                                        outTime.value, outMinute.value, outPart.value);

        if((action == "next1-btn") && validateInputs(bedWakeData, defaultInBed, defaultOutBed)) {
            toggleBackGround();
            toggleValidationContainer();

        } else if((action == "next1-btn")) {
            console.log(JSON.stringify(bedWakeData));
            $.ajax({
              url: Flask.url_for('index', {}),
    //        url: '/index',
             type: "POST",
             data: JSON.stringify(bedWakeData),
             contentType: "application/json"})
            .done(function(result) {console.log("success")})
        location.href = "/time_taken";
        }
    })
})


inputBackground.addEventListener("click", () => {
    toggleBackground();
    toggleValidationContainer();

})