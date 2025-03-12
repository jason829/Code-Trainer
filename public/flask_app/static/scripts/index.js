const form = document.getElementById("form");
const confirmUsername = document.getElementById("confirm-username");
const startButton = document.getElementById("start-button");
startButton.disabled = true; // disabled button on page load for consistency

document.getElementById("user-form").addEventListener("submit", function (event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirm-password").value.trim();

    if (password != confirmPassword) {
        window.alert("Password and confirm password are not the same");
        return;
    }

    fetch("/json/newUser", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ user: username, pass: password }),
    }).then((response) => response.json())
        .then((data) => {
            if (data.Success == false) {
                window.alert("Username is already taken")
                return;
            }
            window.alert("Successfully created user, you can continue")
            localStorage.setItem("user", username)
            localStorage.setItem(username, 1);

            startButton.disabled = false;
        })
        .catch((e) => {
            console.error("ERROR: " + e);
        }).finally(() => closeForm())
});

function getUsername(event) {
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
                window.alert("Incorrect username/password")
                document.getElementById("msg").textContent =
                    "Failed to authenticate";
                startButton.disabled = true;
                return;
            }

            document.getElementById("msg").textContent =
                "Successful... Please click on 'Start'";

            localStorage.setItem("user", username)
            localStorage.setItem(username, data.level);

            startButton.disabled = false;
        })
        .catch((e) => {
            console.error("ERROR: " + e);
        })
}

function openForm() {
    document.getElementById("new-user-popup").style.display = "block";
}

function closeForm() {
    document.getElementById("new-user-popup").style.display = "none";
}
