let questionData = [];
let currentUserData = { id: 0, level: 1, answer: "" };
const submitButton = document.getElementById("submit-button");

document.addEventListener("DOMContentLoaded", () => {
    /* 
        Fetch questions from server and display them in the container.
        */

    const container = document.getElementById("question-container");

    fetch("/api/questions")
        .then((response) => response.json())
        .then((fetchedData) => {
            questionData = fetchedData;
            let id = 0;
            // Display the first ID
            const questionNode = questionData.find((item) => item.id === id);

            if (questionNode) {
                container.textContent = questionNode.question;
                currentUserData.id = questionNode.id;
                currentUserData.level = questionNode.level;

                currentIndex = questionData.indexOf(questionNode);
            } else {
                container.textContent = "No question";
            }
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
    
    if (currentUserData.answer === "") {
        document.getElementById("msg-container").textContent =
            "Please enter an answer";
        submitButton.classList.toggle("button--loading");
        document.getElementById("submit-button").disabled = false; // Enable button after response
        return;
    }
    
    document.getElementById("submit-button").disabled = true; // Disable button to prevent accidental double submission
    // POST request to server
    fetch("/json", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(currentUserData),
    })
        .then((response) => response.json())
        .then(async (questionResult) => {
            console.log("Success:", questionResult);
            result = questionResult.result;
            console.log(result);
            
            if (!result) {
                /* display hint */
                console.log(questionData[currentUserData.id].hint);
                document.getElementById("msg-container").textContent =
                    "Incorrect answer. HINT: " + questionData[currentUserData.id].hint;
            }
            
            /* call function to change question if true */
            currentUserData.id++;
            await changeQuestion();
        })
        .catch((error) => {
            console.error("Error:", error);
        })
        .finally(() => {
            submitButton.classList.toggle("button--loading");
            document.getElementById("submit-button").disabled = false; // Enable button after response
        });
});

async function changeQuestion() {
    /* 
        Change the question displayed in the container
        */
    const container = document.getElementById("question-container");
    const questionNode = questionData.find(
        (item) => item.id === currentUserData.id
    );

    if (questionNode) {
        container.textContent = questionNode.question;
        currentUserData.id = questionNode.id;
        currentUserData.level = questionNode.level;

        currentIndex = questionData.indexOf(questionNode);
    } else {
        container.textContent = "No question";
    }
}
