document.addEventListener('DOMContentLoaded', function() {
    var saveButton = document.getElementById('save');
    var userForm = document.getElementById('updateUser');

    if (saveButton && userForm) {
        saveButton.addEventListener('click', function() {
            userForm.submit();
        });
    }
});