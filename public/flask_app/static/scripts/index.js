const form = document.getElementById("form");
const confirmUsername = document.getElementById("confirm-username");
const startButton = document.getElementById("start-button");

async function getUsername(event) {
    /* 
    Fetch username data and hold in local storage
    */
    event.preventDefault(); // This stops page reload FYI 
    confirmUsername.disabled = true;
    const username = document.getElementById("username-input").value;
    const password = document.getElementById("password-input").value;

    fetch("/json/username", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user: username, pass: password }),
    }).then((response) => response.json())
        .then((data) => {
            if (data.success == false) {
                console.log("FAILED AUTHENTICATION");
                document.getElementById("msg-container").textContent =
                    "Failed to authenticate";
                return;
            }

            document.getElementById("msg-container").textContent =
                "Successful... Please click on 'Start'";

            localStorage.setItem("user", username)
            localStorage.setItem(username, data.level);

            startButton.disabled = false;
        })
        .catch((e) => {
            console.error("ERROR: " + e);
        })
}