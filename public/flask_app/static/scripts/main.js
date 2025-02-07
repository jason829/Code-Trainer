document.addEventListener("DOMContentLoaded", () => {
    /* 
    Fetch questions from server and display them in the container.
    */
    let data = [];
    const container = document.getElementById("question-container");

    fetch("/api/questions")
        .then((response) => response.json())
        .then((fetchedData) => {
            data = fetchedData;
            let id = 0;
            
            // Display the first ID
            const questionNode = data.find((item) => item.id === id);
            if (questionNode) {
                container.textContent = questionNode.question;
                currentIndex = data.indexOf(questionNode);
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

    const userAnswer = document.getElementById("answer-input").value.trim();
    // console.log(userAnswer); // check

    // POST request to server
    fetch("/json", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ answer: userAnswer }),
    })
        .then(data => {
            console.log("Success:", data);
        })
        .catch((error) => {
            console.error("Error:", error);
        });

});

/* function displayQuestionById(id) {
    const questionNode = data.find((item) => item.id === id);
    if (questionNode) {
        container.textContent = questionNode.question;
        currentIndex = data.indexOf(questionNode);
    } else {
        container.textContent = "No question";
    }
} */