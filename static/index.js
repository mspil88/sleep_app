var next1Btn = document.getElementById("next1-btn");

var bedTime = document.getElementById("bed-time");
var bedMinute = document.getElementById("bed-minute");
var bedPart = document.getElementById("bed-part");

var outTime = document.getElementById("out-time");
var outMinute = document.getElementById("out-minute");
var outPart = document.getElementById("out-part");

console.log("test index.js");
console.log(`next button ${next1Btn}`);

function bedWakeObj(bt, bm, bp, ot, om, op) {
    return {'inbed': bt + ":" + bm + bp,
            'outbed': ot + ":" + om + op
    }
}


let defaultInBed = "Hour I went to bed:Minute I went to bedam/ pm";
let defaultOutBed =  "Hour I got out of bed:Minute I got out of bedam/ pm";

next1Btn.addEventListener("click", () => {
    console.log("next btn clicked");

    let bedWakeData = bedWakeObj(bedTime.value, bedMinute.value, bedPart.value,
        outTime.value, outMinute.value, outPart.value);

    //console.log(bedTime);
    //json_data = JSON.stringify(bedWakeData);
    console.log(bedWakeData);
    console.log("bed wake data");

    if((bedWakeData.inbed === defaultInBed) || (bedWakeData.outbed === defaultOutBed)) {
        console.log("invalid inputs");
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