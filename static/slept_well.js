var next4Btn = document.getElementById("next4-btn");
let backBtn = document.getElementById("back-btn");

//var yes = document.getElementById("yes");
//var somewhat = document.getElementById("somewhat");
//var no = document.getElementById("no");

console.log("test slept_well.js");

var btns = document.querySelectorAll("button");

console.log(btns);

function sleptWellObj(status) {
    return {'slept_well': status}
}

function sendData(data) {
    $.ajax({
            url: Flask.url_for('slept_well', {}),
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json"})
            .done(function(result) {console.log("success")})
}

btns.forEach((btn) => {
    btn.addEventListener('click', (e) => {
        const actions = e.currentTarget.id;
        if(actions === "yes") {
            let status = sleptWellObj("yes");
            console.log(status);
            sendData(status);
            }
        else if(actions === "somewhat") {
            let status = sleptWellObj("somewhat");
            console.log(status);
            sendData(status);
            }
        else if(actions === "no") {
            let status = sleptWellObj("no");
            console.log(status);
            sendData(status);
            }
        })
        })


//next4Btn.addEventListener("click", () => {
//    console.log("next btn clicked");
//
//    let timeData = timeInOut(timeToSleep.value, timeGetOut.value);
//
//    //console.log(bedTime);
//    //json_data = JSON.stringify(bedWakeData);
//    console.log(timeData);
//    $.ajax({
//        url: Flask.url_for('time_taken', {}),
////        url: '/index',
//        type: "POST",
//        data: JSON.stringify(timeData),
//        contentType: "application/json"})
//        .done(function(result) {console.log("success")})
//})

backBtn.addEventListener("click", () => {
    location.href = "/feel";

})