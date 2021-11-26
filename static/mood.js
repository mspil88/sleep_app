let questionHeader = document.getElementById("question-header");
let allBtns = document.querySelectorAll("button");
let moodTitle = document.getElementById("mood-title");
const nextBtn = document.getElementById("next-q1-btn");
const questionContainer = document.getElementById("question-container");

dataContainer = [];

//add question number input
function moodSurveyResponses(questionNumber, questionResponse, answer) {
    return {'questionNumber': questionNumber, 'questionResponse': questionResponse,
            'answer': answer, 'score': getScore(questionResponse)}
}

function getScore(questionResponse) {
    if(questionResponse === "Not at all") {
        return 0;
    } else if(questionResponse === "Several days") {
        return 1;
    } else if(questionResponse === "More than half the days") {
        return 2;
    } else if(questionResponse === "Nearly every day") {
        return 3;
    }

}

// handle duplicated answer
function pushQuestionData(questionNumber) {
    for(let i of questionContainer.childNodes) {
        if(i.tagName == "LABEL") {
            let checked = i.childNodes[1].checked;
            if(checked) {
                dataContainer.push(moodSurveyResponses(questionNumber, i.childNodes[0].nodeValue.trim(), checked))}
        }};
   }

function uncheckOptions(questionNumber){
    for(let i of questionContainer.childNodes) {
        if(i.tagName == "LABEL") {
            i.childNodes[1].checked = false;
        }
    }

}

function sumScores(dataContainer) {
    depressionScore = 0;
    anxietyScore = 0;
    for(let i of dataContainer) {
        if(i.questionNumber <= 6) {
            depressionScore += i.score;
        } else {
            anxietyScore += i.score;
        }
    }
    return [depressionScore, anxietyScore];
}

const questionArray = ["Question 2 of 16", "Question 3 of 16", "Question 4 of 16", "Question 5 of 16", "Question 6 of 16",
                       "Question 7 of 16", "Question 8 of 16", "Question 9 of 16", "Question 10 of 16",
                       "Question 11 of 16", "Question 12 of 16", "Question 13 of 16", "Question 14 of 16", "Question 15 of 16",
                       "Question 16 of 16", "Results"]

const questionsArray = [
                        "How often have you had little interest or pleasure in doing things?",
                        "How often have you been bothered by trouble falling or staying asleep, or sleeping too much?",
                        "How often have you been bothered by feeling tired or having little energy?",
                        "How often have you been bothered by poor appetite or overeating?",
                        "How often have you been bothered by feeling bad about yourself, or that you are a failure, or have let yourself or your family down?",
                        "How often have you been bothered by trouble concentrating on things, such as reading the newspaper or watching television?",
                        "How often have you been bothered by moving or speaking so slowly that other people could have noticed, or the opposite - being so fidgety or restless that you have been moving around a lot more than usual?",
                        "How often have you been bothered by feeling nervous, anxious or on edge?",
                        "How often have you been bothered by not being able to stop or control worrying?",
                        "How often have you been bothered by worrying too much about different things?",
                        "How often have you been bothered by having trouble relaxing?",
                        "How often have you been bothered by being so restless that it is hard to sit still?",
                        "How often have you been bothered by becoming easily annoyed or irritable?",
                        "How often have you been bothered by feeling afraid as if something awful might happen?",
                        "Have you been bothered by worrying about any of the following?",
                      ]

allBtns.forEach(btn => {

    btn.addEventListener("click", (event)=> {
        const action = event.currentTarget.id;
        let questionValue = questionHeader.innerHTML;
        let currentIdx = questionArray.indexOf(questionValue);
        const questionArrayLen = questionsArray.length;

        if((action.includes("next")) && (currentIdx < questionArrayLen)) {
            console.log(`Current index ${currentIdx}`);

            //split out data catch and push? Then do not move if empty
            pushQuestionData(currentIdx);
            console.log(dataContainer);
            let nextQuestionValue = questionArray[currentIdx+1];
            let nextQuestion = questionsArray[currentIdx+1];
            questionHeader.innerHTML = nextQuestionValue;
            moodTitle.innerHTML = nextQuestion;
            uncheckOptions(currentIdx);
            let checkedValue = document.querySelector(".mood-checkbox");
            if(currentIdx === 4 || currentIdx === 5 || currentIdx === 6) {
                moodTitle.style.fontSize = "20px";
            } else {
                moodTitle.style.fontSize = "25px";
            }
            if(currentIdx === 14) {
                questionContainer.remove();
                const [depressionScore, anxietyScore] = sumScores(dataContainer);
                console.log(depressionScore);
                console.log(anxietyScore);
            }

            }
        else if((action.includes("back")) && (currentIdx > 0)) {
            let prevQuestionValue = questionArray[currentIdx-1];
            let prevQuestion = questionsArray[currentIdx-1];
            questionHeader.innerHTML = prevQuestionValue;
            moodTitle.innerHTML = prevQuestion;

        }
         }
        )
    }
)


