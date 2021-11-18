var next2Btn = document.getElementById("next2-btn");
let backBtn = document.getElementById("back-btn");
var timeToSleep = document.getElementById("times-to-fall");
var timeGetOut = document.getElementById("get-out-bed");

let defaultTimeToSleep = "Time to fall asleep";
let defaultTimeGetOut = "Time to get out of bed";

console.log("test time_taken.js");

function timeInOut(tts, tgo) {
    return {'time_to_sleep': tts,
            'time_get_out': tgo
    }
}

next2Btn.addEventListener("click", () => {
    console.log("next btn clicked");

    let timeData = timeInOut(timeToSleep.value, timeGetOut.value);

    if((timeData.time_to_sleep === defaultTimeToSleep) || (timeData.time_get_out === defaultTimeGetOut)) {
        console.log("Invalid inputs")
    } else {
        $.ajax({
            url: Flask.url_for('time_taken', {}),
    //        url: '/index',
            type: "POST",
            data: JSON.stringify(timeData),
            contentType: "application/json"})
            .done(function(result) {console.log("success")})
        location.href = "/gaps";}
})

backBtn.addEventListener("click", () => {
    location.href = "/";
})