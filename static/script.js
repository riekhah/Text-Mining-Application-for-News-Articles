document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submitBtn");

    submitBtn.addEventListener("click", () => {
        // Hide all result divs first
        document.querySelectorAll(".result").forEach(div => {
            div.style.display = "none";
        });

        // Get selected task
        const task = document.getElementById("task").value;

        // Show the corresponding div
        const selectedDiv = document.getElementById(task);
        if (selectedDiv) {
            selectedDiv.style.display = "block";
        }

        // --- Send event to Flask ---f
        fetch("/button_clicked", { method: "POST" })
            .then(response => response.text())
            .then(data => {
                console.log(data); // Browser console
            })
            .catch(error => console.error("Error:", error));

        const newsData = {};

        for (let i = 1; i <= 5; i++) {
            newsData["news" + i] = document.getElementById("news" + i).value;
        }

        // Send to Flask
        fetch("/button_clicked", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(newsData)
            })
            .then(response => response.text())
            .then(data => {
                console.log("Server replied:", data);
            })
            .catch(error => console.error("Error:", error));
    });

});