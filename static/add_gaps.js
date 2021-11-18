let gapsContainer = document.getElementById("my-gaps-container");
let backNextContainer = document.getElementById("next-back-container");

console.log(gapsContainer);

function getSelectValues(container) {
    let selectArray = [];
    for(let i = 0; i < container.length; i++) {
        if(container[i].tagName == 'SELECT') {
            selectArray.push(container[i].value);
        }
    } return selectArray;
}

function sendData(data) {
    $.ajax({
            url: Flask.url_for('add_gaps', {}),
            type: "POST",
            data: JSON.stringify(data),
            contentType: "application/json"})
            .done(function(result) {console.log("success")})
}



backNextContainer.addEventListener("click", (event) => {
    let action = event.target;
//    let c = getSelectValues(gapsContainer.children);
//    console.log(`printing c ${typeof c}`);

    if(action.id == "next6-btn") {
        console.log("next button clicked");
        let c = getSelectValues(gapsContainer.children);
        console.log(`printing c ${c}`);
        if(c.includes("Length of time")) {
        } else {
            sendData(c);
            console.log(c);
            location.href = "/feel";
        }
    } else if(action.id == "back-btn") {
        location.href = "/gaps";
    }

})
