let questionHeader = document.getElementById("question-header");
let allBtns = document.querySelectorAll("button");
let moodTitle = document.getElementById("mood-title");
const nextBtn = document.getElementById("next-q1-btn");


const questionArray = ["Question 1 of 18", "Question 2 of 18", "Question 3 of 18"]
const questionsArray = ["How often have you been bothered by feeling down, depressed or hopeless?",
                        "How often have you had little interest or pleasure in doing things?",
                        "How often have you been bothered by trouble falling or staying asleep, or sleeping too much?"]

allBtns.forEach(btn => {

    btn.addEventListener("click", (event)=> {
        const action = event.currentTarget.id;
        let questionValue = questionHeader.innerHTML;
        let currentIdx = questionArray.indexOf(questionValue);
        const questionArrayLen = questionsArray.length;

        if((action.includes("next")) && (currentIdx < questionArrayLen-1)) {

            let nextQuestionValue = questionArray[currentIdx+1];
            let nextQuestion = questionsArray[currentIdx+1];
            questionHeader.innerHTML = nextQuestionValue;
            moodTitle.innerHTML = nextQuestion;
            let checkedValue = document.querySelector(".mood-checkbox");
            console.log(checkedValue);
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


