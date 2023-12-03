document.addEventListener('DOMContentLoaded', function() {
    var saveButton = document.getElementById('Upload');
    var bookForm = document.getElementById('addBookForm');

    if (saveButton && bookForm) {
        saveButton.addEventListener('click', function() {
            bookForm.submit();
        });
    }
});

function addGenre() {
    var genreSelect = document.getElementById("genres");
    var genreInput = document.getElementById("genreText");

    var selectedGenre = genreSelect.options[genreSelect.selectedIndex].value;

    if (genreInput.value.indexOf(selectedGenre) === -1) {
        if (genreInput.value === "") {
            genreInput.value = selectedGenre;
        } else {
            genreInput.value += ", " + selectedGenre;
        }
    }
}

document.getElementById('getCover').addEventListener('click', function(e) {
    e.preventDefault();
    document.getElementById('coverInput').click();
});

function previewCoverImage(input) {
    var preview = document.getElementById('coverPreview');
    var file = input.files[0];

    if (file) {
        var reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
        };

        reader.readAsDataURL(file);
    }
}



