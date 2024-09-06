document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const resultsContainer = document.getElementById("results");
    const downloadBtn = document.getElementById("download-btn");

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/upload", true);

        xhr.onload = function() {
            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                displayEmails(response.valid_emails, response.invalid_emails);
                if (response.valid_emails.length > 0) {
                    downloadBtn.style.display = "inline-block";
                }
            }
        };

        xhr.send(formData);
    });

    function displayEmails(validEmails, invalidEmails) {
        resultsContainer.innerHTML = ''; // Clear previous results
        resultsContainer.style.display = "block";

        let index = 0;
        const totalEmails = validEmails.length + invalidEmails.length;
        const allEmails = validEmails.map(email => ({ email, isValid: true }))
            .concat(invalidEmails.map(email => ({ email, isValid: false })));

        function showNextEmail() {
            if (index < totalEmails) {
                const emailData = allEmails[index];
                const emailElement = document.createElement("li");
                emailElement.textContent = emailData.email;
                emailElement.style.color = emailData.isValid ? "green" : "red";
                resultsContainer.appendChild(emailElement);
                index++;
                setTimeout(showNextEmail, 500); // Adjust the delay as needed
            }
        }

        showNextEmail();
    }
});
