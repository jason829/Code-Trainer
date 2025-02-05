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
            displayQuestionById(0);
        })
        .catch((error) => {
            console.error("Error:", error);
            container.textContent = "Failed to load questions.";
        });

    function displayQuestionById(id) {
        console.log(data);
        const questionNode = data.find((item) => item.id === id);
        if (questionNode) {
            container.textContent = questionNode.question;
            currentIndex = data.indexOf(questionNode);
        } else {
            container.textContent = "No question";
        }
    }
});

document.getElementById("submit-button").addEventListener("click", function() {
    /* 
    Submit button event listener
    Send answer in the input text box to the server
    */
    console.log("clicked");
    

});
