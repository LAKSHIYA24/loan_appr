document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loanForm');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const data = {};
            for (const [key, value] of formData.entries()) {
                data[key] = value;
            }

            fetch('/api/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(result => {
                if (result.result) {
                    localStorage.setItem('loan_result', result.result);
                    window.location.href = '/result';
                } else {
                    alert("Error: " + result.error);
                }
            })
            .catch(error => {
                alert("Failed to predict: " + error);
            });
        });
    }
});
