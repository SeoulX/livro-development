document.addEventListener('DOMContentLoaded', function () {
    var confirmationMessage = document.getElementById('confirmation-message');
    var confirmDeleteButton = document.getElementById('confirm-delete');
    var cancelDeleteButton = document.getElementById('cancel-delete');

    var currentBookId;

    function showConfirmation(bookId) {
        confirmationMessage.style.display = 'block';
        currentBookId = bookId;
    }

    function hideConfirmation() {
        confirmationMessage.style.display = 'none';
    }

    document.querySelectorAll('.delete-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            var bookId = button.getAttribute('data-book-id');
            showConfirmation(bookId);
        });
    });

    confirmDeleteButton.addEventListener('click', function () {
        // Use AJAX to delete the book

        // Get the CSRF token from the cookie
        var csrftoken = getCookie('csrftoken');

        fetch(`/delete_book/${currentBookId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            // Add an empty body for the POST request
            body: JSON.stringify({}),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Handle success, e.g., show a message or update the UI
                console.log('Book deleted successfully');
                hideConfirmation();
                // Reload the HTML to reflect the changes
                location.reload();
            } else {
                // Handle failure, e.g., show an error message
                console.error('Error deleting book:', data.error);
            }
        })
        .catch(error => console.error('Error deleting book:', error));
    });

    cancelDeleteButton.addEventListener('click', function () {
        hideConfirmation();
    });

    // Function to get the CSRF token from the cookie
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
