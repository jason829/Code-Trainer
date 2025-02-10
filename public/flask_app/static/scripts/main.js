let questionData = [];
let currentUserData = {id: 0, level: 1, answer: ""};

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

document.getElementById("submit-button").addEventListener("click", function() {
    /* 
    Submit button event listener
    Send answer in the input text box to the server
    */
    // console.log("clicked");

    currentUserData.answer = document.getElementById("answer-input").value.trim();
    console.log(currentUserData); // check

    // POST request to server
    fetch("/json", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(currentUserData),
    })
        .then(questionData => {
            console.log("Success:", questionData);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});

/* function displayQuestionById(id) {
    const questionNode = questionData.find((item) => item.id === id);
    if (questionNode) {
        container.textContent = questionNode.question;
        currentIndex = questionData.indexOf(questionNode);
    } else {
        container.textContent = "No question";
    }
} */