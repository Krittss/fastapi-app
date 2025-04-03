document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("screening-form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        let dataList = [];

        // Convert form values to integers and store in an array
        for (let key of formData.keys()) {
            dataList.push(parseInt(formData.get(key)));
        }

        try {
            const response = await fetch("http://127.0.0.1:8000/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ "data": dataList })  // Send data in correct JSON format
            });

            const data = await response.json();
            
            if (response.ok) {
                document.getElementById("result").innerHTML = 
                    `<strong>Prediction:</strong> ${data.prediction}`;
            } else {
                document.getElementById("result").innerHTML = 
                    `<strong>Error:</strong> ${data.error}`;
            }

        } catch (error) {
            document.getElementById("result").innerHTML = `<strong>Error:</strong> ${error.message}`;
        }
    });
});
 