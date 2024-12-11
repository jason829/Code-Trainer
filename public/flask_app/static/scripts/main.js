document.addEventListener('DOMContentLoaded', () => {
    /* 
    API call for objects
    display and simple traversal
    */
    const container = document.getElementById('question-container');
    const leftBtn = document.getElementById('left');
    const rightBtn = document.getElementById('right');

    let data = [];
    let currentIndex = 0;

    fetch('/api/questions')
        .then(response => response.json())
        .then(fetchedData => {
            data = fetchedData;
            displayQuestionById(0);
        })
        .catch(error => {
            console.error('Error:', error);
            container.textContent = 'Failed to load questions.';
        });

    function displayQuestionById(id) {
        console.log(data)
        const questionNode = data.find(item => item.id === id);
        if (questionNode) {
            container.textContent = questionNode.question;
            currentIndex = data.indexOf(questionNode);
        } else {
            container.textContent = 'No question';
        }
    }

    leftBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            displayQuestionById(data[currentIndex - 1].id);
        } else {
            console.log('can not go left');
        }
    });

    rightBtn.addEventListener('click', () => {
        if (currentIndex < data.length - 1) {
            displayQuestionById(data[currentIndex + 1].id);
        } else {
            console.log('can not go right');
        }
    });
});

