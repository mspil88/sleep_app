var moodBtns = document.querySelectorAll("button");
const moodContainer = document.getElementById("hold-btns");
const moveBtnContainer = document.getElementById("next-back-container");

let moodsToRender = moods;

function countButtons(container) {
    let numButtons = 0;
    for(let i = 0; i < container.length; i++) {
        let child = container[i];
        if(child.id.includes("btn")) {
            numButtons ++;
        }
    } return numButtons;
}


function getMyMoods(container) {
    let myMoods = [];
    for(let i = 0; i < container.length; i++) {
        let child = container[i];
        if((child.id.includes("btn")) && (child.name != '')) {
            myMoods.push(child.name);
        }
    } return myMoods;
}

function createButton(addButton, moodValue) {
    let newButton = document.createElement("button");
    newButton.className = "mood-btn";
    newButton.id = moodValue + "-btn";
    newButton.innerHTML = moodValue;
    newButton.name = moodValue;
    return newButton
}

function sendData(data) {
    $.ajax({
            url: Flask.url_for('feel', {}),
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json"})
            .done(function(result) {console.log("success")})
}

function buttonStruct(buttonName) {
    return {buttonName: buttonName + "-btn"}
}

function clearButtons(parent) {
    for(let i of parent.children) {
        if((i.name !== undefined )) {
            if(!i.name.includes("add")) {
                i.remove();}
        }
    }
}

Array.prototype.unique = function() {
    return [...new Set(this)];
}

let moodSet = [];

function createMyMoodPackage(selectedMoods, tracked_moods) {
    return {'selected_moods': selectedMoods,
            'tracked_moods': tracked_moods
    }
}


moodContainer.addEventListener('click', (event) => {
    let action = event.target;

    if(action.id.includes("-btn")) {
    let buttonCount = countButtons(moodContainer.children);
    console.log(`Number of buttons in moodContainer ${buttonCount}`)
        if((action.id == "add-btn") && (buttonCount < 12)) {
            console.log("add-btn clicked!");
            var moodValue = document.getElementById("mood-entry").value;
            if(moodValue.trim() == "") {
            } else {
                var addButton = document.getElementById("add-btn");
                var newButton = createButton(addButton, moodValue);
                moodContainer.insertBefore(newButton, addButton);

                }
        } else if((action.type != null) && (!moodSet.includes(action.name))) {
            moodSet.push(action.name);
            console.log(action.type);
            action.style.background = "palevioletred";
            console.log(moodSet.unique());

        } else if((action.type != null) && (moodSet.includes(action.name))) {
            moodSet = moodSet.filter(mood => mood != action.name)
            action.style.background = "white";
        }
    }
})
// need to fully replace in render function
moodContainer.addEventListener("dblclick", (event) => {
    let action = event.target;
    console.log("check");
    if((action.id.includes("btn") && ((!action.name.includes("back")) || (!action.name.includes("next"))))) {
        console.log("check2");
        moodsToRender = moodsToRender.filter(mood => mood != action.name)
        console.log(moodsToRender);
        renderButtons(moodsToRender);
        clearButtons(moodContainer);
    }
})

moveBtnContainer.addEventListener("click", (event) => {
    let action = event.target;

    if(action.id == "next5-btn") {
        console.log("next button hit!");
        let myTrackedMoods = getMyMoods(moodContainer.children);
        let myMoodPackage = createMyMoodPackage(moodSet.unique(), myTrackedMoods.unique());
        sendData(myMoodPackage);
        location.href = "/slept_well";
    } else if(action.id == "back-btn") {
        location.href = "/add_gaps"
    }

})