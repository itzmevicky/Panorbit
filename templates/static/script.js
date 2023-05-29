function submitForm(event) {
    event.preventDefault(); // Prevent default form submission

    // Get form data
    const form = document.getElementById('user-form');
    const formData = new FormData(form);

    // Make AJAX POST request to the API endpoint
    fetch('http://127.0.0.1:8000/register/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response
        if (data.success) {
            alert('Your account has been created. Please login.');
            console.log('Account Created');
            window.location.href = '/login'; // Redirect to login page
        } else {
            alert('An error occurred. Please try again.');
        }
    })
    .catch(error => {
        console.log(error);
        alert('An error occurred. Please try again.');
    });
}

// Add event listener to the form submit button
const submitButton = document.getElementById('submit-button');
submitButton.addEventListener('click', submitForm);