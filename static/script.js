document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("screening-form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const jsonData = Object.fromEntries(formData.entries());

        // Convert values to integers
        for (let key in jsonData) {
            jsonData[key] = parseInt(jsonData[key]);
        }

        try {
            const response = await fetch("https://fastapi-app-production-c1ed.up.railway.app/predict", {

                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams(jsonData)
            });

            const data = await response.json();
            
            if (response.ok) {
                document.getElementById("result").innerHTML = 
                    `<strong>Prediction:</strong> ${data.prediction === 1 ? "High Risk" : "Low Risk"}`;
            } else {
                document.getElementById("result").innerHTML = 
                    `<strong>Error:</strong> ${data.error}`;
            }

        } catch (error) {
            document.getElementById("result").innerHTML = `<strong>Error:</strong> ${error}`;
        }
    });
});
