const next2Btn = document.getElementById("next2-btn");
const backBtn = document.getElementById("back-btn");
const timeToSleep = document.getElementById("times-to-fall");
const timeGetOut = document.getElementById("get-out-bed");
const inputBackground = document.getElementById("input-background");
const validationContainer = document.getElementById("gap-input-add");

const defaultTimeToSleep = "Time to fall asleep";
const defaultTimeGetOut = "Time to get out of bed";

function toggleBackground() {
    inputBackground.classList.toggle('visible');
}

function toggleValidationContainer() {
    validationContainer.classList.toggle('visible');
}

function timeInOut(tts, tgo) {
    return {'time_to_sleep': tts,
            'time_get_out': tgo
    }
}

function validateInputs(timeToSleepData, defaultTimeToSleep, defaultTimeGetOut) {
    if((timeToSleepData.time_to_sleep === defaultTimeToSleep) || (timeToSleepData.time_get_out === defaultTimeGetOut)) {
        return true;
    }
}

inputBackground.addEventListener("click", ()=> {
    toggleBackground();
    toggleValidationContainer();
})

next2Btn.addEventListener("click", () => {
    console.log("next btn clicked");

    let timeData = timeInOut(timeToSleep.value, timeGetOut.value);

    if(validateInputs(timeData, defaultTimeToSleep, defaultTimeGetOut)) {
        console.log("Invalid inputs");
        console.log(timeData);
        toggleBackground();
        toggleValidationContainer();
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