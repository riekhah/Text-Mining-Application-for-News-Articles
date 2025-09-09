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

        // Collect values from inputs with ids News1, News2, ... News5
        const newsData = {};
        for (let i = 1; i <= 5; i++) {
            const el = document.getElementById("News " + i);
            if (el) newsData["News " + i] = el.value;
        }

        // Send JSON to Flask
        fetch("/button_clicked", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(newsData)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Server replied:", data);

                const results = data.results;

                // Helper to build output for all tasks
                const buildOutput = (task) => {
                    let output = "";
                    if (task === "similarity") {
                        // Handle similarity separately
                        const sims = results.similarity;
                        for (const newsA in sims) {
                            output += `${newsA} similarities:\n`;
                            for (const newsB in sims[newsA]) {
                                output += `   → ${newsB}: ${sims[newsA][newsB]}\n`;
                            }
                            output += "\n";
                        }
                    } else {
                        // Handle per-news outputs
                        for (let i = 1; i <= 5; i++) {
                            const key = "News " + i;
                            if (results[key]) {
                                output += `\n${key}:\n`;

                                if (task === "classification") {
                                    output += `  Category → ${results[key].prediction}\n`;
                                } else if (task === "sentiment") {
                                    output += `  Sentiment → ${JSON.stringify(results[key].sentiment)}\n`;
                                } else if (task === "extract") {
                                    output += `  Entities → ${JSON.stringify(results[key].entities)}\n`;
                                } else if (task === "summary") {
                                    output += `  Summary → ${results[key].summary.join(" | ")}\n`;
                                } else if (task === "trend") {
                                    output += "  Top Words:\n";
                                    results[key].trends.forEach(t => {
                                        output += `    ${t[0]}: ${t[1]}\n`;
                                    });
                                }
                            }
                        }
                    }
                    return output;
                };

                // Update the correct section
                if (task === "classification") {
                    document.getElementById("classification_output").innerText = buildOutput(task);
                } else if (task === "sentiment") {
                    document.getElementById("sentiment_output").innerText = buildOutput(task);
                } else if (task === "extract") {
                    document.getElementById("extract_output").innerText = buildOutput(task);
                } else if (task === "summary") {
                    document.getElementById("summary_output").innerText = buildOutput(task);
                } else if (task === "trend") {
                    document.getElementById("trend_output").innerText = buildOutput(task);
                } else if (task === "similarity") {
                    document.getElementById("similarity_output").innerText = buildOutput(task);
                }
            })
            .catch(error => console.error("Error:", error));
    });
});