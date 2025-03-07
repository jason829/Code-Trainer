let questionData;
let currentUserData = { level: 1, question: "", answer: "", correctAnswer: 0 };
const submitButton = document.getElementById("submit-button");
const questionContainer = document.getElementById("question-container");

document.addEventListener("DOMContentLoaded", () => {
    /* 
        Initial requests on page load
    */
    getQuestion();
});

submitButton.addEventListener("click", function () {
    /* 
        Submit button event listener
        Send answer in the input text box to the server
    */
    let result;
    currentUserData.answer = document.getElementById("answer-input").value.trim();

    // Check if the input is empty
    if (currentUserData.answer === "") {
        document.getElementById("msg-container").textContent =
            "Please enter an answer";
        submitButton.classList.toggle("button--loading");
        return;
    }

    document.getElementById("submit-button").disabled = true; // Disable button to prevent accidental double submission
    document.getElementById("msg-container").textContent = "Please wait while we check your answer...";

    // POST request to server
    fetch("/json/mark", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(currentUserData),
    })
        .then((response) => response.json())
        .then(async (questionResult) => {
            console.log("Successful response");
            result = questionResult.result;
            console.log(result)

            document.getElementById("msg-container").textContent =
                "Feedback: " + result.feedback;

            // Check mark thresholds
            if (result.total_mark >= 20) currentUserData.correctAnswer++;

            if (result.total_mark <= 10) currentUserData.correctAnswer--;

            // Check if user has answered 3 questions correctly, increment level
            if (currentUserData.correctAnswer >= 3) {
                document.getElementById("msg-container").textContent =
                    "You have successfully completed this level!";
                currentUserData.level++;
                currentUserData.correctAnswer = 0;
            } else if (currentUserData.correctAnswer <= -3) {
                currentUserData.level--;
                if (currentUserData.level <= 0) {
                    currentUserData.level = 1;
                }
                currentUserData.correctAnswer = 0;
            }

            /* call function to change question if true */
            await getQuestion();
        })
        .catch((error) => {
            console.error("Error:", error);
        })
        .finally(() => {
            // Enable button and remove loading animation
            submitButton.classList.toggle("button--loading");
            document.getElementById("submit-button").disabled = false;
        });
});

async function getQuestion() {
    /* 
        Change the question displayed in the container
    */
    fetch(`/api/questions?level=${currentUserData.level}`)
        .then((response) => response.json())
        .then((fetchedData) => {
            questionData = fetchedData; // Store fetched data in global variable

            if (questionData) {
                questionContainer.textContent = questionData.question;
                currentUserData.question = questionData.question;
            } else {
                questionContainer.textContent = "No question";
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            questionContainer.textContent = "Failed to load questions.";
        });
}


// DELETE MAYBE ---- REFACTORING :(
// async function addNewQuestion(level) {
//     /* 
//         Add new question to the questionData array
//     */

//     fetch("/json/create", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json",
//         },
//         body: JSON.stringify({ level: level }),
//     })
//         .then((response) => response.json())
//         .then((newQuestion) => {
//             if (newQuestion.level === 0) {
//                 console.error("Error has occurred server side");
//                 return;
//             }

//             console.log(newQuestion);
//             // questionData.push(newQuestion);
//             console.log("New question added");
//         })
//         .catch((error) => {
//             console.error("Error:", error);
//         });
// }
