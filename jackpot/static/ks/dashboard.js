document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById('bucket-modal');
    const closeBtn = document.getElementsByClassName('close-btn')[0];
    const addBucketBtn = document.querySelector('.add-bucket-btn');

    // Show the modal when the button is clicked
    addBucketBtn.addEventListener('click', function () {
        modal.style.display = 'flex';
    });

    // Close the modal
    closeBtn.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Close the modal if clicked outside
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Handle bucket form submission via AJAX
    const bucketForm = document.getElementById('bucket-form');
    bucketForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submit

        const formData = new FormData(bucketForm);

        fetch('/create-bucket/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Bucket created!');
                location.reload(); // Reload the page
            } else {
                alert('Error creating bucket');
            }
        });
    });

    // Function to retrieve CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
