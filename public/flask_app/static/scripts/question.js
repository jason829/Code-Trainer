let questionData = [];
let currentUserData = { id: 0, level: 1, question: "", answer: "", correctAnswer: 0 };
const submitButton = document.getElementById("submit-button");

document.addEventListener("DOMContentLoaded", () => {
    /* 
        Fetch questions from server and display them in the container.
    */

    const container = document.getElementById("question-container");

    fetch("/api/questions")
        .then((response) => response.json())
        .then((fetchedData) => {
            questionData = fetchedData; // Store fetched data in global variable
            let id = 0;
            // Display the first ID
            const questionNode = questionData.find((item) => item.id === id);

            if (questionNode) {
                container.textContent = questionNode.question;
                currentUserData.id = questionNode.id;
                currentUserData.level = questionNode.level;
                currentUserData.question = questionNode.question;
            } else {
                container.textContent = "No question";
            }
            console.log(currentUserData)
        })
        .catch((error) => {
            console.error("Error:", error);
            container.textContent = "Failed to load questions.";
        });
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
            console.log(result);

            document.getElementById("msg-container").textContent =
                "Feedback: " + result.feedback;

            // Check if marks is high enough
            if (result.total_mark >= 20) {
                currentUserData.correctAnswer++;
            }

            // Check if user has answered 3 questions correctly, increment level
            if (currentUserData.correctAnswer >= 3) {
                document.getElementById("msg-container").textContent =
                    "You have successfully completed this level!";
                currentUserData.level++;
                currentUserData.correctAnswer = 0;
            }

            /* call function to change question if true */
            await changeQuestion(currentUserData.level);
            console.log(currentUserData)
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

async function changeQuestion(requiredLevel) {
    /* 
        Change the question displayed in the container
    */

    const container = document.getElementById("question-container");
    const questionNode = questionData.filter(
        (item) => item.level === requiredLevel
    );

    if (questionNode) {
        const random = Math.floor(Math.random() * questionNode.length);
        selectedQuestion = questionNode[random];
        container.textContent = selectedQuestion.question;
        currentUserData.id = selectedQuestion.id;
        currentUserData.level = selectedQuestion.level;
        currentUserData.question = selectedQuestion.question;
    } else {
        container.textContent = "No question";
    }
}

function addNewQuestion(level) {
    /* 
        Add new question to the questionData array
    */

    fetch("/json/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ level: level }),
    })
        .then((response) => response.json())
        .then((newQuestion) => {
            console.log(newQuestion);
            // questionData.push(newQuestion);
            console.log("New question added");
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
