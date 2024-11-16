document.getElementById("login-container").addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("email").value;
    const password = document.getElementById("password").value;
	print(username);
	print(password);
    const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });

    if (response.status === 200) {
        window.location.href = "/dashboard";
    } else {
        alert("Login fehlgeschlagen! Bitte überprüfen Sie Ihre Anmeldedaten.");
    }
});
