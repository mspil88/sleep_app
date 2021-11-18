const inputBackground = document.getElementById("input-background");
const gapInput = document.getElementById("gap-input-add");
const allBtns = document.querySelectorAll("button");
const backNextContainer = document.getElementById("next-back-container");
const addGapInputs = document.getElementById("add-gap-inputs");
let gapContainer = [];


function sendData(data) {
    $.ajax({
            url: Flask.url_for('add_gaps_2', {}),
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json"})
            .done(function(result) {console.log("success")})
}

function toggleGapInput() {
    gapInput.classList.toggle("visible");
};

function toggleBackground() {
    inputBackground.classList.toggle("visible");
}

function gapDataObj(gapLength, gotOutBed, triedThought, triedCount) {

    return {
            'gapLength': gapLength,
            'gotOutBed': gotOutBed,
            'triedThought': triedThought,
            'triedCount': triedCount}
}


function getGapData() {
//https://stackoverflow.com/questions/10111668/find-all-elements-whose-id-begins-with-a-common-string/52759092
    const gapLength = document.getElementById("gap-select").value;
    const outOfBed = document.getElementById("checkbox-bed").checked;
    const thoughtSub = document.getElementById("checkbox-sub").checked;
    const counting = document.getElementById("checkbox-count").checked;

    return gapDataObj(gapLength, outOfBed, thoughtSub, counting);

}

function clearInputs() {
    addGapInputs.childNodes.forEach(node => {
        if(node.tagName === "SELECT") {
            node.value = "Length of time of gap";
        } else if(node.tagName === "INPUT") {
            node.checked = false;
        }
    });
}

allBtns.forEach(btn => {
    btn.addEventListener("click", event=> {
        const action = event.currentTarget.id;
        //let gapNum = '';
        if(action.includes("gap-")) {
            toggleGapInput();
            toggleBackground();
            console.log(action);
            //gapNum = action;
        }
        else if(action === "input-add") {
            gapData = getGapData();
            gapContainer.push(gapData);
            toggleGapInput();
            toggleBackground();
            clearInputs();
        }
        else if(action === "input-cancel") {
            toggleGapInput();
            toggleBackground();
            clearInputs();
        }

    })

})

inputBackground.addEventListener("click", ()=> {
    toggleGapInput();
    toggleBackground();
    clearInputs();
})

backNextContainer.addEventListener("click", event => {
    let action = event.target;

    if(action.id == "next6-btn") {
        console.log("next button clicked");

        sendData(gapContainer);
        console.log(gapContainer);
        //location.href = "/feel";

    } else if(action.id == "back-btn") {
        //location.href = "/gaps";
    }

})